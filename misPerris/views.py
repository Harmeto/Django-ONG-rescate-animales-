from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

#manipulacion de archivos
import os

#expresiones regulares
import re

#login - logout - admin
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

#models - forms
from .models import Region, Ciudad, Contact, Animal, CustomUser
from .forms import ContactForm, AnimalForm, CustomUserCreationForm
import json


#pasword reset 
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str 
from django.template.loader import get_template
from django.template import Context
from .utils import TemplateEmail

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

       
            current_site = get_current_site(request)
            reset_link = f"{current_site}/reset-password/{uid}/{token}"

           
            email_context = {
                'user': user,
                'reset_link': reset_link
            }
    
            template = TemplateEmail(
                to=email,
                subject='Restablecimiento de contraseña',
                template='reset_password_email',
                context=email_context
            )

            template.fail_silently = False
            template.send()

            return render(request, 'password_reset/password_reset_success.html', {'success': True})
        else:
            return render(request, 'password_reset/password_reset_request.html', {'error': True, 'message': "Correo ingresado no existe, intente de nuevo"})

    return render(request, 'password_reset/password_reset_request.html')


def password_reset(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password == confirm_password:
                if not re.search(r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=]).*$', password):
                    return render(request, 'password_reset/password_reset.html', {'error': True, 'message': 'La contraseña no cumple los requisitos de seguridad.'})
                # Establecer la nueva contraseña para el usuario
                user.set_password(password)
                user.save()

                return render(request, 'password_reset/password_reset_success.html', {'message':'Su contraseña se ha reestablecido satisfactoriamente.'})
            else:
                return render(request, 'password_reset/password_reset.html', {'error': True, 'message': 'Las contraseñas deben coincidir.'})

        return render(request, 'password_reset/password_reset.html')
    else:
        return render(request, 'password_reset/password_reset_invalid.html')

#vista admin ( list animal )
@login_required
def admin_view(request):
    if request.user is not None:
        if(request.user.is_superuser):
            animales = Animal.objects.all()
            form = AnimalForm()
            context = {'animales': animales, 'form': form}
            return render(request, 'admin/panel.html', context)
        else:
            return render(request, 'users/acceso_denegado.html')
    else:
        return render(request, 'users/acceso_denegado.html')

def about_view(request):
    return render(request, 'about-us.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if(user.is_superuser):
                    return redirect('panel')
                else:
                    return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if(user.is_superuser):
                    return redirect('panel')
                else:
                    return redirect('index')
    else:
        #form = UserCreationForm()
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    animales = Animal.objects.filter(estado='disponible').order_by('id')

    #rangos para galeria principal
    rango1 = animales[:3]
    rango2 = animales[3:5]
    rango3 = animales[5:7]
    rangos = [rango1, rango2, rango3]

    context = {
        'rangos' : rangos
    }

    return render(request, 'index.html', context)

##carga datos de json a base de datos ( basicamente un seeder )
def cargar_datos_desde_json(request):
    with open('misPerris/assets/data.json', encoding='utf-8') as file:
        data = json.load(file)

        for region_data in data['regiones']:
            region = Region.objects.create(nombre=region_data['region'])

            for ciudad_data in region_data['comunas']:
                Ciudad.objects.create(nombre=ciudad_data, region=region)

    return HttpResponse('datos cargados')

def contact_view(request):
    form = ContactForm(request.POST or None)
   
    if form.is_valid():
        # Crear una nueva instancia de Contact y guardar los datos del formulario en ella
        name=form.cleaned_data['name']
        email=form.cleaned_data['email']
        rut=form.cleaned_data['rut']
        date_of_birth=form.cleaned_data['date_of_birth']
        phone=form.cleaned_data['phone']
        region = Region.objects.filter(id=request.POST['region']).first()
        city=form.cleaned_data['city']
        housing_type=form.cleaned_data['housing_type']
        terms=form.cleaned_data['terms']
        message=form.cleaned_data['message']
            
        contact = Contact(
            name=name,
            email=email,
            rut=rut,
            date_of_birth=date_of_birth,
            phone=phone,
            region=region,
            city=city,
            housing_type=housing_type,
            terms=terms,
            message=message
        )
        contact.save()

        context = {
            'name': name
        }


        # Redirigir a la página de éxito
        return render(request, 'events/success.html', context)
    else:
    # The form is not valid, so you need to correct the errors
        print(form.errors)
    context = {
        'form': form,
    }

    return render(request, 'forms/contact.html', context)

def rescatados_view(request):
    animales = Animal.objects.filter(estado='disponible')
    context = {'animales': animales}
    return render(request, 'animal-list.html', context)

def animal_detail(request, animal_id):
    animal = Animal.objects.get(id=animal_id)
    if not (animal):
        return render(request, 'events/acceso_denegado.html')
    else:
        return render(request, 'animals/animal_detail.html', {'animal': animal}) 


#animal crud ( create, edit, delete )
def animal_create(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('panel')
    else:
        form = AnimalForm()
    return render(request, 'forms/animal_form.html', {'form': form})

def animal_edit(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)

    if request.method == 'POST':
        if request.FILES.get('imagen'):
            if animal.imagen:
                imagen_path = animal.imagen.path
                if os.path.exists(imagen_path):
                    os.remove(imagen_path)
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            return redirect('panel')
    else:
        form = AnimalForm(instance=animal)

    return render(request, 'forms/animal_form.html', {'form': form, 'animal': animal})

def animal_delete(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    
    if request.method == 'POST':
        if animal.imagen:
            imagen_path = animal.imagen.path
            if os.path.exists(imagen_path):
                os.remove(imagen_path)
        # Procesar la eliminación del animal
        animal.delete()
        return redirect('panel')  
        
    return redirect('panel')

def success(request): 
    return render(request, 'events/success.html')





