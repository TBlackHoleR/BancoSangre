from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import Donante, Donacion
from Donacion.models import Donante,  Grupo_sanguineo, Factor, Donacion
import datetime as dt
from datetime import datetime, timedelta
from django.db.models import F
from .forms import DonanteForm, DonacionForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO





class Index(LoginRequiredMixin, View):
    template = 'index.html'
    login_url = '/login/'

    def get(self, request):
        return render(request, self.template)
# Create your views here.

class Login(View):
    template = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template, {'form': form})


    def post(self, request):
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template, {'form': form})
        
class Tablas(View):
    template = 'tablas.html'

    def get(self, request):
        return render(request, self.template)
    
class Reporte(View):
    template = 'reportes.html'

    def get(self, request):
        return render(request, self.template)
    
class Configuracion(View):
    template = 'configuraciones.html'

    def get(self, request):
        return render(request, self.template)

class DonacionListView(ListView):
    """!
    Clase que muestra la lista de Donacion

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = Donacion
    template_name = 'verDonantes.html'

    def get_queryset(self):
        """!
        Función que obtiene la lista de personas que están asociados al usuario

        @author William Páez (paez.william8 at gmail.com)
        @param self <b>{object}</b> Objeto que instancia la clase
        @return queryset <b>{object}</b> lista de personas asociadas al usuario
        """

        queryset = Donacion.objects.all()
        return queryset



class DonanteView(View):
    template='donante.html' 
    def get(self, request):
        # Calcula la fecha mínima para tener 18 años
        fecha_limite = datetime.now() - timedelta(days=18 * 365) 
             
        buscador=request.GET.get('nombreBusqueda','')
        fecha_inicio=request.GET.get('fecha_inicio')
        fecha_fin=request.GET.get('fecha_fin')
        
        busqueda_fecha=Donante.objects.filter(fecha_nacimiento__range=(fecha_inicio, fecha_fin))        
        busqueda=Donante.objects.filter(nombre__icontains=buscador)
        personas_mayores = Donante.objects.annotate(edad=F('fecha_nacimiento')).filter(edad__lte=fecha_limite)
        grupo_sanguineo = Grupo_sanguineo.objects.all()
        
        return render(request, self.template, {'busqueda': busqueda, 'busqueda_fecha': busqueda_fecha, 'personas_mayores': personas_mayores, 'mostrar_resultado':True, 'grupo_sanguineo': grupo_sanguineo})
        return render(request, 'donante.html', {'mostrar_resultado': False})
    

    def post(self, request):
       
        fecha_actual= dt.datetime.now().date() #obtenemos la fecha de hoy
       
        if request.method=='POST' :
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            fecha_nacimiento = request.POST['fechanac']
            grupo = request.POST['mi_select']  
            
            grupo_sanguineo = Grupo_sanguineo.objects.get(id=grupo)#CONVERIT A UNA VARIABLE VÁLIDA PARA LA CLASE GRUPO_SANGUINEO
                      
            fecha_convertida=dt.datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            
            
            if fecha_convertida < fecha_actual:
                nuevo_registro = Donante(nombre=nombre, apellido=apellido, fecha_nacimiento=fecha_nacimiento, grupo_sanguineo=grupo_sanguineo)
                
                nuevo_registro.save()
            #Mensaje de confirmación        
                messages.success(request, 'Ingresado correctamente')
            else:
                messages.error(request, 'Fecha inválida')
             
        
        return redirect('/donante')


def eliminar(request, id):
    
    donante=Donante.objects.get(id=id)
    donante.delete()
        
    return redirect('/donante')   #Agregar la libreria redirect    

def edicionDonante(request, id):
    template='edicion.html'
    donante=Donante.objects.get(id=id)
    return render(request, template, {'donante':donante})

def editarDonante(request):
    
    codigo=request.POST['id']
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    fecha_nacimiento = request.POST['fechanac']
    
    donante=Donante.objects.get(id=codigo)
    donante.nombre = nombre
    donante.apellido =apellido
    donante.fecha_nacimiento =fecha_nacimiento
   
    donante.save()
    
    return redirect('/donante')



def mostrar_donante(request, id):
    template='registrar_donacion.html'
    donante=Donante.objects.get(id=id)
    return render(request, template, {'donante':donante})

def registrar_donacion(request):
    
    if request.method == 'POST':    
        codigo=request.POST['id']
        cant=request.POST['cantidad']
        obs=request.POST['observacion']
        id_donante = Donante.objects.get(id=codigo)
        
        nuevo_registro = Donacion(donante=id_donante, cantidad=cant, observacion=obs)
              
        nuevo_registro.save()
        messages.success(request, 'Ingresado correctamente')
    else:
        messages.error(request, 'Error al ingresar')
        
    #return render(request, 'registrar_donacion.html')  
    return redirect('/donante')




def mostrar_donaciones(request, id):
    donante = get_object_or_404(Donante, id=id)
    donaciones = Donacion.objects.filter(donante=donante)
    
    context = {
        'donante': donante,
        'donaciones': donaciones,
        'id': id,  # Asegúrate de pasar el valor de id al contexto
    }

    return render(request, 'mostrar_donaciones.html', {'donante': donante, 'donaciones': donaciones})



def generar_pdf(request, id):
    donante = get_object_or_404(Donante, id=id)
    donaciones = Donacion.objects.filter(donante=donante)
    
    context = {
        'donante': donante,
        'donaciones': donaciones,
    }
    
    template = get_template('mostrar_donaciones.html')
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="historial_donaciones_{donante.nombre}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
    
    return response
