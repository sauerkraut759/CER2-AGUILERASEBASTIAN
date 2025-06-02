from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

from .models import MaterialReciclable, UsuarioSistema, SolicitudRetiro
from .forms import UsuarioSistemaForm, SolicitudRetiroForm

# Create your views here.

def home(request):

    solicitudes_mes = 45
    tiempo_retiro = '12 horas'

    materiales = MaterialReciclable.objects.all()

    mas_reciclados = list(materiales)
    mas_reciclados.sort(key= lambda a: a.veces_reciclado, reverse=True)
    mas_reciclados = [m.nombre for m in mas_reciclados][0:3]

    data = {
        "solicitudes_mes": solicitudes_mes,
        "materiales": materiales,
        "mas_reciclados": mas_reciclados,
        "tiempo_retiro": tiempo_retiro
    }

    return render(request, 'core/index.html', data);

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            messages.success(request, 'Sesion iniciada correctamente')
            return redirect('home')
        else:
            messages.warning(request, "Error al iniciar sesion")
            return redirect('login')

    else:
        return render(request, 'core/login.html');

def logoutUser(request):
    if request.user.is_anonymous:
        return redirect('home')
    
    logout(request)
    messages.success(request, 'Sesion cerrada correctamente')
    return redirect('home')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UsuarioSistemaForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            UsuarioSistema.objects.create(
                user = user,
                telefono = form.cleaned_data['telefono'],
                direccion = form.cleaned_data['direccion']
            )

            grupo = Group.objects.get(name='Ciudadano')
            user.groups.add(grupo)

            login(request, user)

            return redirect('home')

    else:
        form = UsuarioSistemaForm

    return render(request, 'core/register.html', {'form': form})

def registrarSolicitud(request):
    if request.user.is_anonymous:
        messages.warning(request, 'Debe iniciar sesion para ver esta pagina')
        return redirect('login')
    
    if request.method == 'POST':
        form = SolicitudRetiroForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.user = request.user
            solicitud.save()

            messages.success(request, 'Solicitud registrada correctamente')
            return redirect('home')
    else:
        form = SolicitudRetiroForm
    
    return render(request, 'core/registrar_solicitud.html', {'form': form})

def solicitudesUsuario(request):
    if request.user.is_anonymous:
        messages.warning(request, 'Debe iniciar sesion para ver esta pagina')
        return redirect('login')
    
    solicitudes = SolicitudRetiro.objects.filter(user=request.user)
    
    return render(request, 'core/mis_solicitudes.html', {'solicitudes': solicitudes})