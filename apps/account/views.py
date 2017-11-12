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
from zaunt import settings

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
              'Bienvenido Metin2 Zaunt',
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
        context['player'] = total_pl()
        context['account'] = total_us()
        context['online'] = last_hour()
        context['actualmente'] = last_min()
        context['top_player'] = player_top()
        context['guild_top'] = guild_top()
        return context

#funcion usada para el login
""" es necesario agregar re factorin a esta funcion """
def login(request):
  form = CustomLoginForm(request.POST or None)
  if request.session.has_key('id'):
    a = Account.objects.get(id=request.session['id'])
    b = Top.objects.filter(account_id=a.id)
    context = { 
          'session': a ,                            
          'personajes': b,
          'player': total_pl(),
          'account': total_us(),
          'online': last_hour(), 
          'actualmente': last_min(),
          'guild_top': guild_top(),
          'top_player': player_top(),
    }
    return render(request, 'account/logon.html', context)
  else: 
    if request.method == 'POST':  #Validando que los datos vengan por post
      if form.is_valid():       
        try:
          a = Account.objects.get(login=request.POST['login'])  #obteniendo datos de usuario
        except Account.DoesNotExist:          
          context = {
                'key':'El nombre de usuario no existe',
                'form': form,
                'player': total_pl(), 
                'account': total_us(), 
                'online': last_hour(), 
                'actualmente': last_min(),
                'guild_top': guild_top(),
                'top_player': player_top(),
          }
          return render(request, 'account/login.html', context)
      else:        
        context = {
                'key':'Por favor no deje campos en blanco',
                'form': form,
                'player': total_pl(), 
                'account': total_us(), 
                'online': last_hour(), 
                'actualmente': last_min(),
                'guild_top': guild_top(),
                'top_player': player_top(),
        }
        return render(request, 'account/login.html', context )
      b = a.micryp(request.POST['password']) #uso implicito de cursor para encriptar password   
      if a.password == b:
        request.session['id'] = a.id   
      if request.session.has_key('id'):
        b = Top.objects.filter(account_id=a.id)
        context = {
              'session': a , 
              'personajes': b,
              'player': total_pl(), 
              'account': total_us(), 
              'online': last_hour(), 
              'actualmente': last_min(),
              'guild_top': guild_top(),
              'top_player': player_top(),
        }
        return render(request, 'account/logon.html', context )
      else:        
        context = {
              'key':'Nombre de usuario o password incorrecto',
              'form': form,              
              'player': total_pl(), 
              'account': total_us(), 
              'online': last_hour(), 
              'actualmente': last_min(),
              'guild_top': guild_top(),
              'top_player': player_top(),
        }
        return render(request, 'account/login.html',  context, )      
    else:      
      context = {
              'key': '',
              'form': form,              
              'player': total_pl(), 
              'account': total_us(), 
              'online': last_hour(), 
              'actualmente': last_min(),
              'guild_top': guild_top(),
              'top_player': player_top(),
      }      
      return render(request,'account/login.html', context)

#funcion usada para cerra session
def logout(request):
  try:
    a = Account.objects.get(id=request.session['id'])
    del request.session['id']
  except:
  	pass
  b = Top.objects.filter(account_id=a.id)  
  context = {
              'datos': a,
              'personajes': b,
              'player': total_pl(), 
              'account': total_us(), 
              'online': last_hour(), 
              'actualmente': last_min(),
  }
  return render(request, 'account/salir.html', {'datos': context } )

#funcion usada para cambiar password estando logeado
def changepasswd(request):
  form = CustomChangePassword(request.POST or None)
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
    				context = { 
                  'key':'se ha cambiado el password exitosamente.', 
                  'form': form,
                  'player': total_pl(), 
                  'account': total_us(), 
                  'online': last_hour(), 
                  'actualmente': last_min(),
                  'top_player': player_top(),
                  'guild_top': guild_top()
            }
    				return render(request, 'account/password.html', context )
    		else:
    			context = { 
                'key':'El password no es correcto', 
                'form': form,
                'player': total_pl(), 
                'account': total_us(), 
                'online': last_hour(), 
                'actualmente': last_min(),
                'top_player': player_top(),
                'guild_top': guild_top()
          }
    			return render(request, 'account/password.html', context )
    	else:
    		#'contraseas no coinciden'
    		context = { 
              'key':'Los password no coinciden' ,
              'form': form,
              'player': total_pl(), 
              'account': total_us(), 
              'online': last_hour(), 
              'actualmente': last_min(),
              'top_player': player_top(),
              'guild_top': guild_top()
        }        
    		return render(request, 'account/password.html', context )
    else:
    	context = {
            'form': form,
            'player': total_pl(), 
            'account': total_us(), 
            'online': last_hour(), 
            'actualmente': last_min(),
            'top_player': player_top(),
            'guild_top': guild_top()
      }
    	return render(request, 'account/password.html' , context )

  else:
  	return redirect('account:login')

#Funcion usada para confirmar el registro exitoso
def exito(request):
  context = {
            'player': total_pl(), 
            'account': total_us(), 
            'online': last_hour(), 
            'actualmente': last_min(),
            'top_player': player_top(),
            'guild_top': guild_top()
  }
  return render(request, 'account/exito.html', context)

#funcion usada para la pagina de descarga
def descarga(request):
  a = Descarga.objects.all()
  context = { 
              'descarga': a,              
              'player': total_pl(), 
              'account': total_us(), 
              'online': last_hour(), 
              'actualmente': last_min(),
              'top_player': player_top(),
              'guild_top': guild_top()
  }
  return render(request, 'account/download.html', context)

"""def top100(request):
  a = Player.objects.all().exclude(Q(name__contains='[')).order_by('-level','-exp')#[:10]
  context = { 'player': a}
  return render(request,'account/top100.html', context)
"""
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
        context['player'] = total_pl()
        context['account'] = total_us()
        context['online'] = last_hour()
        context['actualmente'] = last_min()
        context['top_player'] = player_top()
        context['guild_top'] = guild_top()
        return context

#clase usada para renderizar el top del juego y paginarlo
class top_g(ListView):
  model = Guild
  template_name = 'account/top_g.html'
  queryset = Guild.objects.all().order_by('-level','-exp','-win', '-ladder_point')
  paginate_by = 20

  def get_context_data(self, **kwargs):
        context = super(top_g, self).get_context_data(**kwargs)
        context['player'] = total_pl()
        context['account'] = total_us()
        context['online'] = last_hour()
        context['actualmente'] = last_min()
        context['top_player'] = player_top()
        context['guild_top'] = guild_top()
        return context

#Funcion usada para recuperar password por correo
"""Realizar refactorin a esta funcion """
def recuperar_password(request):
    form = ResPassword(request.POST or None)
    #validando los datos que se envian por post
    if request.method == 'POST' and form.is_valid():      
      a = request.POST['login']
      b = request.POST['email']
      try:
        usuario = Account.objects.get(login=a)
      except Account.DoesNotExist:
        context = {
              'key': 'No se encuentran registros en nuestra base de datos',
              'form': form ,
              'player': total_pl(), 
              'account': total_us(), 
              'online': last_hour(), 
              'actualmente': last_min(),
              'top_player': player_top(),
              'guild_top': guild_top()
        }
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
  
            context = {
                    'key': 'se ha enviado un correo electronico con las instrucciones para recupear el password',
                    'form': form,
                    'player': total_pl(), 
                    'account': total_us(), 
                    'online': last_hour(), 
                    'actualmente': last_min(),
                    'top_player': player_top(),
                    'guild_top': guild_top()
            }
            return render(request, 'account/rescue.html', context)
        except:
            context = {
                  'key': 'Error enviando el correo',
                  'form': form,
                  'player': total_pl(), 
                  'account': total_us(), 
                  'online': last_hour(), 
                  'actualmente': last_min(),
                  'top_player': player_top(),
                  'guild_top': guild_top()
            }
            return render(request, 'account/rescue.html', context)
      else:
        context = {
              'key': 'El usuario no concuerda con el correo electronico',
              'form': form,
              'player': total_pl(), 
              'account': total_us(), 
              'online': last_hour(), 
              'actualmente': last_min(),
              'top_player': player_top(),
              'guild_top': guild_top()
        }
        return render(request, 'account/rescue.html', context)
    else:
      context = {
            'key': '', 
            'form': form,
            'player': total_pl(), 
            'account': total_us(), 
            'online': last_hour(), 
            'actualmente': last_min(),
            'top_player': player_top(),
            'guild_top': guild_top()
      }
      return render(request, 'account/rescue.html', context)

#Procesando el correo de recuperacion de password.
def process_password(request,url):
  form = FormResetPassword(request.POST or None)
  if request.method == 'GET':
    if url:
      try:
        a = Account.objects.get(address=url)
      except:
        context = {
          'key': 'El token que intentas usar no existe',
          'if_form': False,
          'player': total_pl(), 
          'account': total_us(), 
          'online': last_hour(), 
          'actualmente': last_min(),
          'top_player': player_top(),
          'guild_top': guild_top()
        }
        return render(request, 'account/cambio_passwd.html', context)
      z = (timezone.now() - a.token_expire).days
      if z >= 1:
        context = {
          'key': 'El token que intentas usar esta vencido',
          'if_form': False,
          'player': total_pl(), 
          'account': total_us(), 
          'online': last_hour(), 
          'actualmente': last_min(),
          'top_player': player_top(),
          'guild_top': guild_top()
        }
        return render(request, 'account/cambio_passwd.html' , context)        
      else:
        request.session['tmp_id'] = a.id
        context = {
          'key': 'ingresa tu nuevo password',
          'form': form,
          'if_form': True,
          'player': total_pl(), 
          'account': total_us(), 
          'online': last_hour(), 
          'actualmente': last_min(),
          'top_player': player_top(),
          'guild_top': guild_top()
        }
        return render(request, 'account/cambio_passwd.html' , context)        
    else:
      context = {
        'key': 'No has enviado ningun token',
        'if_form': False,
        'player': total_pl(), 
        'account': total_us(), 
        'online': last_hour(), 
        'actualmente': last_min(),
        'top_player': player_top(),
        'guild_top': guild_top()
      }
      return render(request, 'account/cambio_passwd.html', context)
  if request.method == 'POST':
    password = request.POST['password']
    password_again = request.POST['password_again']
    if password == password_again and form.is_valid():
      if request.session.has_key('tmp_id'):
        try:
          a = Account.objects.get(id=request.session['tmp_id'])
        except:
          context = {
                'key': 'No se encuentra el usuario',
                'if_form': False,
                'player': total_pl(), 
                'account': total_us(), 
                'online': last_hour(), 
                'actualmente': last_min(),
          }
          return render(request, 'account/cambio_passwd.html', context)
        a.password = a.micryp(password)
        a.address = aleatorio(40)
        a.save()
        del request.session['tmp_id']
        context = {
              'key': 'Password actualizado correctamente',
              'if_form': False,
              'player': total_pl(), 
              'account': total_us(), 
              'online': last_hour(), 
              'actualmente': last_min(),
        }
        return render(request, 'account/cambio_passwd.html', context)
      else:
        context = {
              'key': 'No existe la session temporal',
              'if_form': False,
              'player': total_pl(), 
              'account': total_us(), 
              'online': last_hour(), 
              'actualmente': last_min(),
        }
        return render(request, 'account/cambio_passwd.html', context )
    else:
      context = {
        'if_form': True,
        'key':'Los password no coinciden',
        'form': form,
        'player': total_pl(), 
        'account': total_us(), 
        'online': last_hour(), 
        'actualmente': last_min(),
      }
      return render(request, 'account/cambio_passwd.html', context)

#Aqui validamos los link's de activacion de la cuenta.
def process_reg(request, url):
  if request.method == 'GET':
    if url:
      try:
        a = Account.objects.get(address=url)
        b = Account.objects.get(login='luisito666') #cuenta base para la comparacion de fecha de activacion
      except:
        context = {
              'key': 'El token que instentas usar no existe.',
              'player': total_pl(), 
              'account': total_us(), 
              'online': last_hour(), 
              'actualmente': last_min(),
        }
        return render(request, 'account/activar_cuenta.html', context)
      if a.status == 'OK':
        if a.availdt == b.availdt:
          a.address = aleatorio(40)
          a.save()
          context = {
              'key': 'Tu cuenta ya esta activada',
              'player': total_pl(), 
              'account': total_us(), 
              'online': last_hour(), 
              'actualmente': last_min(),
          }
          return render(request, 'account/activar_cuenta.html', context )
        else:
          a.availdt = "2009-01-01T00:00:00"
          a.address = aleatorio(40)
          a.save()

          context = {
              'key': 'Tu cuenta se ha activado correctamente',
              'player': total_pl(), 
              'account': total_us(), 
              'online': last_hour(), 
              'actualmente': last_min(),
          }
          return render(request, 'account/activar_cuenta.html', context )
      else:
        context = {
              'key': 'Tu cuenta esta baneada',
              'player': total_pl(), 
              'account': total_us(), 
              'online': last_hour(), 
              'actualmente': last_min(),
        }
        return render(request, 'account/activar_cuenta.html', context )
    else:
      context = {
            'key': 'No has enviado ningun token',
            'player': total_pl(), 
            'account': total_us(), 
            'online': last_hour(), 
            'actualmente': last_min(),
      }
      return render(request, 'account/activar_cuenta.html', context)
  else:
    context = {
          'key': 'Metodo no admitido',
          'player': total_pl(), 
          'account': total_us(), 
          'online': last_hour(), 
          'actualmente': last_min(),
    }
    return render(request, 'account/activar_cuenta.html', context)     

def desbuguear(request):
	form = CustomDesbugForm(request.POST or None)
	if request.session.has_key('id'):
		try:
			a = Account.objects.get(id=request.session['id'])
		except Account.DoesNotExist:
			pass

		if request.method == 'POST' and form.is_valid():
			b = request.POST['nombre']
			c = Top.objects.filter(account_id=a.id)
			for personaje in c:
				if str.lower(personaje.name) == str.lower(b):
					resultado = cambio_mapa(a.id, personaje.name)
					if resultado:
						context = {
							'key':'Se ha desbugeado tu personaje correctamente debes esperar 30 min para iniciar con el.',
							'if_form': True,
							'form': form,
							'player': total_pl(), 
							'account': total_us(), 
							'online': last_hour(), 
							'actualmente': last_min(),
						}
						return render(request,'account/unlock.html', context)
					else:
						context = {
							'key':'Error desbugueando.',
							'if_form': True,
							'form': form,
							'player': total_pl(), 
							'account': total_us(), 
							'online': last_hour(), 
							'actualmente': last_min(),
						}
						return render(request,'account/unlock.html', context)
			
			context = {
							'key':'Ningun personaje coincide.',
							'if_form': True,
							'form': form,
							'player': total_pl(), 
							'account': total_us(), 
							'online': last_hour(), 
							'actualmente': last_min(),
					}
			return render(request ,'account/unlock.html', context)

		if request.method == 'GET':
			context = {							
							'if_form': True,
							'form': form,
							'player': total_pl(), 
							'account': total_us(), 
							'online': last_hour(), 
							'actualmente': last_min(),
			}
			return render(request,'account/unlock.html', context)
	else:
		return redirect('account:login')