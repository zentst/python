from django.test import TestCase
from django.contrib.auth.models import User
from todo.models import Todolist
from django.core.urlresolvers import reverse
from django.utils import timezone

# Create your tests here.


def CreateNewUser(username, password, email):
	user = User()
	user.username = username
	user.set_password(password)
	user.email = email
	user.save()
	return user
	
def CreateNewList(user, subject, content):
	return user.todolist_set.create(subject = subject, content = content, added_date = timezone.now(), last_edited_date = timezone.now())
	

		
		

	
	
class UserLoginTest(TestCase):
	def test_user_login_with_correct_inpurt(self):
		user = CreateNewUser('test001', 'test001', 'test001@test.com')
		response =  self.client.post('/todo/userlogin/', {'username':'test001', 'password':'test001'})
		self.assertEqual(response.status_code, 302)
		redirect_response = self.client.get(response.url)
		self.assertContains(redirect_response, 'test001')
	
	def test_user_login_with_incorrect_username(self):
		CreateNewUser('test001', 'test001', 'test001@test.com')
		response =  self.client.post('/todo/userlogin/', {'username':'test002', 'password':'test001'})
		self.assertContains(response, 'username is not exist or password incorrect', status_code = 200)
		response2 = self.client.post('/todo/userlogin/', {'username':'', 'password':'test001'})
		self.assertContains(response2, 'This field is required', status_code = 200)
	
	def test_user_login_with_incorrect_password(self):
		CreateNewUser('test001', 'test001', 'test001@test.com')
		response =  self.client.post('/todo/userlogin/', {'username':'test001', 'password':'test002'})
		self.assertContains(response, 'username is not exist or password incorrect', status_code = 200)
		response2 = self.client.post('/todo/userlogin/', {'username':'test001', 'password':''})
		self.assertContains(response2, 'This field is required', status_code = 200)

		
		
	def test_user_login_while_already_login(self):
		CreateNewUser('test001', 'test001', 'test001@test.com')
		self.client.post('/todo/userlogin/', {'username':'test001', 'password':'test001'})
		response = self.client.post('/todo/userlogin/', {'username':'test001', 'password':'test001'})
		self.assertEqual(response.status_code, 302)
		redirect_response = self.client.get(response.url)
		self.assertContains(redirect_response, 'test001')
		
		
class UserRegisterTest(TestCase):
	
	def test_user_register_with_correct_input(self):
		username = 'test001'
		password = 'test001'
		repeatpassword = 'test001'
		email = 'zentst@test.com'
		
		response = self.client.post('/todo/register/',{'username':username, 'password':password, 'repeatpassword':repeatpassword, 'email':email})
		self.assertEqual(response.status_code, 302)
		redirect_response = self.client.get(response.url)
		self.assertContains(redirect_response, 'test001')
		self.assertContains(redirect_response, 'regist succeed')
		
	def test_user_register_with_two_diffrent_password(self):
		username = 'test001'
		password = 'test001'
		repeatpassword = 'test002'
		email = 'zentst@test.com'
		
		response = self.client.post('/todo/register/',{'username':username, 'password':password, 'repeatpassword':repeatpassword, 'email':email})

		self.assertContains(response, 'repeat password is not the same', status_code = 200)
		
	def test_user_register_with_empty_form(self):
		username = 'test001'
		password = 'test001'
		repeatpassword = 'test001'
		email = 'zentst@test.com'					
		response = self.client.post('/todo/register/',{'username':'', 'password':password, 'repeatpassword':repeatpassword, 'email':email})
		self.assertContains(response, 'This field is required', status_code = 200)
		
	
	def test_user_register_with_invalid_email_format(self):
		#this test may not working as design, nothing useless
		username = 'test001'
		password = 'test001'
		repeatpassword = 'test001'
		email = 'zentst1test.com'					
		response = self.client.post('/todo/register/',{'username':'', 'password':password, 'repeatpassword':repeatpassword, 'email':email})
		self.assertContains(response, 'This field is required', status_code = 200)
		
	def test_user_register_with_exist_user(self):
		CreateNewUser('test001', 'test001', 'test001@test.com')
		username = 'test001'
		password = 'test001'
		repeatpassword = 'test001'
		email = 'zentst@test.com'				
		response = self.client.post('/todo/register/',{'username':username, 'password':password, 'repeatpassword':repeatpassword, 'email':email})				
		self.assertContains(response, 'username is exist', status_code = 200)
		
class AddTodoListTest(TestCase):
	
	def test_add_todo_withow_login(self):
		subject = 'news'
		content = 'is a goodnew'
		response = self.client.post('/todo/add/',{'subject':subject, 'content':content})
		self.assertEqual(response.status_code, 302)
		response = self.client.get(response.url)
		self.assertContains(response, 'login', status_code = 200)
		
	def test_add_todo_after_login(self):
		subject = 'news'
		content = 'is a goodnew'
		CreateNewUser('test001', 'test001', 'test001@test.com')
		self.client.post('/todo/userlogin/', {'username':'test001', 'password':'test001'})
		response = self.client.post('/todo/add/', {'subject':subject, 'content':content})
		self.assertEqual(response.status_code, 302)
		redirect_response = self.client.get(response.url)
		self.assertContains(redirect_response, 'news', status_code = 200)
		self.assertContains(redirect_response, 'add succeed')
		
class DetailEditViewTest(TestCase):
	def test_datail_view_withou_login(self):
		subject = 'news'
		content = 'is a goodnew'
		user = CreateNewUser('test001', 'test001', 'test001@test.com')		
		CreateNewList(user, subject, content)
		response = self.client.get('/todo/1/')
		self.assertEqual(response.status_code, 302)
		redirect_response = self.client.get(response.url)
		self.assertContains(redirect_response, 'login', status_code = 200)
	
	def test_detail_display(self):
		subject = 'news'
		content = 'is a goodnew'
		CreateNewUser('test001', 'test001', 'test001@test.com')
		self.client.post('/todo/userlogin/', {'username':'test001', 'password':'test001'})
		self.client.post('/todo/add/', {'subject':subject, 'content':content})
		response = self.client.get('/todo/1/')
		self.assertContains(response, 'is a goodnew', status_code = 200)
	
	def test_detail_display_with_invalid_id(self):
		subject = 'news'
		content = 'is a goodnew'
		user = CreateNewUser('test001', 'test001', 'test001@test.com')
		CreateNewList(user, subject, content)
		self.client.post('/todo/userlogin/', {'username':'test001', 'password':'test001'})
		response = self.client.get('/todo/2/')
		self.assertContains(response, 'no permit.This list does not exist', status_code = 200)
		
	def test_detail_display_with_other_user_id(self):
		subject = 'news'
		content = 'is a goodnew'
		user = CreateNewUser('test001', 'test001', 'test001@test.com')
		CreateNewList(user, subject, content)
		user = CreateNewUser('test002', 'test002', 'test002@test.com')
		self.client.post('/todo/userlogin/', {'username':'test002', 'password':'test002'})
		response = self.client.get('/todo/1/')
		self.assertContains(response, 'no permit.This is not your list', status_code = 200)
					
			
		
	def test_Edit_view(self):
		subject = 'news'
		content = 'is a goodnew'
		CreateNewUser('test001', 'test001', 'test001@test.com')
		self.client.post('/todo/userlogin/', {'username':'test001', 'password':'test001'})
		self.client.post('/todo/add/', {'subject':subject, 'content':content})
		response = self.client.post('/todo/1/edit/', {'subject':'badnew', 'content':'it is badnew'})
		self.assertEqual(response.status_code, 302)
		redirect_response = self.client.get(response.url)
		self.assertContains(redirect_response, 'edit succeed', status_code = 200)
		self.assertEqual(Todolist.objects.get(pk=1).content, 'it is badnew')
				
class DeleteViewTest(TestCase):
	
	def test_delete(self):
		subject = 'news'
		content = 'is a goodnew'
		CreateNewUser('test001', 'test001', 'test001@test.com')
		self.client.post('/todo/userlogin/', {'username':'test001', 'password':'test001'})
		self.client.post('/todo/add/', {'subject':subject, 'content':content})
		response = self.client.post('/todo/1/delete/')
		self.assertEqual(response.status_code,302)
		response = self.client.get(response.url)
		self.assertContains(response, 'delete succded', status_code=200)
	
	def test_delete_with_invalid_list(self):
		subject = 'news'
		content = 'is a goodnew'
		CreateNewUser('test001', 'test001', 'test001@test.com')
		self.client.post('/todo/userlogin/', {'username':'test001', 'password':'test001'})
		response = self.client.post('/todo/1/delete/')
		self.assertEqual(response.status_code,302)
		response = self.client.get(response.url)
		self.assertContains(response, 'delete fail.list not exist', status_code=200)
			
	def test_delete_with_incorrect_user(self):
		subject = 'news'
		content = 'is a goodnew'
		CreateNewUser('test001', 'test001', 'test001@test.com')
		user = CreateNewUser('test002', 'test002', 'test002@test.com')
		CreateNewList(user, subject, content)
		self.client.post('/todo/userlogin/', {'username':'test001', 'password':'test001'})
		response = self.client.post('/todo/1/delete/')
		self.assertEqual(response.status_code,302)
		response = self.client.get(response.url)
		self.assertContains(response, 'delete fail.this is not your list', status_code=200)