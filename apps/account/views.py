# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# import de datetime nativo de python
import datetime

# importaciones que realiza django por defecto
from django.shortcuts import render, redirect

# Importando los modelos a usar
from apps.account.models import Account
from apps.varios.models import Descarga, Top
from apps.player.models import Guild

# importando los formularios a usar
from apps.account.forms import (
    CreateUserForm,
    CustomLoginForm,
    CustomChangePassword,
    ResPassword,
    FormResetPassword,
    CustomDesbugForm,
    FormRequestPassword
)

# importando funciones varias para el correcto funcionamiento de la web
from apps.account.funciones import (
    guild_top,
    player_top,
    aleatorio,
    get_mail,
    get_mail_register,
    get_mail_username,
    cambio_mapa,
    lenguaje
)

# importando libreria para enviar correo
from django.core.mail import send_mail

# importando funciones integradas en el framework
from django.views.generic import (
    CreateView,
    ListView
)

# Importando execiones personalizadas
from apps.account.excepciones import InternalServerError, SendMailException

# Importaciones adicionales de django
from django.views import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone

# importando clase usada para la traduccion
# from django.utils import translation
from django.utils.translation import ugettext as _

# importando las configuracines de django
from core import settings


# clase usada para el registro de usuarios
class Create(CreateView):
    success_url = reverse_lazy('account:exito')
    template_name = 'account/registro.html'
    model = Account
    form_class = CreateUserForm

    def get(self, request):
        lenguaje(request)
        return super(Create, self).get(request)

    def post(self, request):
        lenguaje(request)
        return super(Create, self).post(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'refer' in self.request.GET:
            context['refer_id'] = self.request.GET.get('refer')
        return context

    def form_valid(self, form):
        key = aleatorio(40)
        self.object = form.save(commit=False)
        new_password = self.object.micryp(self.object.password)
        self.object.password = new_password
        self.object.address = key
        if 'refer_id' in self.request.POST:
            self.object.refer_id = self.request.POST['refer_id']
        self.object.save()
        try:
            send_mail(
                _('Bienvenido a ') + settings.SERVERNAME,
                'Content',
                settings.EMAIL_HOST_USER,
                [self.object.email],
                html_message=get_mail_register(self.object.login, key),
                )
        except Exception as err:
            raise SendMailException(err)
        return HttpResponseRedirect(self.get_success_url())


# funcion usada para el login
# Refactorizando la funcion de login
class Login(View):

    template_name = 'account/login.html'
    template_name_login = 'account/logon.html'
    modelA = Account
    modelB = Top
    form = CustomLoginForm

    def get(self, request):
        lenguaje(request)
        form = self.form()

        if 'g1jwvO' in request.session:
            userinfo = self.modelA.objects.get(id=request.session['g1jwvO'])
            pjinfo = self.modelB.objects.filter(account_id=userinfo.id)
            context = {
                'session': userinfo,
                'personajes': pjinfo
            }
            return render(request, self.template_name_login, context)
        else:
            pass

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        lenguaje(request)
        form = self.form(request.POST or None)

        if form.is_valid():
            try:
                a = self.modelA.objects.get(login=form.cleaned_data['login'])
            except Account.DoesNotExist:
                context = {
                    'key': _('Nombre de usuario o password incorrecto'),
                    'form': form
                }
                return render(request, self.template_name, context)

            b = a.micryp(form.cleaned_data['password'])
            # Validando que las contraseñas coincidan
            if a.password == b:
                # Validando que la cuenta no este baneada
                if a.status == 'OK':
                    request.session['g1jwvO'] = a.id
                    if 'g1jwvO' in request.session:
                        return redirect('account:login')
                else:
                    context = {
                        'key': _('Tu cuenta esta baneada'),
                        'form': form
                    }
                    return render(request, self.template_name, context)

            else:
                context = {
                    'key': _('Nombre de usuario o password incorrecto'),
                    'form': form
                }
                return render(request, self.template_name, context)

        else:
            context = {
                'key': _('Rellene todos los campos correctamente'),
                'form': form
            }
            return render(request, self.template_name, context)


# funcion usada para cerra session
def logout(request):
    lenguaje(request)

    try:
        a = Account.objects.get(id=request.session['g1jwvO'])
        del request.session['g1jwvO']
    except Account.DoesNotExist:
        a = {
            'real_name': _('invalido')
        }
    context = {
        'datos': a
    }
    return render(request, 'account/salir.html', context)


# funcion usada para cambiar password estando logeado
def changepasswd(request):
    lenguaje(request)
    # Declarando el formulario que usara esta funcion
    form = CustomChangePassword(request.POST or None)
    # Preparado el contexto usado por la funcion
    context = {
        'form': form
    }
    if 'g1jwvO' in request.session:
        try:
            a = Account.objects.get(id=request.session['g1jwvO'])
        except Account.DoesNotExist:
            pass
        if request.method == 'POST':
            if request.POST['new_password'] == request.POST['new_password_again']:
                if a.password == a.micryp(request.POST['password']):
                    if form.is_valid():
                        new_password = a.micryp(form.cleaned_data['new_password'])
                        a.password = new_password
                        a.save()
                        context.update({'key': _('se ha cambiado el password exitosamente.')})
                        return render(request, 'account/password.html', context)
                else:
                    context.update({'key': _('El password no es correcto')})
                    return render(request, 'account/password.html', context)
            else:
                # contraseas no coinciden
                context.update({'key': _('Los password no coinciden')})
                return render(request, 'account/password.html', context)
        else:
            return render(request, 'account/password.html', context)
    else:
        return redirect('account:login')


# Funcion usada para confirmar el registro exitoso
# Esta funcion demuestra que aveces lo mas simple, es lo que mejor funciona.
def exito(request):
    lenguaje(request)
    return render(request, 'account/exito.html')


"""
Clase que se uso para realizar comparacion entre una funcion y una Clase
Cuando hicimos los test el rendimiento de esta clase en comparacion con la funcion exito
El rendimiento de la funcion fue superior, aparte la funcion exito solo tenia una linea de codigo
Esto permitia que fuera procesada en menos tiempo en comparacion con esta clase 
"""


class ClaseExito(View):
    # primero definimos el template o skin que se usara en la pagina.
    template_name = 'account/exito.html'

    # Se sobre escribe el methodo get, esto para atender este tipo de peticiones.
    def get(self, request):
        lenguaje(request)
        # Se renderiza el template con el contexto.
        return render(request, self.template_name)


# Clase usada para la pagina de descargas.
class Descargas(View):
    model = Descarga
    template_name = 'account/download.html'

    def get(self, request):
        lenguaje(request)

        context = {
            'descarga': self.model.objects.publicado(),
        }
        return render(request, self.template_name, context)


# clase usada para la pagina del ranking del juego y paginarlo
class ClasificacionPersonajes(ListView):
    model = Top
    template_name = 'account/top100.html'
    queryset = player_top()
    paginate_by = 20

    def get(self, request):
        lenguaje(request)
        return super(ClasificacionPersonajes, self).get(request)


# Clase usada para renderizar el top del juego y paginarlo
class ClasificacionGremios(ListView):
    model = Guild
    template_name = 'account/top_g.html'
    queryset = guild_top()
    paginate_by = 20

    def get(self, request):
        lenguaje(request)
        return super(ClasificacionGremios, self).get(request)


# Funcion usada para recuperar password por correo
# Realizar refactorin a esta funcion
def recuperar_password(request):
    lenguaje(request)
    # Declarando el formulario
    form = ResPassword(request.POST or None)
    # Preparando el contexto que manajara la funcion
    context = {
        'form': form
    }
    # validando los datos que se envian por post
    if request.method == 'POST' and form.is_valid():
        a = request.POST['login']
        b = request.POST['email']
        try:
            usuario = Account.objects.get(login=a)
        except Account.DoesNotExist:
            context.update({'key': _('No se encuentran registros en nuestra base de datos')})
            return render(request, 'account/rescue.html', context)

        if usuario.email == b:
            key = aleatorio(40)
            usuario.address = key
            usuario.token_expire = timezone.now()
            usuario.save()
            try:
                send_mail(
                    _('Recuperar password'),
                    'Content',
                    settings.EMAIL_HOST_USER,
                    [usuario.email],
                    html_message=get_mail(usuario.real_name, key),
                )

                context.update({'key': _('se ha enviado un correo electronico con las instrucciones '
                                         'para recupear el password')})
                return render(request, 'account/rescue.html', context)
            except SendMailException:
                context.update({'key': _('Error enviando el correo')})
                return render(request, 'account/rescue.html', context)
        else:
            context.update({'key': _('El usuario no concuerda con el correo electronico')})
            return render(request, 'account/rescue.html', context)
    else:
        context.update({'key': ''})
        return render(request, 'account/rescue.html', context)


# Procesando el correo de recuperacion de password.
def process_password(request, url):
    lenguaje(request)
    # Declarando el formulario
    form = FormResetPassword(request.POST or None)
    # Preparando el contexto de la funcion
    context = {}
    if request.method == 'GET':
        if url:
            try:
                a = Account.objects.get(address=url)
            except Account.DoesNotExist:
                context.update({
                    'key': _('El token que intentas usar no existe'),
                    'if_form': False
                })
                return render(request, 'account/cambio_passwd.html', context)
            z = (timezone.now() - a.token_expire).days
            if z >= 1:
                context.update({
                    'key': _('El token que intentas usar esta vencido'),
                    'if_form': False
                })
                return render(request, 'account/cambio_passwd.html', context)
            else:
                request.session['tmp_id'] = a.id
                context.update({
                    'key': _('ingresa tu nuevo password'),
                    'form': form,
                    'if_form': True
                })
                return render(request, 'account/cambio_passwd.html', context)
        else:
            context.update({
                'key': _('No has enviado ningun token'),
                'if_form': False
            })
            return render(request, 'account/cambio_passwd.html', context)
    if request.method == 'POST':
        password = request.POST['password']
        password_again = request.POST['password_again']
        if password == password_again and form.is_valid():
            if 'tmp_id' in request.session:
                try:
                    a = Account.objects.get(id=request.session['tmp_id'])
                except Account.DoesNotExist:
                    context.update({
                        'key': _('No se encuentra el usuario'),
                        'if_form': False
                    })
                    return render(request, 'account/cambio_passwd.html', context)
                a.password = a.micryp(password)
                a.address = aleatorio(40)
                a.save()
                del request.session['tmp_id']
                context.update({
                    'key': _('Password actualizado correctamente'),
                    'if_form': False
                })
                return render(request, 'account/cambio_passwd.html', context)
            else:
                context.update({
                    'key': _('No existe la session temporal'),
                    'if_form': False
                })
                return render(request, 'account/cambio_passwd.html', context )
        else:
            context.update({
                'if_form': True,
                'key':_('Los password no coinciden')
            })
            return render(request, 'account/cambio_passwd.html', context)


# Aqui validamos los link's de activacion de la cuenta.
def process_reg(request, url):
    lenguaje(request)
    # Preparando el contexto usado por la funcion
    context = {}
    if request.method == 'GET':
        if url:
            try:
                a = Account.objects.get(address=url)
            except Account.DoesNotExist:
                context.update({'key': _('El token que intentas usar no existe.')})
                return render(request, 'account/activar_cuenta.html', context)
            if a.status == 'OK':
                b = datetime.datetime(2009, 1, 1, 0, 0,)
                if a.availdt.year == b.year and a.availdt.month == b.month:
                    a.address = aleatorio(40)
                    a.save()
                    context.update({'key': _('Tu cuenta ya esta activada')})
                    return render(request, 'account/activar_cuenta.html', context )
                else:
                    a.availdt = "2009-01-01T00:00:00"
                    a.address = aleatorio(40)
                    a.save()

                    context.update({'key': _('Tu cuenta se ha activado correctamente')})
                    return render(request, 'account/activar_cuenta.html', context )
            else:
                context.update({'key': _('Tu cuenta esta baneada')})
                return render(request, 'account/activar_cuenta.html', context )
        else:
            context.update({'key': _('No has enviado ningun token')})
            return render(request, 'account/activar_cuenta.html', context)
    else:
        context.update({'key': _('Metodo no admitido')})
        return render(request, 'account/activar_cuenta.html', context)


def desbuguear(request):
    lenguaje(request)
    # Declarando el formulario que usara la funcion
    form = CustomDesbugForm(request.POST or None)
    # Preparando el contexto usado por la funcion
    context = {
        'form': form,
    }
    if 'g1jwvO' in request.session:
        try:
            a = Account.objects.get(id=request.session['g1jwvO'])
        except Account.DoesNotExist:
            pass

        if request.method == 'POST' and form.is_valid():
            b = form.cleaned_data['nombre']
            c = Top.objects.filter(account_id=a.id)
            for personaje in c:
                if str.lower(personaje.name) == str.lower(b):
                    resultado = cambio_mapa(a.id, personaje.name)
                    if resultado:
                        context.update({
                            'key': _('Se ha movido tu personaje correctamente debes esperar '
                                     '30 min para iniciar con el.'),
                            'if_form': True
                        })
                        return render(request, 'account/unlock.html', context)
                    else:
                        context.update({
                            'key': _('Error moviendo personaje'),
                            'if_form': True
                        })
                        return render(request, 'account/unlock.html', context)
            context.update({
                'key': _('Ningun personaje coincide.'),
                'if_form': True
            })
            return render(request, 'account/unlock.html', context)

        if request.method == 'GET':
            pj = Top.objects.filter(account_id=request.session['g1jwvO'])
            if pj.count() == 0:
                return redirect('account:login')
            context.update({
                'if_form': True,
                'form': form
            })
            return render(request,'account/unlock.html', context)
    else:
        return redirect('account:login')


# Clase usada para re enviar el correo de activacion, en caso de que no llegue.
class RequestToken(View):

    template_name = 'account/envio_token.html'
    model = Account
    form = ResPassword

    def get(self, request):
        lenguaje(request)
        form = self.form(request.POST or None)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        lenguaje(request)
        form = self.form(request.POST or None)
        context = {
            'form': form
        }
        if form.is_valid():
            try:
                a = self.model.objects.get(login=form.cleaned_data['login'])
            except Account.DoesNotExist:
                context.update({
                    'key': _('Cuenta no existe.')
                })
                return render(request, self.template_name, context)

            b = datetime.datetime(2009, 1, 1, 0, 0,)
            if a.availdt.year == b.year and a.availdt.month == b.month:
                context.update({
                    'key': _('Tu cuenta ya esta activada'),
                })
                return render(request, self.template_name, context)

            if a.status != 'OK':
                context.update({
                    'key': _('Tu cuenta esta baneada')
                })
                return render(request, self.template_name, context)

            if form.cleaned_data['email'] == a.email:
                key = aleatorio(40)
                a.address = key
                a.save()
                try:
                    send_mail(
                        _('Activacion de cuentas ')+settings.SERVERNAME,
                        'Content',
                        settings.EMAIL_HOST_USER,
                        [a.email],
                        html_message=get_mail_register(a.login, key)
                    )
                except SendMailException:
                    context.update({
                        'key': _('Error enviando correo al usuario')
                    })
                    return render(request, self.template_name, context)

                context.update({
                    'key': _('Se ha enviado el codigo de activacion al email')
                })
                return render(request, self.template_name, context)
            else:
                context.update({
                    'key': _('El email no coincide con el usuario')
                })
                return render(request, self.template_name, context)
        else:
            context.update({
                'key': _('Por favor rellena todos los campos correctamente.')
            })
            return render(request, self.template_name, context)


class RequestUsername(View):
    template_name = 'account/usernames.html'
    model = Account
    form = FormRequestPassword

    def get(self, request):
        lenguaje(request)
        form = self.form(request.POST or None)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        lenguaje(request)
        form = self.form(request.POST or None)
        context = {
            'form': form
        }
        if form.is_valid():
            accounts = Account.objects.filter(email=form.cleaned_data['email'])
            if len(accounts) == 0:
                context.update({
                    'key': _('No se encontraron cuentas asociadas al email')
                })
                return render(request, self.template_name, context)
            try:
                send_mail(
                    _('Cuentas asociadas al correo ') + settings.SERVERNAME,
                    'content',
                    settings.EMAIL_HOST_USER,
                    [form.cleaned_data['email']],
                    html_message=get_mail_username(accounts)
                )
            except SendMailException as err:
                context.update({'err': err})
                return render(request, self.template_name, context)
            context.update({
                'key': _('Correo enviado exitosamente')
            })
            return render(request, self.template_name, context)

        else:
            return render(request, self.template_name, context)
