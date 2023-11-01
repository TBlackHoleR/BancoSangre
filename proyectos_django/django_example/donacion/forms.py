from django import forms
from .models import Donante, Donacion

class DonanteForm(forms.Form):
    class Meta:
        model=Donante
        fields=['nombre', 'apellido','fecha_nacimiento']
        #fields='__all__'
        
class DonacionForm(forms.Form):
    cantidad = forms.FloatField()
    observacion = forms.CharField(max_length=150, required=False)

class DonacionForm(forms.ModelForm):
    class Meta:
        model = Donacion
        fields = ('cantidad',)  # O puedes especificar los campos que deseas mostrar en el formulario

    def save(self, commit=True):
        donacion = super().save(commit=False)
        # Realiza cualquier procesamiento adicional que desees aquí
        if commit:
            donacion.save()
        return donacion

        
        
        