from django.db import models
from django.contrib.auth import hashers
from django.contrib.auth.models import User

# Create your models here.

'''
class User(models.User):
	user_name = models.CharField(max_length = 20)
	user_password = models.CharField(max_length = 200)
	joined_date = models.DateTimeField('registed date')
	
	def __unicode__(self):
		return self.user_name
'''	
	
	
class Todolist(models.Model):
	user = models.ForeignKey(User)
	subject = models.CharField(max_length = 200)
	content = models.CharField(max_length = 500)
	added_date = models.DateTimeField('added date')
	last_edited_date = models.DateTimeField('last edited date')
	
	def __unicode__(self):
		return self.list_name
		
	