from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404
from datetime import datetime
from principal.forms import *
from django.template.context import RequestContext
from principal.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core import serializers
from django.db.models import F, Count
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from collections import defaultdict

#Vista login
def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/dashboard')
	if request.method == 'POST':
		form = AuthenticationForm(request.POST)
		if form.is_valid:
			usuario = request.POST['username']
			pwd = request.POST['password']
			acceso = authenticate(username=usuario, password=pwd)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/dashboard')
				else:
					return render_to_response('noactivo.html', context_instance=RequestContext(request,{'form':form}))
			else:
				return render_to_response('nousuario.html', context_instance=RequestContext(request,{'form':form}))
	else:
		form = AuthenticationForm()
	return render_to_response('login.html',{'form':form}, context_instance=RequestContext(request))
	
#Vista cerra session
@login_required(login_url='/')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')

#Vista pronosticos
@login_required(login_url='/')
def viewpronostico(request):
	usuario = request.user
	pronosticos = juegopronostico.objects.all().filter(fkusr=usuario).order_by('-fkjuego')[:6]
	return render_to_response('viewpronostico.html', context_instance=RequestContext(request,{'pronosticos':pronosticos,'usuario':usuario}))

#Vista save pronosticos
@login_required(login_url='/')
def savepronostico(request):
	usuario = request.user
	pro = request.POST.getlist('pro[]')
	juego = request.POST.getlist('juego[]')
	i=0
	a = []
	for item in juego:
		if pro[i] == '4':
			#msg = "Debe ingresar su pronostico"
			return HttpResponseRedirect('/errorpronostico')
			#return render_to_response('errorpronostico.html', context_instance=RequestContext(request,{'msg':msg}))
		else:
			a = juegopronostico(fkusr=usuario, fkjuego_id=item, fkpro_id=pro[i])
			a.save()
			i+=1
	p1 = punto.objects.get(fkusr__username__exact=usuario)
	p2 = 2
	u1 = User.objects.get(username=usuario)
	u2 = u1.id
	f1 = fecha.objects.latest('id').id
	fu1 = fechausuario(fkfecha_id=f1, fkusr_id=u2, apuesta=p2)
	fu1.save()
	p1.puntousr = F('puntousr') - p2
	p1.save()
	return HttpResponseRedirect('/dashboard')

#Vista errorpronostico
@login_required(login_url='/')
def errorpronostico(request):
	msg = "Debe ingresar un resultado"
	return render_to_response('errorpronostico.html', context_instance=RequestContext(request,{'msg':msg}))

#Vista form pronosticos
@login_required(login_url='/')
def formpronostico(request):
	usuario = request.user
	juegos = juego.objects.all().order_by('-id')[:6]
	res = resultado.objects.all().order_by('id')
	#fechas = fecha.objects.all().order_by('-id')[0]
	fechas = fecha.objects.latest('id').id
	n = juegopronostico.objects.filter(fkjuego__fkfecha__id__exact=fechas,fkusr__username__exact=usuario).exists()
	#fu = fechausuario.objects.filter(fkfecha__id__exact=fechas,fkusr__username__exact=usuario).exits()
	tmptime = datetime.now()
	now = tmptime.strftime("%A")
	if n == True:
		msg = 'si'
	else:
		msg = 'no'
	p1 = punto.objects.get(fkusr__username=usuario)
	p2 = p1.puntousr
	return render_to_response('formpronosticos.html', context_instance=RequestContext(request,{'juegos':juegos, 'usuario':usuario,'res':res,'msg':msg,'p2':p2,'now':now}))


#Vista index paginado
@login_required(login_url='/')
def dashboard(request):
	usuario = "%s" %request.user
	fechalast = fecha.objects.latest('id').id
	fu2 = fechausuario.objects.all()
	a2 = 0
	for it in fu2:
		if it.fkfecha_id == fechalast:
			a2+=it.apuesta
	a3 = a2*2000
	a4 = (a3*30)/100
	a2 = a3-a4
	juegos_list = juego.objects.all().order_by('-fkfecha','-id')
	paginator = Paginator(juegos_list,6)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		juegos = paginator.page(page)
	except (EmptyPage, InvalidPage):
		juegos = paginator.page(paginator.num_pages)
	return render_to_response('viewjuegos.html', context_instance=RequestContext(request,{'juegos':juegos,'usuario':usuario,'a2':a2}))

#Vista form detalles de juegos
@login_required(login_url='/')
def detjuego(request, id_juego):
	if request.method == 'POST':
		a = get_object_or_404(juego, pk=id_juego)
		form = JuegoForm(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/pronostico')
	else:
		b = juego.objects.get(pk=id_juego)
		form = JuegoForm(instance=b)
		juegos = juego.objects.get(pk=id_juego)
	return render_to_response('formjuegos.html', context_instance=RequestContext(request,{'form':form, 'juegos':juegos}))

#Vista condiciones
def condiciones(request):	
    return render_to_response('condiciones.html', context_instance=RequestContext(request))

#Vista juegos
@login_required(login_url='/')
def viewjuegos(request):	
    juegos = juego.objects.all().order_by('id')
    return render_to_response('viewjuegos.html', context_instance=RequestContext(request,{'juegos':juegos}))

#Vista index
def index(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		#formulario = registroForm(request.POST)
		usr = request.POST['username']
		mail = request.POST['mail']
		if form.is_valid():
			form.save()
			u1 = User.objects.get(username=usr)
			u2 = u1.id
			formpunto = punto(fkusr_id=u2)
			formpunto.save()
			u1.email = mail
			u1.save()
			return HttpResponseRedirect('/')
	else:
		form = UserCreationForm()
		#formulario = registroForm()
	return render_to_response('formregistro.html',{'form':form}, context_instance=RequestContext(request))

#Vista test jquery
@login_required(login_url='/')
def searchs(request):
	error = False
	#if 'search_text' in request.GET:
	if request.method == 'GET':
		q = request.GET['search_text']
		if not q:
			error = True
		else:
			team = equipo.objects.filter(desequipo__contains=q)
			return render_to_response('search.html',{'team':team}, context_instance=RequestContext(request))

#Vista para modificar usuario
@login_required(login_url='/')
def edituser(request, user_name):
	usuario = request.user
	if request.method == 'POST':
		pwd = request.POST['pass']
		if pwd != '':
			u = User.objects.get(username__exact=user_name)
			u.set_password(pwd)
			u.save()
			b = get_object_or_404(User, username=user_name)
			form = userForm(request.POST, instance=b)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/dashboard')
		else:
			b = get_object_or_404(User, username=user_name)
			form = userForm(request.POST, instance=b)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/dashboard')
	a = get_object_or_404(User, username=user_name)
	form = userForm(instance=a)
	return render_to_response('usuario.html',{'form':form,'usuario':usuario}, context_instance=RequestContext(request))
	
#Vista resultado de los pronosticos
@login_required(login_url='/login')
def restotal(request):
	usuario = request.user
	juegor = juego.objects.all()
	juegopro = juegopronostico.objects.all()
	fechalast = fecha.objects.latest('id').id
	fu2 = fechausuario.objects.all()
	a1 = []
	a2 = 0
	for it in fu2:
		if it.fkfecha_id == fechalast:
			a2+=it.apuesta
	a3 = a2*2000
	a4 = (a3*30)/100
	a2 = a3-a4
	for itemp in juegopro:
		for itemj in juegor:
			if itemj.id == itemp.fkjuego_id:
				if itemj.fkres_id == itemp.fkpro_id and itemj.fkfecha_id == fechalast:
					tmp = {'userid':itemp.fkusr_id,'user':itemp.fkusr,'local':itemj.fklocal,'visita':itemj.fkvisita,'pro':itemp.fkpro}
					a1.append(tmp)
	return render_to_response('resultado.html',{'a1':a1,'usuario':usuario,'a2':a2}, context_instance=RequestContext(request))

#def edituser(request, user_name):
#	if request.method == 'POST':
#		b = get_object_or_404(User, username=user_name)
#		form = userForm(request.POST, instance=b)
#		if form.is_valid():
#			form.save()
#			return HttpResponseRedirect('/dashboard')
#	a = get_object_or_404(User, username=user_name)
#	form = userForm(instance=a)
#	return render_to_response('usuario.html',{'form':form}, context_instance=RequestContext(request))

#counts = defaultdict(int)
#@login_required(login_url='/login')
#def edituser(request, user_name):
#	msg = User.objects.filter(username=user_name)
#	a = get_object_or_404(User, username=user_name)
#	msg = userForm(instance=a)
#	msg = "%s" %user_name
#		formulario = UserCreationForm(request.POST)
#		if formulario.is_valid:
#			formulario.save()
#			return HttpResponseRedirect('/')
#	else:
#		formulario = UserCreationForm()
#	return render_to_response('usuario.html',{'msg':msg}, context_instance=RequestContext(request))

#def searchs(request):
#	msg = {}
#	msg.update(csrf(request))
#	if request.method == 'POST':
#		search_text = request.POST['search_text']
#	else:
#		search_text = ''
#	team = equipo.objects.filter(desequipo__contains=search_text)
#	return render_to_response('search.html',{'team':team,'msg':msg}, context_instance=RequestContext(request))

#Vista para hacer combo anidado
#def obtener_libro(request):
#	error = False
#	if 'autor' in request.GET:
#		q = int(request.GET['autor'])
#		if not q:
#			error = True
#		else:
#			books = Libro.objects.filter(autor=q)
#			return render_to_response('filtro.html', context_instance=RequestContext(request,{'books':books}))	
#html = "<html><body><script>alert('Debe realizar su pronostico')</script></body></html>"
#return HttpResponse(html)
#@login_required(login_url='/')
#def savepronostico(request):
#	usuario = request.user
#	pro = request.POST.getlist('pro[]')
#	juego = request.POST.getlist('juego[]')
#	i=0
#	a = []
#	for item in juego:
#		tmp = " Nro. Juego: " + item + " Resultado: " + pro[i] + " Usuario: %s " %usuario
#		a.append(tmp)
#		i+=1
#	return render_to_response('savepronostico.html', context_instance=RequestContext(request,{'a':a}))

#Vista form pronosticos
#@login_required(login_url='/')
#def viewpronostico(request):
#	usuario = request.user
#	pronosticos = juegopronostico.objects.all().filter(fkusr=usuario).order_by('-fkjuego')
#	return render_to_response('viewpronostico.html', context_instance=RequestContext(request,{'pronosticos':pronosticos}))
