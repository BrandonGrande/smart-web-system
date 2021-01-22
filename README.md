### Instalación del sistema inteligente | Smart system installation

El sistema inteligente solo puede utilizarse de manera local. Debido a las dependencias de la red neuronal (CNN), las cuales necesitan un alto grado de procesamiento.
The smart system can only be used locally. Due to the dependencies of neural network (CNN), which need a high degree of processing.

####Requerimiento principal | Main requirement
- Anaconda (Python 3.7) : Es necesario tener instalado Anaconda con Python 3.7, para hacer uso de las librerias que necesita la red neuronal convolucional. It is necessary to have Anaconda installed with Python 3.7, to make use of the libraries that the convolutional neural network needs.
![](https://assets-cdn.anaconda.com/assets/company/anaconda-logo.png?mtime=20200723150109&focal=none)

####Librerias | Librarys
- Django==3.1.1
- Django-cleanup==5.1.0
- Django-dbbackup==3.3.0
- Mysqlclient==2.0.1
- Numpy==1.17.1
- Tensorflow==1.13.1

####Base de datos  | Database
- MySQL: El proyecto utiliza la base de datos MySQL, por lo que deberas crear la base de datos en el servidor local con el nombre **bdsistemainteligente**. The project uses the MySQL database, so you must create the database on the local server with the name **bdsistemainteligente**.
![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-TNVDOv6IPeRc0blPM0bxy2zBNWnGIxlgGA&usqp=CAU)

####Pasos para implantación del sistema inteligente | Steps to implant the smart system

- Abrir la terminal del sistema operativo y ubicarte en la raiz del proyecto | Open the terminal of the operating system and go to the root of the project.
- Colocar los siguientes comandos | Place the following commands
 - Pip install requirements.txt 
 - Python manage.py migrate 
 - Python manage.py runserver

####Abrir el sistema inteligente | Open the smart system
- Abre un navegador web (Google Chrome, Firefox, Edge) | Open a web browser (Google Chrome, Firefox, Edge)
- Coloca la siguiente dirección en la URL | Put the following address in the URL
  - 127.0.0.1:8000





