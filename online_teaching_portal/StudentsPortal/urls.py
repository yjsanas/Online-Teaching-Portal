from django.urls import path

from . import views

urlpatterns = [
    path('', views.Login, name='login'),
    path('logout', views.Logout, name='login'),
    path('register', views.register, name='register'),
     path('home', views.home, name='home'),
    path('temp', views.temp, name='temp'),
    path('temppost', views.temppost , name='temp'),
    
    
    # courses    
    path('slistcourse.html', views.slistcourse),
    path('joincourse.html', views.joincourse),
    path('sunenrolcourse/<int:cid>/', views.unenrolcourse),
    path('sviewmaterials/<int:cid>/', views.sviewmaterial),
    #attendance
    path('viewattendance.html', views.viewattendance),




    #materials
    path('allmaterials.html', views.allmaterials),
    path('smaterialinfo/<int:cid>/<int:mid>/', views.smaterialinfo),
    
    
    
    
]