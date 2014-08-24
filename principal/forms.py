#encoding:utf-8
from django.forms import ModelForm
from django import forms
from principal.models import *

class JuegoForm(ModelForm):
	class Meta:
		model = juego
		fields = ('id','fkres')

class puntoForm(ModelForm):
	class Meta:
		model = punto
		fields = ('id','fkusr')

#class registroForm(forms.Form):
#	correo = forms.CharField(label='Correo electronico')
#	pwd = forms.CharField(label='Contrasena')
#	usr = forms.CharField(label='username')
class registroForm(ModelForm):
	class Meta:
		model = User
		fields = ('username','email','password')

class userForm(ModelForm):
	class Meta:
		model = User
		fields = ('id','first_name','last_name','email')
