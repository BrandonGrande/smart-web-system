#libreria para poder movernos en carpetas del sistema operativo
import sys
import os
import numpy as np
#libreria para preprocesar las imagenes del entrenamiento
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
#libreria que contiene un optimizador para el algoritmo
from tensorflow.python.keras import optimizers
#libreria que permite hacer redes neuronales secuenciales 
from tensorflow.python.keras.models import Sequential
#libreria de redes neuronales 
from tensorflow.python.keras.layers import Dropout, Flatten, Dense, Activation
#libreria para las capas de las convoluciones 
from tensorflow.python.keras.layers import  Convolution2D, MaxPooling2D
#libreria para las sesiones de keras 
from tensorflow.python.keras import backend as K

from sklearn.metrics import confusion_matrix

from django.conf import settings

def entrenamiento_red_neuronal(num_filtro1,num_filtro2,num_epocas,num_clases):
    K.clear_session()
    #directorios de imagenes para entrenar 

    data_entrenamiento = os.path.join(settings.BASE_DIR, 'media/imgEntrenamiento')
    data_validacion =os.path.join(settings.BASE_DIR, 'media/imgValidacion') 
    #numero de veces que se itera 
    epocas=num_epocas
    #tamaño de las imagenes 
    altura,longitud = 100, 100
    #numero de imagenes que mandaremos a procesar 
    batch_size = 30
    #numero de veces que se procesa la informacion de cada epoca 
    pasos = 1
    #Numero de veces que se valida la informacion 
    pasos_validacion = 200
    #Numero de filtros que se aplica en cada convolucion
    filtrosConv1 = num_filtro1
    filtrosConv2 = num_filtro2
    #Tamaño de los filtros 
    tamano_filtro1 = (3, 3)
    tamano_filtro2 = (2, 2)
    #Tamaño del maxpooling
    tamano_pool = (2, 2)
    #clasificaciones que tendra la red 
    clases = num_clases
    #ajustador de la red
    lr = 0.0005
    #Preprocesamiento de imagenes (Ajusta las imagenes)
    entrenamiento_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
        )
    #Preprocesamiento de imagenes de validacion
    validacion_datagen = ImageDataGenerator(
        rescale=1. / 255    
        )

    #Abre la carpeta de entrenamiento y obtiene las imagenes para clasificarlas 
    imagen_entrenamiento=entrenamiento_datagen.flow_from_directory(
        data_entrenamiento,
        target_size=(altura,longitud),
        batch_size=batch_size,
        class_mode='categorical'    
        )
    #Abre la carpeta de validacion y obtiene las imagenes para clasificarlas 
    imagen_validacion=validacion_datagen.flow_from_directory(
        data_validacion,
        target_size=(altura,longitud),
        batch_size=batch_size,
        class_mode='categorical'
        )

    #La red neuronal es secuencial
    cnn=Sequential()
    #Capa de la primera convolucion con funcion de activacion relu
    cnn.add(Convolution2D(filtrosConv1, tamano_filtro1, padding='same',input_shape=(altura,longitud,3),activation='relu'))
    #Capa de pooling 
    cnn.add(MaxPooling2D(pool_size=tamano_pool))
    #Capa de la segunda convolucion con funcion de activacion relu
    cnn.add(Convolution2D(filtrosConv2, tamano_filtro2, padding='same',activation='relu'))
    #Capa de pooling 
    cnn.add(MaxPooling2D(pool_size=tamano_pool))
    #Convierte la imagen a una sola dimencion 
    cnn.add(Flatten())
    #Capa con 256 neuronas y funcion de activacion relu
    cnn.add(Dense(256,activation='relu'))
    #Durante el procesamiento se apagan la mitad de las 256 neuronas para evitar sobreajuste
    cnn.add(Dropout(0,5))
    #Capa que ayuda a clasificar, tiene neuronas de acuerdo a las clases y funcion de activacion softmax 
    cnn.add(Dense(clases, activation='softmax'))
    #Funcion de perdida, optimizador y metrica de optimizacion 
    cnn.compile(loss='categorical_crossentropy', optimizer=optimizers.Adam(lr=lr),metrics=['accuracy'])
    #realiza entrenamiento 
    hist=cnn.fit_generator(imagen_entrenamiento,steps_per_epoch=pasos,epochs=epocas,validation_data=imagen_validacion, validation_steps=pasos_validacion
        )

    calidad=hist.history['val_acc']
    error=hist.history['val_loss']
    clases=imagen_validacion.class_indices
    #dire=os.path.join(settings.BASE_DIR, 'modelo_red_neuronal')
    
    #if not os.path.exists(dire):
    #   os.mkdir(dire)


    cnn.save(os.path.join(settings.BASE_DIR, 'modelo_red_neuronal/modelo.h5'))
    cnn.save_weights(os.path.join(settings.BASE_DIR, 'modelo_red_neuronal/pesos.h5'))

    return {'calidad':calidad,'error':error,'clases':clases}
