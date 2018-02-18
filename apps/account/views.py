# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

#import de python
import datetime

#importaciones que realiza django por defecto
from django.shortcuts import render, redirect

#Importando los modelos a usar
from apps.account.models import Account
from apps.varios.models import Descarga, Top
from apps.player.models import Guild
from django.db.models import Q

#importando los formularios a usar
from apps.account.forms import  CreateUserForm, \
                                CustomLoginForm, \
                                CustomChangePassword,\
                                ResPassword, \
                                FormResetPassword,\
                                CustomDesbugForm

#importando funciones varias para el correcto funcionamiento de la web
from apps.account.funciones import *

#importando libreria para enviar correo
from django.core.mail import send_mail

#importando funciones integradas en el framework
from django.views.generic import CreateView, DetailView, ListView
from django.views import View
from django.http import HttpResponseRedirect , HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone

#importando las configuracines de django
from core import settings

#clase usada para el registro de usuarios
class Create(CreateView):
  success_url = reverse_lazy('account:exito')
  template_name = 'account/registro.html'
  model = Account
  form_class = CreateUserForm
  def form_valid(self,form):
    key = aleatorio(40)
    self.object = form.save(commit=False)
    new_password = self.object.micryp( self.object.password )
    self.object.password = new_password
    self.object.address = key
    self.object.save()
    try:
      send_mail(
              'Bienvenido a '+ settings.SERVERNAME,
              'Content',
              settings.EMAIL_HOST_USER ,
              [self.object.email],
              html_message=get_mail_register(self.object.login,key),
            )
    except:
      pass
    return HttpResponseRedirect( self.get_success_url() )
  def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        context.update(contexto())
        return context

#funcion usada para el login
#Refactorizando la funcion de login
class login(View):

    template_name = 'account/login.html'
    template_name_login = 'account/logon.html'
    modelA = Account
    modelB = Top
    form = CustomLoginForm

    def __init__(self):
        super(login,self).__init__()
        self.context = contexto()

    def get(self, request):
        form = self.form()
        if request.session.has_key('g1jwvO'):
            userinfo = self.modelA.objects.get(id=request.session['g1jwvO'])
            pjinfo = self.modelB.objects.filter(account_id=userinfo.id)
            self.context.update({
                'session': userinfo,
                'personajes': pjinfo
            })
            return render(request, self.template_name_login, self.context)
        else:
            pass

        self.context.update({
            'form':form
        })
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = self.form(request.POST or None)
        if form.is_valid():
            try:
                a = self.modelA.objects.get(login=form.cleaned_data['login'])
            except Account.DoesNotExist:
                self.context.update({
                    'key':'Nombre de usuario o password incorrecto',
                    'form':form
                })
                return render(request, self.template_name, self.context)

            b = a.micryp(form.cleaned_data['password'])
            #Validando que las contraseñas coincidan
            if a.password == b:
                #Validando que la cuenta no este baneada
                if a.status == 'OK':
                    request.session['g1jwvO'] = a.id
                    if request.session.has_key('g1jwvO'):
                        return redirect('account:login')
                else:
                    self.context.update({
                        'key':'Tu cuenta esta baneada',
                        'form':form
                    })
                    return render(request, self.template_name, self.context)

            else:
                self.context.update({
                    'key':'Nombre de usuario o password incorrecto',
                    'form':form
                })
                return render(request, self.template_name, self.context)

        else:
            self.context.update({
                'key':'Rellene todos los campos correctamente',
                'form':form
            })
            return render(request, self.template_name, self.context)

#funcion usada para cerra session
def logout(request):
  try:
    a = Account.objects.get(id=request.session['g1jwvO'])
    del request.session['g1jwvO']
  except:
  	a = {
        'real_name':'invalido'
    }
  context = contexto()
  context.update({
    'datos': a
  })
  return render(request, 'account/salir.html',  context  )

#funcion usada para cambiar password estando logeado
def changepasswd(request):
  """Declarando el formulario que usara esta funcion  """
  form = CustomChangePassword(request.POST or None)
  """Preparado el contexto usado por la funcion"""
  context = contexto()
  context.update({
    'form':form
  })
  if request.session.has_key('g1jwvO'):
    try:
      a = Account.objects.get(id=request.session['g1jwvO'])
    except Account.DoesNotExist:
      pass
    if request.method == 'POST':
    	if request.POST['new_password'] == request.POST['new_password_again']:
    		if a.password == a.micryp(request.POST['password']):
    			if form.is_valid():
    				new_password = a.micryp( form.cleaned_data['new_password'] )
    				a.password = new_password
    				a.save()
    				context.update({'key':'se ha cambiado el password exitosamente.'})
    				return render(request, 'account/password.html', context )
    		else:
    			context.update({'key':'El password no es correcto'})
    			return render(request, 'account/password.html', context )
    	else:
    		#'contraseas no coinciden'
    		context.update({'key':'Los password no coinciden'})
    		return render(request, 'account/password.html', context )
    else:
    	return render(request, 'account/password.html' , context )
  else:
  	return redirect('account:login')

#Funcion usada para confirmar el registro exitoso
#Esta funcion demuestra que aveces lo mas simple, es lo que mejor funciona.
def exito(request):
  return render(request, 'account/exito.html', contexto())

#Clase que se uso para realizar comparacion entre una funcion y una Clase
#Cuando hicimos los test el rendimiento de esta clase en comparacion con la funcion exito
#El rendimiento de la funcion fue superior, aparte la funcion exito solo tenia una linea de codigo
#Esto permitia que fuera procesada en menos tiempo en comparacion con lesta clase
class ExitoRefine(View):
    #primero definimos el template o skin que se usara en la pagina.
    template_name = 'account/exito.html'

    #Ahora vamos a crear un contexto personalizado, este contexto se usara para renderizarlo
    #en el template que se definio primero.
    def __init__(self):
        super(ExitoRefine, self).__init__()
        self.context = contexto()

    #Se sobre escribe el methodo get, esto para atender este tipo de peticiones.
    def get(self,request):
        #Se renderiza el template con el contexto.
        return render(request,self.template_name, self.context)

#clase usada para la pagina de descargas.
class Descargas(View):
    model = Descarga
    template_name = 'account/download.html'

    def __init__(self):
        super(Descargas,self).__init__()
        self.context = contexto()

    def get(self, request):
        self.context.update({
            'descarga': self.model.objects.publicado(),
        })
        return render(request, self.template_name, self.context)

#clase usada para la pagina del ranking del juego y paginarlo
class top(ListView):
  model = Top
  template_name = 'account/top100.html'
  #context_object_name = 'player'
  queryset = Top.objects.all().exclude(Q(name__contains='[')).order_by('-level','ranking')
  #queryset = Player.objects.filter(string__contains='[%]%')
  paginate_by = 20

  def get_context_data(self, **kwargs):
        context = super(top, self).get_context_data(**kwargs)
        context.update(contexto())
        return context

#clase usada para renderizar el top del juego y paginarlo
class top_g(ListView):
  model = Guild
  template_name = 'account/top_g.html'
  queryset = Guild.objects.all().order_by('-level','-exp','-win', '-ladder_point')
  paginate_by = 20

  def get_context_data(self, **kwargs):
        context = super(top_g, self).get_context_data(**kwargs)
        context.update(contexto())
        return context

#Funcion usada para recuperar password por correo
"""Realizar refactorin a esta funcion """
def recuperar_password(request):
    """Declarando el formulario"""
    form = ResPassword(request.POST or None)
    """Preparando el contexto que manajara la funcion"""
    context = contexto()
    context.update({
        'form': form
    })
    #validando los datos que se envian por post
    if request.method == 'POST' and form.is_valid():
      a = request.POST['login']
      b = request.POST['email']
      try:
        usuario = Account.objects.get(login=a)
      except Account.DoesNotExist:
        context.update({'key': 'No se encuentran registros en nuestra base de datos'})
        return render(request, 'account/rescue.html', context)

      if usuario.email == b:
        key = aleatorio(40)
        usuario.address = key
        usuario.token_expire = timezone.now()
        usuario.save()
        try:
            send_mail(
              'Recuperar password',
              'Content',
              settings.EMAIL_HOST_USER ,
              [usuario.email],
              html_message=get_mail(usuario.real_name,key),
            )

            context.update({'key': 'se ha enviado un correo electronico con las instrucciones para recupear el password'})
            return render(request, 'account/rescue.html', context)
        except:
            context.update({'key': 'Error enviando el correo'})
            return render(request, 'account/rescue.html', context)
      else:
        context.update({'key': 'El usuario no concuerda con el correo electronico'})
        return render(request, 'account/rescue.html', context)
    else:
      context.update({'key': ''})
      return render(request, 'account/rescue.html', context)

#Procesando el correo de recuperacion de password.
def process_password(request,url):
  """Declarando el formulario"""
  form = FormResetPassword(request.POST or None)
  """Preparando el contexto de la funcion"""
  context = contexto()
  if request.method == 'GET':
    if url:
      try:
        a = Account.objects.get(address=url)
      except:
        context.update({
            'key': 'El token que intentas usar no existe',
            'if_form': False
        })
        return render(request, 'account/cambio_passwd.html', context)
      z = (timezone.now() - a.token_expire).days
      if z >= 1:
        context.update({
            'key': 'El token que intentas usar esta vencido',
            'if_form': False
        })
        return render(request, 'account/cambio_passwd.html' , context)
      else:
        request.session['tmp_id'] = a.id
        context.update({
            'key': 'ingresa tu nuevo password',
            'form': form,
            'if_form': True
        })
        return render(request, 'account/cambio_passwd.html' , context)
    else:
      context.update({
          'key': 'No has enviado ningun token',
          'if_form': False
      })
      return render(request, 'account/cambio_passwd.html', context)
  if request.method == 'POST':
    password = request.POST['password']
    password_again = request.POST['password_again']
    if password == password_again and form.is_valid():
      if request.session.has_key('tmp_id'):
        try:
          a = Account.objects.get(id=request.session['tmp_id'])
        except:
          context.update({
              'key': 'No se encuentra el usuario',
              'if_form': False
          })
          return render(request, 'account/cambio_passwd.html', context)
        a.password = a.micryp(password)
        a.address = aleatorio(40)
        a.save()
        del request.session['tmp_id']
        context.update({
            'key': 'Password actualizado correctamente',
            'if_form': False
        })
        return render(request, 'account/cambio_passwd.html', context)
      else:
        context.update({
            'key': 'No existe la session temporal',
            'if_form': False
        })
        return render(request, 'account/cambio_passwd.html', context )
    else:
      context.update({
          'if_form': True,
          'key':'Los password no coinciden'
      })
      return render(request, 'account/cambio_passwd.html', context)

#Aqui validamos los link's de activacion de la cuenta.
def process_reg(request, url):
  """Preparando el contexto usado por la funcion """
  context = contexto()
  if request.method == 'GET':
    if url:
      try:
        a = Account.objects.get(address=url)
      except:
        context.update({'key': 'El token que intentas usar no existe.'})
        return render(request, 'account/activar_cuenta.html', context)
      if a.status == 'OK':
        b = datetime.datetime(2009, 1, 1, 0, 0,)
        if a.availdt.year == b.year and a.availdt.month == b.month:
          a.address = aleatorio(40)
          a.save()
          context.update({'key': 'Tu cuenta ya esta activada'})
          return render(request, 'account/activar_cuenta.html', context )
        else:
          a.availdt = "2009-01-01T00:00:00"
          a.address = aleatorio(40)
          a.save()

          context.update({'key': 'Tu cuenta se ha activado correctamente'})
          return render(request, 'account/activar_cuenta.html', context )
      else:
        context.update({'key': 'Tu cuenta esta baneada'})
        return render(request, 'account/activar_cuenta.html', context )
    else:
      context.update({'key': 'No has enviado ningun token'})
      return render(request, 'account/activar_cuenta.html', context)
  else:
    context.update({'key': 'Metodo no admitido'})
    return render(request, 'account/activar_cuenta.html', context)

def desbuguear(request):
    """Declarando el formulario que usara la funcion """
    form = CustomDesbugForm(request.POST or None)
    """Preparando el contexto usado por la funcion """
    context = contexto()
    context.update({
        'form': form,
    })
    if request.session.has_key('g1jwvO'):
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
                            'key':'Se ha desbugeado tu personaje correctamente debes esperar 30 min para iniciar con el.',
                            'if_form': True
                        })
                        return render(request,'account/unlock.html', context)
                    else:
                        context.update({
                            'key':'Error desbugueando.',
                            'if_form': True
                        })
                        return render(request,'account/unlock.html', context)
            context.update({
                'key':'Ningun personaje coincide.',
                'if_form': True
            })
            return render(request ,'account/unlock.html', context)

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

#Clase usada para re enviar el correo de activacion , en caso de que no llegue.
class requestToken(View):

    template_name = 'account/envio_token.html'
    model = Account
    form = ResPassword

    def __init__(self):
        super(requestToken,self).__init__()
        self.context = contexto()

    def get(self, request):
        form = self.form(request.POST or None)
        self.context.update({
            'form':form
        })
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = self.form(request.POST or None)
        self.context.update({'form':form})
        if form.is_valid():
            try:
                a = self.model.objects.get(login=form.cleaned_data['login'])
            except Account.DoesNotExist:
                self.context.update({
                    'key':'Cuenta no existe.'
                })
                return render(request, self.template_name, self.context)

            b = datetime.datetime(2009, 1, 1, 0, 0,)
            if a.availdt.year == b.year and a.availdt.month == b.month:
                self.context.update({
                    'key': 'Tu cuenta ya esta activada',
                })
                return render(request, self.template_name, self.context)

            if a.status != 'OK':
                self.context.update({
                    'key':'Tu cuenta esta baneada'
                })
                return render(request, self.template_name, self.context)

            if form.cleaned_data['email'] == a.email:
                key = aleatorio(40)
                a.address = key
                a.save()
                try:
                    send_mail(
                        'Activacion de cuentas '+settings.SERVERNAME,
                        'Content',
                        settings.EMAIL_HOST_USER ,
                        [a.email],
                        html_message=get_mail_register(a.login,key)
                    )
                except:
                    self.context.update({
                        'key':'Error enviando correo al usuario'
                    })
                    return render(request, self.template_name, self.context)

                self.context.update({
                    'key':'Se ha enviado el codigo de activacion al email'
                })
                return render(request, self.template_name, self.context)
            else:
                self.context.update({
                    'key': 'El email no coincide con el usuario'
                })
                return render(request, self.template_name, self.context)
        else:
            self.context.update({
                'key':'Por favor rellena todos los campos correctamente.'
            })
            return render(request, self.template_name, self.context)
