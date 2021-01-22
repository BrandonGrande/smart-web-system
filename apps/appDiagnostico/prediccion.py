import numpy as np
#Libreria para conversion de imagenes
from tensorflow.keras.preprocessing.image import load_img, img_to_array
#Libreria para cargar el modelo
from tensorflow.keras.models import load_model
#import os.path
from django.conf import settings
import os

#funcion de predicion de enfermedad recibe(Imagen JPG, PNG)
def prediccion(file):
    #longitud que tendra la imagen
    longitud,altura=100,100
    #directorios del modelos y pesos entrenados
    #BASE = os.path.dirname(os.path.abspath(__file__))
    modelo =os.path.join(settings.BASE_DIR, 'modelo_red_neuronal/modelo.h5')
    pesos = os.path.join(settings.BASE_DIR, 'modelo_red_neuronal/pesos.h5')

    #cargar archivos del modelo y pesos
    cnn=load_model(modelo)
    cnn.load_weights(pesos)
    #carga la imagen
    x=load_img(file,target_size=(longitud,altura))
    #convierte en arreglo la imagen
    x=img_to_array(x)/255.
    #dimension extra
    x=np.expand_dims(x,axis=0)
    #llamada a la red recibe(arreglo)
    #arreglo=cnn.predict(x)
    probabilidades=cnn.predict_proba(x)
    clase=cnn.predict_classes(x)
    #p = np.array(arreglo2)
    #print(p.sum())
    #print(arreglo)
    #print(arreglo2)
    #print(arreglo3)
    #resultado de la prediccion
    #resultado=arreglo[0]
    #el valor mas alto del arreglo indica la predicion recibe(arreglo)
    #respuesta=np.argmax(resultado)
    #determina enfermedad

    return {'probabilidades':probabilidades,'clase':clase}


