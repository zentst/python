from django.contrib import admin
from todo.models import Todolist

# Register your models here.

class TodolistAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['list_name']}),
        ('user imformation', {'fields':['user'],}),
		('date imformation',{'fields':['added_date','last_edited_date'],}),
		('todo context',{'fields':['content'],}), 
        ]
    list_display = ('subject', 'user', 'added_date', 'last_edited_date')
    search_fields = ['subject']

admin.site.register(Todolist, TodolistAdmin)