from django.shortcuts import render
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Todolist

# Create your views here.

class RegisterForm(forms.Form):
	username = forms.CharField(label='username')
	password = forms.CharField(label='password', widget = forms.PasswordInput)
	repeatpassword = forms.CharField(label='repeat password', widget = forms.PasswordInput)
	email = forms.EmailField()
	
class LoginForm(forms.Form):
	username = forms.CharField(label='username')
	password = forms.CharField(label='password', widget = forms.PasswordInput)

class ListForm(forms.Form):
	subject = forms.CharField(label='title')
	content = forms.CharField(label='content', widget = forms.Textarea)

@login_required(login_url = 'todo:login')
def index(request):
	todolist = request.user.todolist_set.all()
	#catch HttpResonseRedirect message
	try:
		redirect_message = request.session['redirect_message']
	except Exception:
		context = {'todolist':todolist}
	else:
		context = {'todolist':todolist, 'redirect_message':redirect_message}
	return render(request, 'todo/index.html', context)

@login_required(login_url = 'todo:login')
def add(request):
	if request.method == 'POST':
		subject = request.POST['subject']
		content = request.POST['content']
		#check input is valid
		addform = ListForm({'subject':subject, 'content':content,})
		if not addform.is_valid():
			return render(request, 'todo/add_edit.html',{'form':addform})
		add_date = timezone.now()
		#create new todo quest	
		request.user.todolist_set.create(
			subject = subject, 
			content = content,
			added_date = add_date,
			last_edited_date = add_date
			)
		request.session['redirect_message'] = 'add succeed'
		return HttpResponseRedirect(reverse('todo:index'))
	else:
		addform = ListForm()
		return render(request, 'todo/add_edit.html', {'form':addform})


def register(request):
	#user logined, redirect to index
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('todo:index'))
	# get post data	
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		repeatpassword = request.POST['repeatpassword']
		email = request.POST['email']
		# checking post data
		registerform = RegisterForm({'username':username, 'password':password, 'repeatpassword':repeatpassword, 'email':email})
		if not registerform.is_valid():
			return render(request, 'todo/register.html', {'form':registerform})
		
		if password != repeatpassword:
			return render(request, 'todo/register.html',{
				'form':registerform,
				'error_message':'repeat password is not the same'
				})
		# check username exist
		if len(User.objects.filter(username = username)) > 0:
			return render(request, 'todo/register.html',{
				'form':registerform,
				'error_message':'username is exist'
				})
		# create new user	
		new_user = User()
		new_user.username = username
		new_user.set_password(password)
		new_user.email =  email
		new_user.save()
		#check new user is valid
		new = authenticate(username = username, password = password)
		if new is not None:
			login(request, new)
			request.session['redirect_message'] = 'regist succeed'
			return HttpResponseRedirect(reverse('todo:index'))
	else:
		#in not post request, create a new form for input
		registerform = RegisterForm()
		return render(request, 'todo/register.html',{'form':registerform})

def userlogout(request):
	if request.user.is_authenticated():
		logout(request)
	return HttpResponseRedirect(reverse('todo:login'))

def userlogin(request):
	#if already login,redirect to index
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('todo:index'))
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']		
		#check form input correction
		loginform = LoginForm({'username':username, 'password':password})
		if not loginform.is_valid():
			return render(request, 'todo/login.html', {'form':loginform})
		else:
			#check user valid
			user = authenticate(username = username, password = password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('todo:index'))
			else:
				return render(request, 'todo/login.html', {'form':loginform, 'error_message':'username is not exist or password incorrect'})
	else:
		#display loginform
		loginform = LoginForm()
		return render(request, 'todo/login.html',{'form':loginform})
		
	
@login_required(login_url = 'todo:login')	
def detail(request, list_id):
	#check this list exist and belond to user ,if not, return error
	try:
		request_list = Todolist.objects.get(pk = list_id)
	except Todolist.DoesNotExist:
		return render(request, 'todo/detail.html', {'error_message':'no permit.This list does not exist'})
	if request_list.user != request.user:
		return render(request, 'todo/detail.html', {'error_message':'no permit.This is not your list'})
	#display list	
	listform = ListForm({'subject':request_list.subject, 'content':request_list.content})
	return render(request, 'todo/detail.html',{'todolist':request_list, 'form':listform})

@login_required(login_url = 'todo:login')		
def edit(request, list_id):
	request_list = Todolist.objects.get(pk = list_id)
	subject = request.POST['subject']
	content = request.POST['content']
	listform = ListForm({'subject':subject, 'content':content})
	if not listform.is_valid():
		return render(request, 'todo/detail.html',{'form':listform, 'todolist':request_list})
	#set todolist new values
	request_list.subject = subject
	request_list.content = content
	request_list.last_edited_date = timezone.now()
	request_list.save()
	request.session['redirect_message'] = 'edit succeed'
	return HttpResponseRedirect(reverse('todo:index'))
		
@login_required(login_url = 'todo:login')
def delete(request, list_id):
	try:
		request_list = Todolist.objects.get(pk = list_id)
	except Todolist.DoesNotExist:
		request.session['redirect_message'] = 'delete fail.list not exist'
		return HttpResponseRedirect('/todo/')	
	if request_list.user == request.user:
		request_list.delete()
		request.session['redirect_message'] = 'delete succded'		
		return HttpResponseRedirect('/todo/')	
	else:
		request.session['redirect_message'] = 'delete fail.this is not your list'			
		return HttpResponseRedirect('/todo/')
		