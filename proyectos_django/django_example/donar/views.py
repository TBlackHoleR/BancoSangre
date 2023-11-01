from django.shortcuts import render
from base.constant import CREATE_MESSAGE, DELETE_MESSAGE, UPDATE_MESSAGE
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import DonacionForms
from person.models import Person, Donacion

class DonacionListView(ListView):
    """!
    Clase que muestra la lista de personas

    """

    model = Donacion
    template_name = 'donar/listadonaciones.html'

    def get_queryset(self):
        """!
        Función que obtiene la lista de personas que están asociados al usuario     
        @param self <b>{object}</b> Objeto que instancia la clase
        @return queryset <b>{object}</b> lista de personas asociadas al usuario
        """
        # queryset = Donacion.objects.filter(user=self.request.user)
        queryset = Donacion.objects.all()
        return queryset

class DonacionCreateView(SuccessMessageMixin, CreateView):
    """!
    Clase que permite a un usuario registrar personas

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = Donacion
    form_class = DonacionForms
    template_name = 'donar/create.html'
    success_url = reverse_lazy('donar:list')
    success_message = CREATE_MESSAGE

    def form_valid(self, form):
        """!
        Función que valida si el formulario está correcto

        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario
        @return super <b>{object}</b> Formulario validado
        """

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        #self.object.parish = form.cleaned_data['parish']
        self.object.save()
        return super(DonacionCreateView, self).form_valid(form)

class DonacionUpdateView(SuccessMessageMixin, UpdateView):
    """!
    Clase que permite a un usuario actualizar los datos de una persona

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = Donacion
    form_class = DonacionForms
    template_name = 'donar/create.html'
    success_url = reverse_lazy('donar:list')
    success_message = UPDATE_MESSAGE

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
            a esta vista

        @author William Páez (paez.william8 at gmail.com)
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene los datos de la
            petición
        @param *args <b>{tuple}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return super <b>{object}</b> Entra a la vista de actualización de una
            persona, sino redirecciona hacia la vista de error de permisos
        """

        if Donacion.objects.all():
            return super(DonacionUpdateView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return redirect('base:error_403')

    def get_initial(self):
        """!
        Función que agrega valores predeterminados a los campos del formulario

        @author William Páez (paez.william8 at gmail.com)
        @param self <b>{object}</b> Objeto que instancia la clase
        @return initial_data <b>{object}</b> Valores predeterminado de los
            campos del formulario
        """

        initial_data = super(DonacionUpdateView, self).get_initial()
        #initial_data['donante'] = self.object.donante.quantity.date
        return initial_data


class DonacionDeleteView(SuccessMessageMixin, DeleteView):
    """!
    Clase que permite a un usuario eliminar los datos de una persona

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = Donacion
    template_name = 'donar/delete.html'
    success_url = reverse_lazy('donar:list')
    success_message = DELETE_MESSAGE

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
            a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene los datos de la
            petición
        @param *args <b>{tuple}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return super <b>{object}</b> Entra a la vista de actualización de una
            persona, sino redirecciona hacia la vista de error de permisos
        """

        if Donacion.objects.all():
            return super(DonacionDeleteView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return redirect('base:error_403')

    def delete(self, request, *args, **kwargs):
        """!
        Función que retorna el mensaje de confirmación de la eliminación

        @author William Páez (wpaez at cenditel.gob.ve)
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene los datos de la
            petición
        @param *args <b>{tuple}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return super <b>{object}</b> Objeto con el mensaje de confirmación
            de la eliminación
        """

        messages.success(self.request, self.success_message)
        return super(DonacionDeleteView, self).delete(request, *args, **kwargs)

# Create your views here.
