from django import forms
from dynamic_forms import DynamicField, DynamicFormMixin
from django.core.validators import EmailValidator
from django.contrib.auth.forms import UserCreationForm
from .models import Contact, Region, Ciudad, Animal, CustomUser
import re

class CustomUserCreationForm(DynamicFormMixin, UserCreationForm):
    def city_choices(form):
            region = form['region'].value()
            return Ciudad.objects.filter(region=region)
    
    def initial_city(form):
        region = form['region'].value()
        return Ciudad.objects.filter(region=region)

    region = forms.ModelChoiceField(queryset=Region.objects.all(), initial=None, required=True, label='Region', empty_label='Regiones')
    city = DynamicField( forms.ModelChoiceField, queryset=city_choices, required=True, label='Ciudad', empty_label='Seleccione una region')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'region', 'city')



class ContactForm(DynamicFormMixin, forms.Form):

    def city_choices(form):
        region = form['region'].value()
        return Ciudad.objects.filter(region=region)
    
    def initial_city(form):
        region = form['region'].value()
        return Ciudad.objects.filter(region=region)
      
    HOUSING_CHOICES = (
        ('Casa con patio grande', 'Casa con patio grande'),
        ('Casa con patio pequeño', 'Casa con patio pequeño'),
        ('Casa sin patio', 'Casa sin patio'),
        ('Departamento', 'Departamento'),
    )

    region = forms.ModelChoiceField(queryset=Region.objects.all(), initial=None, required=True, label='Region', empty_label='Regiones')
    city = DynamicField( forms.ModelChoiceField, queryset=city_choices, required=True, label='Ciudad', empty_label='Seleccione una region')
    name = forms.CharField(max_length=200, required=True, label='Nombre Completo')
    email = forms.CharField(label='Correo electrónico', max_length=100, validators=[EmailValidator], required=True)
    rut = forms.CharField(label='RUT', max_length=10, required=True, widget=forms.TextInput(attrs={'pattern': '[0-9]{7,8}-[0-9Kk]{1}'}))
    date_of_birth = forms.DateField(label='Fecha de nacimiento', required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    phone = forms.CharField(label='Teléfono de contacto', max_length=20, required=True)
    housing_type = forms.ChoiceField(label='Tipo de vivienda', choices=HOUSING_CHOICES, required=True)
    terms = forms.BooleanField(label='Acepto términos y condiciones', required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols': 40}), label='Mensaje', max_length=250, required=False)

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nombre', 'imagen', 'raza', 'descripcion', 'estado', 'size', 'peso']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(AnimalForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].required = True

    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        if peso:
            # Patrón de expresión regular para solo aceptar números con una parte decimal opcional
            patron = r'^\d+(\.\d+)?$'
            if not re.match(patron, peso):
                raise forms.ValidationError("El peso debe ser un número válido.")
        return peso
    