from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os

class User(AbstractUser):
	image=models.ImageField(upload_to='usuarios',null=True,blank=True)
	email = models.EmailField('Email address', unique=True)
	username = models.CharField(max_length=30, unique=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	
	def get_image(self):

		if(self.image):
			return '{}{}'.format(settings.MEDIA_URL,self.image)
		return '{}{}'.format(settings.MEDIA_URL,'usuarios/perfil.png')



