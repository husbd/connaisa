"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

app_name = 'connaisaV0'
urlpatterns = [
    url(r'^index/', views.index, name="index"),
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^accounthome/', views.accounthome, name="accounthome"),
    url(r'^editprofile/', views.editProfile, name="editprofile"),
    url(r'^newpost/', views.newPost, name="newpost"),
    url(r'^post/(?P<post_id>\d+)/$', views.viewPost, name="viewpost"),
    url(r'^editpost/(?P<post_id>\d+)/$', views.editPost, name="editpost"),
    url(r'^userpage/(?P<user_id>\d+)/$', views.userPage, name="userpage"),
    #url(r'^search/', views.search, name="search"),
    #test use only
    url(r'^clean/', views.clean, name="clean"),
    url(r'^main/$', views.main, name="main"),
    url(r'^$', views.index, name="index"),

]