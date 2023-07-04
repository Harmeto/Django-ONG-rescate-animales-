from django.contrib import admin
from .models import Animal, Contact, CustomUser

admin.site.register(Animal)
admin.site.register(CustomUser)
admin.site.register(Contact)
