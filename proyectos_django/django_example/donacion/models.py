from django.db import models

class Factor(models.Model):  # +    - 
    factor = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=150)
    
    def __str__(self):
        return self.factor
    
class Grupo_sanguineo(models.Model): # A -
    tipo = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=150)
    factor=models.ForeignKey(Factor, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.tipo} {self.factor}"

class Donante(models.Model):  # donante tiene 1 tipo de sangre
    nombre = models.CharField(max_length=150)    #Cuánta es la cantida de sangre que ha donado X donante
    apellido = models.CharField(max_length=150)
    fecha_nacimiento=models.DateField()
    grupo_sanguineo=models.ForeignKey(Grupo_sanguineo, on_delete=models.CASCADE)
    
  
    def __str__(self):
        return self.nombre
 
class Donacion(models.Model):
    donante=models.ForeignKey(Donante, on_delete=models.CASCADE)
    cantidad=models.FloatField()
    fecha_ingreso=models.DateTimeField(auto_now=True)
    observacion=models.CharField(max_length=150, null=True, blank=True)
    
    def __str__(self):
        
        return f"{self.observacion} - {self.fecha_ingreso.strftime('%d-%m-%Y')} - {self.cantidad:.2f} - {self.donante.nombre}"
# Create your models here.


