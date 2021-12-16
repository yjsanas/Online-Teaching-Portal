from django import forms  
class Materialsform(forms.Form): 
    material_title = forms.CharField(label="Material Title",max_length=50)  
    coursename  = forms.CharField(label="Course Name", max_length = 10)  
    mdec     = forms.EmailField(label="Material description")  
    file      = forms.FileField() # for creating file input 
   

