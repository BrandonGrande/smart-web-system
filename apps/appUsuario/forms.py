from apps.appUsuario.models import User
from django.contrib.auth.forms import UserCreationForm



class registro_form(UserCreationForm):

	class Meta:
		model=User 
		fields=[ 
		       'username',
		       'first_name',
		       'last_name',
		       'email',
		       ]
	