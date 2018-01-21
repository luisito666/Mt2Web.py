# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

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
""" es necesario agregar re factorin a esta funcion """
def login(request):
  """Declarando el formulario que usara esta funcion  """
  form = CustomLoginForm(request.POST or None)
  """Preparado el contexto usando por la funcion"""
  context = contexto()
  if request.session.has_key('id'):
    a = Account.objects.get(id=request.session['id'])
    b = Top.objects.filter(account_id=a.id)
    context.update({
        'session': a ,
        'personajes': b
    })
    return render(request, 'account/logon.html', context)
  else:
    if request.method == 'POST':  #Validando que los datos vengan por post
      if form.is_valid():
        try:
          a = Account.objects.get(login=request.POST['login'])  #obteniendo datos de usuario
        except Account.DoesNotExist:
          context.update({
              'key':'El nombre de usuario no existe',
              'form': form
          })
          return render(request, 'account/login.html', context)
      else:
        context.update({
            'key':'Por favor no deje campos en blanco',
            'form': form
        })
        return render(request, 'account/login.html', context )
      b = a.micryp(request.POST['password']) #uso implicito de cursor para encriptar password
      if a.password == b:
        request.session['id'] = a.id
      if request.session.has_key('id'):
        b = Top.objects.filter(account_id=a.id)
        context.update({
            'session': a ,
            'personajes': b
        })
        return render(request, 'account/logon.html', context )
      else:
        context.update({
            'key':'Nombre de usuario o password incorrecto',
            'form': form
        })
        return render(request, 'account/login.html',  context, )
    else:
      context.update({
          'key': '',
          'form': form
      })
      return render(request,'account/login.html', context)

#funcion usada para cerra session
def logout(request):
  try:
    a = Account.objects.get(id=request.session['id'])
    del request.session['id']
  except:
  	pass
  b = Top.objects.filter(account_id=a.id)
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
  if request.session.has_key('id'):
    try:
      a = Account.objects.get(id=request.session['id'])
    except Account.DoesNotExist:
      pass
    if request.method == 'POST':
    	if request.POST['new_password'] == request.POST['new_password_again']:
    		if a.password == a.micryp(request.POST['password']):
    			if form.is_valid():
    				new_password = a.micryp( request.POST['new_password'] )
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
def exito(request):
  return render(request, 'account/exito.html', contexto())

#funcion usada para la pagina de descarga
def descarga(request):
  a = Descarga.objects.all()
  context = contexto()
  context.update({
    'descarga': a
  })
  return render(request, 'account/download.html', context)


#clase usada para renderizar el TOP del juego y paginarlo
class top(ListView):
  model = Top
  template_name = 'account/top100.html'
  #context_object_name = 'player'
  queryset = Top.objects.all().exclude(Q(name__contains='[')).order_by('-level','-ranking')
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
            'form': form
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
        b = Account.objects.get(login='luisito666') #cuenta base para la comparacion de fecha de activacion
      except:
        context.update({'key': 'El token que instentas usar no existe.'})
        return render(request, 'account/activar_cuenta.html', context)
      if a.status == 'OK':
        if a.availdt == b.availdt:
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
    if request.session.has_key('id'):
        try:
            a = Account.objects.get(id=request.session['id'])
        except Account.DoesNotExist:
            pass

        if request.method == 'POST' and form.is_valid():
            b = request.POST['nombre']
            c = Top.objects.filter(account_id=a.id)
            for pexrsonaje in c:
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
            context.update({
                'if_form': True,
                'form': form
            })
            return render(request,'account/unlock.html', context)
    else:
        return redirect('account:login')
