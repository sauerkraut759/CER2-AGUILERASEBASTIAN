from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import MaterialReciclable, UsuarioSistema, SolicitudRetiro

# Register your models here.
class SolicitudRetiroAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'operario', 'estado', 'material', 'fecha_creacion')
    actions = ['marcar_completadas']

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        user = request.user

        if user.is_superuser or user.groups.filter(name='Staff').exists():
            return qs
        if user.groups.filter(name='Operario').exists():
            return qs.filter(operario=user)
        
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == 'operario':
            kwargs['queryset'] = User.objects.filter(groups__name="Operario")

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def marcar_completadas(self, request, queryset):

        for solicitud in queryset:
            solicitud.marcar_completada()

        self.message_user(request, f"{queryset.count()} solicitudes completadas.")
    
    marcar_completadas.short_description = "Marcar como completadas"



admin.site.register(MaterialReciclable)
admin.site.register(UsuarioSistema)
admin.site.register(SolicitudRetiro, SolicitudRetiroAdmin)