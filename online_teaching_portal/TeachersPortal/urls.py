from django.urls import path
from . import models
from . import views

urlpatterns = [
    path('', views.Login, name='login'),
    path('tlogin.html', views.Login, name='tlogin'),
    path('tregister', views.register, name='register'),
    
    path('temppost', views.temppost , name='temp'),
    path('thome.html', views.thome , name='home'),
    path('tlogout', views.Logout , name='logout'),
    # courses
    path('taddcourse.html', views.AddCourse),
    path('tcourse.html', views.ViewCourse),
    path('updateCourse.html', views.updatePostCourse),
    path('updateCourse/<int:cid>/', views.updateGetCourse),
    path('deletecourse/<int:cid>/', views.deleteCourse),
    
    #attendance
    path('viewattendance/<int:cid>/', views.viewattendance),
    path('attendance.html', views.attendance),    
    path('attendancecourses.html', views.attendancecourses),
    path('fullattendance/<int:cid>/', views.fullattendance),
    path('Upadateattendance/<int:cid>/<str:date>/', views.Upadateattendance),
    
    
    
     
    # assignment
    path('taddassignment.html', views.taddassignment),
    path('tcourse.html', views.tViewAssignment),

    # materials
    path('taddmaterials.html', views.Addmaterials , name='addmaterials'),
    path('tmaterials.html', views.tmaterials , name='addmaterials'),  
    path('tmaterials/<int:cid>/', views.detailedCourse),#this is for displaying list of materials and assignments in theat course 
    path('tupdatematerials/<int:mid>/', views.updateMaterials),#update the materials in that course dont move these t2o any where
    path('updatematerials', views.updatepostmaterials , name='updatematerials'),  
    path('delete/<int:mid>/', views.deleteMaterial),
    
]