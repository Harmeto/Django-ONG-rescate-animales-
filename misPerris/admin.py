from django.contrib import admin
from .models import Animal, Contact, CustomUser, Solicitud

class Animales(admin.ModelAdmin):
    list_display = ['nombre', 'raza', 'tamano', 'peso', 'estado']

    def tamano(self, obj):
        return obj.size 
    
    tamano.short_description = 'Tamaño'

admin.site.register(Animal, Animales)

class Users(admin.ModelAdmin):
    list_display = ['nombre_completo', 'email', 'region', 'ciudad']

    def nombre_completo(self, obj): 
        return obj.first_name + " " + obj.last_name

    def ciudad(self, obj):
        return obj.city

    nombre_completo.short_description = 'Nombre Completo'
    
admin.site.register(CustomUser, Users)

class Contacto(admin.ModelAdmin):
    list_display = ['nombre', 'rut', 'email', 'telefono', 'region', 'ciudad']

    def nombre(self, obj):
        return obj.name
    
    def telefono(self, obj):
        return obj.phone
    
    def ciudad(self, obj):
        return obj.city
    
   

admin.site.register(Contact, Contacto)

class Solicitudes(admin.ModelAdmin):
    list_display=['usuario', 'animal', 'estado']
    list_filter=['estado']
    actions=['aprobar_solicitud', 'rechazar_solicitud', 'borrar_solicitud']

    def aprobar_solicitud(self, request, queryset):
        queryset.update(estado='Aprobada')
        for solicitud in queryset:
            solicitud.animal.estado = 'adoptado'  # <- Modificar a 'adoptado'
            solicitud.animal.save()

    def rechazar_solicitud(self, request, queryset):
        queryset.update(estado='Rechazada')
        for solicitud in queryset:
            solicitud.animal.estado = 'disponible'  # <- Modificar a 'adoptado'
            solicitud.animal.save()
    
    def borrar_solicitud(self, request, queryset):
        queryset.delete()

admin.site.register(Solicitud, Solicitudes)