from django.contrib import admin

from .models import Donante,Factor, Grupo_sanguineo, Donacion


class DonanteAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Donante._meta.fields]


admin.site.register(Donante, DonanteAdmin)


    
admin.site.register(Donacion)
admin.site.register(Factor)
admin.site.register(Grupo_sanguineo)
# Register your models here.
