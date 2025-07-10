"""
URL configuration for mshp_ctf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexPage.as_view(), name='index'),
    path('calc/', views.CalcPage.as_view(), name='calc'),
    path('profile/<int:id>/', views.ProfilePage.as_view(), name='profile'),
    path('create_note/', views.CreateNotePage.as_view(), name='create_note'),
    path('notes/', views.NotesPage.as_view(), name='notes'),
    path('note/<int:id>/', views.NotePage.as_view(), name='note'),
    path('7b2768656164657273273a20276f6e277d/', views.SecretPage.as_view(), name='secret'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', include('django_registration.backends.one_step.urls')),
]
