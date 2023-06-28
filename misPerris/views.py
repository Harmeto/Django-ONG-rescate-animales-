from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

#manipulacion de archivos
import os

#login - logout - admin
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

#models - forms
from .models import Region, Ciudad, Contact, Animal
from .forms import ContactForm, AnimalForm
import json
# Create your views here.

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if(user.is_superuser):
                    return redirect('panel')
                else:
                    return redirect('index')
    else:
        form = UserCreationForm()
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





