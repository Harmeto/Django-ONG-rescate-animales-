from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='region')

    def __str__(self):
        return self.nombre

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    rut = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='region_nombre')
    city = models.ForeignKey(Ciudad, on_delete=models.CASCADE, related_name='ciudad_nombre')
    housing_type = models.CharField(max_length=100)
    terms = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.name
    
class Animal(models.Model):
    ESTADO_CHOICES = (
        ('rescatado', 'Rescatado'),
        ('disponible', 'Disponible'),
        ('adoptado', 'Adoptado'),
    )

    SIZE_CHOICES = (
        ('pequeno', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande')
    )

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='animal_images')
    raza = models.CharField(max_length=100)
    size = models.CharField(max_length=50, choices=SIZE_CHOICES)
    peso = models.CharField(max_length=10)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)


    def __str__(self):
        return self.nombre
    