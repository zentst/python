from django.conf.urls import include, url
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name = 'index'),
    url(r'^add/$', views.add, name = 'add'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^userlogin/$', views.userlogin, name = 'login'),    
    url(r'^userlogout/$', views.userlogout, name = 'logout'),
    url(r'^(?P<list_id>\d+)/$',views.detail, name = 'detail'),
    url(r'^(?P<list_id>\d+)/edit/$', views.edit, name = 'edit'),
    url(r'^(?P<list_id>\d+)/delete/$', views.delete, name = 'delete'),
]
