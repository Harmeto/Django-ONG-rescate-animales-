from django.urls import path
#para cargar y mostrar imagenes en otro lugar que no
#sea assets, cosas de BD se guardan aparte
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    #regular page
    path("", views.index, name="index"),
    path("about-us/", views.about_view, name="about-us"),
    path("contact/", views.contact_view, name="contact"),
    path("rescatados/", views.rescatados_view, name="rescatados"),

    #users
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    #path('acceso-denegado/', views.admin_view, name="check"),
    path('reset-password/', views.password_reset_request, name='password_reset_request'),
    path('reset-password/<str:uid>/<str:token>/', views.password_reset, name='password_reset'),     
    #animal
    path('animal-detail/<int:animal_id>', views.animal_detail, name="animal-detail"),

    #users admin
    path("panel/", views.admin_view, name="panel"),
    path("panel/agregar", views.animal_create, name="agregar"),
    path("panel/editar/<int:animal_id>", views.animal_edit, name="editar"),
    path("panel/eliminar/<int:animal_id>", views.animal_delete, name="eliminar"),
    # vista para cargar datos de region y ciudad a BBDD 
    #path('cargar_datos_desde_json/', views.cargar_datos_desde_json, name='cargar_datos_desde_json'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)