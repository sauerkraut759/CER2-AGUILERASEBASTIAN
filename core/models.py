from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

# Create your models here.

class MaterialReciclable(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)
    veces_reciclado = models.PositiveIntegerField(default=0)

    def incrementar_veces_retirado(self):
        self.veces_reciclado += 1
        self.save()

    def __str__(self):
        return f"{self.codigo} - {self.nombre} - {self.descripcion}"
    
class UsuarioSistema(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


class SolicitudRetiro(models.Model):
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_ruta', 'En ruta'),
        ('completado', 'Completado')
    ]

    UNIDADES = [
        ('kg', 'Kilogramos'),
        ('l', 'Litros'),
        ('u', 'Unidades')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(MaterialReciclable, on_delete=models.PROTECT)
    cantidad = models.FloatField()
    unidad = models.CharField(max_length=15, choices=UNIDADES, default='kg')
    fecha_estimada = models.DateField()

    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    tiempo_en_completar = models.DurationField(null=True, blank=True)

    operario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="Solicitudes_asignadas"
    )

    def marcar_completada(self):
        if self.estado != 'completado':
            self.estado = 'completado'
            self.fecha_completado = timezone.now()
            self.tiempo_en_completar = self.fecha_completado - self.fecha_creacion
            self.save()
            self.material.incrementar_veces_retirado()

    def marcar_enruta(self):
        if self.estado != 'en_ruta':
            self.estado = 'en_ruta'
            self.save()

    def __str__(self):
        op = self.operario.username if self.operario else "sin asignar"
        return f"Solicitud # {self.id} - {self.user.username} - {self.material.codigo} - Operario: {op}"

