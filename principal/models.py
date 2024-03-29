#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

class punto(models.Model):
	fkusr = models.ForeignKey(User)
	puntousr = models.IntegerField(blank=False, default="0")
	def __unicode__(self):
		return "%s %s" %(self.fkusr, self.puntousr)

class resultado(models.Model):
	desres = models.CharField(blank=False, max_length=50)
	def __unicode__(self):
		return self.desres

class pais(models.Model):
	despais = models.CharField(blank=False, max_length=50)
	def __unicode__(self):
		return self.despais

class equipo(models.Model):
	desequipo = models.CharField(blank=True, max_length=50)
	puntos = models.IntegerField(blank=True, default="0")
	pj =  models.IntegerField(blank=True, default="0")
	pg =  models.IntegerField(blank=True, default="0")
	pe =  models.IntegerField(blank=True, default="0")
	pp =  models.IntegerField(blank=True, default="0")
	gf =  models.IntegerField(blank=True, default="0")
	gc =  models.IntegerField(blank=True, default="0")
	def __unicode__(self):
		return self.desequipo
		
class fecha(models.Model):
	desfecha = models.CharField(blank=True, max_length=50)
	fechausr = models.ManyToManyField(User, through='fechausuario')
	def __unicode__(self):
		return self.desfecha

class juego(models.Model):
	fklocal = models.ForeignKey(equipo, related_name='+')
	fkvisita = models.ForeignKey(equipo, related_name='+')
	fkres = models.ForeignKey(resultado)
	fkfecha = models.ForeignKey(fecha)
	fkpais = models.ForeignKey(pais)
	def __unicode__(self):
		return '%s vs %s' %(self.fklocal, self.fkvisita)

class pronostico(models.Model):
	despro = models.CharField(blank=False, max_length=50)
	pronoticos = models.ManyToManyField(juego, through='juegopronostico')
	def __unicode__(self):
		return self.despro
	
class juegopronostico(models.Model):
	fkusr = models.ForeignKey(User)
	fkjuego = models.ForeignKey(juego)
	fkpro = models.ForeignKey(pronostico)
	fecha = models.DateField(auto_now=True)
	def __unicode__(self):
		return '%s %s %s %s' %(self.fkjuego, self.fkpro, self.fkusr, self.fecha)
		
class fechausuario(models.Model):
	fkfecha = models.ForeignKey(fecha)
	fkusr = models.ForeignKey(User)
	apuesta = models.IntegerField(blank=False, default="0")
	def __unicode__(self):
		return '%s Usuario: %s Apuesta: %s' %(self.fkfecha, self.fkusr, self.apuesta)
