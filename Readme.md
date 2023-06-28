//STAR PROYECT U NEED INSTALL REQUIREMENTS.TXT

-- install requirement.txt 
pip install -r requirements.txt

-- create a env 
python -m venv "name env" 
sourceFolder/ "name env"/bin/activate.bat

-- migrate DB 
python manage.py makemigrations
python manage.py migrate

-- in case regions / cities dont load 
on aseets/data.json check if its load and 
activate route #path('cargar_datos_desde_json/', views.cargar_datos_desde_json, name='cargar_datos_desde_json'), 
run the server and go to that route, then regions / cities are populated on your DB  


-- create superuser for check admin page and panel page( panel page is only in the site ) 
manage.py createsuperuser

-- runserver
python manage.py runserver


--pythonanywhere domain 
harmeto.pythonanywhere.com
