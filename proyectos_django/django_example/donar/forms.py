from base.models import Municipality, Parish, State
from django import forms
from django.utils.translation import gettext_lazy as _

from person.models import Donacion, Person

class DonacionForms(forms.ModelForm):
    quantity = forms.CharField(
        label=_('Cantidad:'),
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'data-toggle': 'tooltip',
                'title': _('Ingrese la cantidad a donar'),
            }
        )
    )

    donante = forms.ModelChoiceField(
            label=_('Seleccione donante:'), queryset=Person.objects.all(),
            empty_label=_('Seleccione...'),
            widget=forms.Select(attrs={
                'class': 'form-control form-control-sm select2',
                'data-toggle': 'tooltip',
                'title': _('Seleccione el estado donde se encuentra ubicada'),
                # 'onchange': "combo_update(\
                #     this.value, 'base', 'Municipality', 'state', 'pk', 'name',\
                #     'id_municipality')",
            })
        )

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades


        """

        model = Donacion
        exclude = ['user']