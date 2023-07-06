from django.test import Client, TestCase, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from misPerris.models import Animal, CustomUser
from misPerris.forms import AnimalForm
from django.urls import reverse

class TestViews(TestCase):

    def setUp(self):
        # Crear un usuario de ejemplo
        self.user = CustomUser.objects.create_superuser(username='testuser', password='testpassword', is_staff=True)

        # Configurar el cliente de pruebas y autenticar al usuario
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        self.factory = RequestFactory()
        # Crear un animal de ejemplo
        Animal.objects.create(nombre='Perro', raza='Labrador', size='pequeno', peso='20', descripcion='Un perro muy amigable', estado='disponible', imagen='perro.jpg')


    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        

    def test_about_view(self):
        response = self.client.get(reverse('about-us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about-us.html')
        

    def test_contact_view(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forms/contact.html')
       

    def test_rescatados_view(self):
        response = self.client.get(reverse('rescatados'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'animal-list.html')
       

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
      

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        

   

    def test_animal_detail_view(self):
        #se crea un animal para poder obtenerlo
        Animal.objects.create(nombre='Perro', raza='Labrador', size='pequeno', peso='20', descripcion='Un perro muy amigable', estado='disponible', imagen='perro.jpg')
        animal_id = 1 

        response = self.client.get(reverse('animal-detail', kwargs={'animal_id': animal_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'animals/animal_detail.html')

        


    def test_make_solicitud_view(self):
        ##esta vista hace un redirect solicita un animal y un usuario conectado
        animal_id = 1  # Id válido de un animal existente
        
        response = self.client.post(reverse('solicitar', args=[animal_id]))
        self.assertRedirects(response, '/')
    
 
    def test_admin_view(self):
        response = self.client.get(reverse('panel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/panel.html')
     

    def test_animal_create_view(self):
            file = open('misPerris\\assets\img\crowfunding.jpg', 'r+b') 
            form_data = {
                'nombre': 'Perro2',
                'raza': 'Labrador',
                'size': 'pequeno',
                'peso': '20',
                'descripcion': 'Un perro muy amigable',
                'estado': 'disponible',
                'imagen': file
            }
            
            response = self.client.post(reverse('agregar'), data=form_data)

            self.assertEqual(response.status_code, 302)  
            self.assertTrue(Animal.objects.exists()) 
            created_animal = Animal.objects.get(nombre='Perro2')  
            self.assertEqual(created_animal.nombre, 'Perro2')  

    def test_animal_edit_view(self):
        # se cambian valores de animal id 1, se cambia nombre
        # se obtiene el animal con nuevo nombre
        file = open('misPerris\\assets\img\crowfunding.jpg', 'r+b') 
        form_data = {
            'nombre': 'Perro editado',
            'raza': 'Labrador',
            'size': 'pequeno',
            'peso': '20',
            'descripcion': 'Un perro muy amigable',
            'estado': 'disponible',
            'imagen': file
        }
        animal_id = 1  
        response = self.client.post(reverse('editar',  kwargs={'animal_id': animal_id}), data=form_data)
        self.assertEqual(response.status_code, 302)
        created_animal = Animal.objects.get(nombre='Perro editado')  
        self.assertEqual(created_animal.nombre, 'Perro editado')  
        

    def test_animal_delete_view(self):
        animal_id = 1 
        response = self.client.post(reverse('eliminar', kwargs={'animal_id': animal_id}))
        self.assertEqual(response.status_code, 302)
        animal = Animal.objects.filter(id=1)
        self.assertFalse(animal.exists())  
 

  

