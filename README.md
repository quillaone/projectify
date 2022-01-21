# projectify
Prueba backend Leanware.io

dentro del repo va un archivo requirements.txt el cual debe ser instalado dentro del ambiente virtual con el comando $pip install -r requirements.txt

luego que se instalen todo los archivos, solo es correr el servicor $python manage.py runserver

adjunto url para evidenciar la documentacion de la API en postman
https://documenter.getpostman.com/view/18241310/UVXomuDk

 API RESTful usando Django y  base de datos "Mysql"  usuarios operativos de AdsForGood reportar, cada semana, su porcentaje de dedicación a cada uno de los   proyectos de la empresa.

1. usuario operativo, puede iniciar sesión en la aplicación para obtener un JWT (JSON Web Token) y poder disfrutar de las funcionalidades de Projectify.
2. metodo de registro, metodo de Login y metodo de LogOut.
3. 
4. usuario operativo, puede ver todos los proyectos de la empresa.(addforGood)
5. usuario operativo, puede reportar cada semana porcentaje de dedicación a
cada proyecto.
para esto dentro del atributo del modelo, se valido un maximo (100) y un minimo (1), ya ue el porcentaje va del 1% al 100%
4. usuario operativo, puede ver o consultar reportes pasados de dedicación.
5. usuario operativo, puede editar los reportes de dedicación siempre y
cuando estén en el mismo mes calendario de la fecha de edición.

 Un usuario no puede poder reportar dos veces la misma semana-proyecto.
para esto se declaro un atributo o campo en el modelo de reportes, el cual fue la fecha de creacion, y por medio de este se obtiene el numero de la semana,
para luego hacer la validacion.
