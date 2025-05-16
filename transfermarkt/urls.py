"""
URL configuration for transfermarkt project.

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
from django.urls import path
from transfermarkt import views
from .views import registrazione
from .views import Lista_Nazionalita
from .views import login
from .views import benvenuto
from .views import login_admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', benvenuto, name='benvenuto'),  # Home mostra benvenuto.html
    path('benvenuto/', benvenuto, name='benvenuto'),
    path('login/', login, name='login'),
    path('login_admin/', views.login_admin, name='login_admin'),
    path('registrazione/', registrazione, name='registrazione'),
    path('nazionalita/', Lista_Nazionalita, name='nazionalita'),
    path('principale/', views.partite_settimana, name='principale'),
]




    # ... altre url ...


