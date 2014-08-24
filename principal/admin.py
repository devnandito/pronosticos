#encoding:utf-8
from django.contrib import admin
from principal.models import *

class equipoAdmin(admin.ModelAdmin):
	list_display  = ('id','desequipo','puntos')
	search_fields = ['desequipo']
	#list_display_links = ('campo','campo')

class fechaAdmin(admin.ModelAdmin):
	list_display  = ('id','desfecha')
	search_fields = ['desfecha']

class fechausuarioAdmin(admin.ModelAdmin):
	list_display  = ('id','fkfecha','fkusr','apuesta')
	search_fields = ['fkfecha']

class juegoAdmin(admin.ModelAdmin):
	list_display  = ('id','fklocal','fkvisita','fkres','fkfecha','fkpais')
	search_fields = ['fkfecha']
	
class juegopronosticoAdmin(admin.ModelAdmin):
	list_display  = ('id','fkusr','fkjuego','fkpro','fecha')
	search_fields = ['fkfecha']

class paisAdmin(admin.ModelAdmin):
	list_display  = ('id','despais')
	search_fields = ['despais']

class pronosticoAdmin(admin.ModelAdmin):
	list_display  = ('id','despro')
	search_fields = ['despro']

class puntoAdmin(admin.ModelAdmin):
	list_display  = ('id','fkusr','puntousr')
	search_fields = ['puntousr']
	
class resultadoAdmin(admin.ModelAdmin):
	list_display  = ('id','desres')
	search_fields = ['desres']

admin.site.register(equipo, equipoAdmin)
admin.site.register(fecha, fechaAdmin)
admin.site.register(fechausuario, fechausuarioAdmin)
admin.site.register(juego, juegoAdmin)
admin.site.register(juegopronostico, juegopronosticoAdmin)
admin.site.register(pais, paisAdmin)
admin.site.register(pronostico, pronosticoAdmin)
admin.site.register(punto, puntoAdmin)
admin.site.register(resultado, resultadoAdmin)

