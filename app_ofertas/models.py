
from django.db import models
from django.contrib.auth.models import User 
# Create your models here.


class Usuario(User):
	TIPO_USUARIOS = (('ad','ADMINISTRADOR'),('of','OFERENTE'))

	tipo_usuario = models.CharField(max_length = 5, null=False, choices = TIPO_USUARIOS) 
	imagen       = models.ImageField(upload_to='fotos_usuarios', null=True,blank=True)

	def get_locales(self):
		return self.locales.all()


class Localidad(models.Model):
	nombre = models.CharField(max_length = 30)

	def get_locales(self):
	 	return self.locales.all()


class Local(models.Model):
	HORARIOS = ('sh','Abierto según horario'),('24hs','Abierto las 24hs')

	nombre     = models.CharField(max_length = 30)
	direccion  = models.CharField(max_length = 50)
	horario    = models.CharField(max_length = 7, choices = HORARIOS)
	usuario    = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'locales')
	localidad  = models.ForeignKey(Localidad, on_delete = models.CASCADE, related_name = 'locales', null=True)

	def get_horarios(self):
		return self.horas.all()

	def get_sucursales(self):
		return self.sucursales.all()

	def get_publicaciones(self):
		return self.publicaciones.all()

	def __str__(self):
		return 'Nombre: {}'.format(self.nombre)


class Sucursal(models.Model):
	direccion = models.CharField(max_length = 50)
	local     = models.ForeignKey(Local, on_delete = models.CASCADE, related_name='sucursales') 
	localidad = models.ForeignKey(Localidad, on_delete = models.CASCADE, related_name='sucursales')



class Horario(models.Model):
	local   = models.ForeignKey(Local, on_delete = models.CASCADE, related_name='horas')
	dia     = models.CharField(max_length = 11)
	hora_d1 = models.CharField(max_length = 5)
	hora_h1 = models.CharField(max_length = 5)
	hora_d2 = models.CharField(max_length = 5, null=True, blank = True)
	hora_h2 = models.CharField(max_length = 5, null=True, blank = True)


class Rubro(models.Model):
	nombre = models.CharField(max_length = 25)


class Publicacion(models.Model):
	local          = models.ForeignKey(Local, on_delete = models.CASCADE, related_name = 'publicaciones')
	rubro   	   = models.ForeignKey(Rubro, on_delete = models.CASCADE, related_name = 'publicaciones')
	titulo         = models.CharField(max_length = 30, null=False)
	detalle        = models.CharField(max_length = 30)
	imagen         = models.ImageField(upload_to='fotos_publicaciones', null=True,blank=True)
	precio_regular = models.DecimalField(max_digits=10, decimal_places=2)
	precio_oferta  = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False)
	fecha_publi    = models.DateTimeField(auto_now_add=True)
	activada 	   = models.BooleanField(default=False)
	tiempo_publi   = models.IntegerField(default=1440)
	cant_visitas   = models.IntegerField(default=0)


class Favorito(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE, related_name = 'favoritos')	
	local   = models.ForeignKey(Local, on_delete = models.CASCADE, related_name = 'favoritos')


class Interes(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE, related_name = 'intereses')
	rubro   = models.ForeignKey(Rubro, on_delete = models.CASCADE, related_name = 'intereses')