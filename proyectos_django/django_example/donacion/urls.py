from django.urls import include, path
from .views import DonacionListView, DonanteView, registrar_donacion, mostrar_donaciones, generar_pdf

urlpatterns = [
    path('insertar', DonanteView.as_view, name='insertar'),
    path('verDonante/', DonacionListView.as_view, name='verDonante'),
    path('registrar_donacion/', registrar_donacion, name='registrar_donacion'),
    path('mostrar_donaciones/<int:id>/', mostrar_donaciones, name='mostrar_donaciones'),
    path('generar_pdf/<int:id>/', generar_pdf, name='generar_pdf'),



]







