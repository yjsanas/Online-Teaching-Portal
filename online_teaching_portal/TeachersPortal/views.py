from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from . import forms
from  StudentsPortal import models as smodel
import datetime
import json
import django_filters
def Logout(request):
    del request.session['context']
    del request.session['tloginsuccess']
    return render(request,'login/tlogin.html')
    
def Login(request):        
    print(request.session.get('tloginsuccess'))
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        print(context)
        return render(request,'home/thome.html',context)
    else:   
        if request.method=="POST":        
            emailid=request.POST['inputEmailAddress']
            ipassword=request.POST['inputPassword']      
            print('email',emailid,'pass',ipassword)      
            data=models.Teacherlogin.objects.filter(email=emailid,password=ipassword).exists()
            print(data)
            if data is True:
                sdata=models.Teacherlogin.objects.get(email=emailid,password=ipassword)
                fname=sdata.first_name
                lname=sdata.last_name
                name=fname+' '+lname
                context={'name':name,'tid':sdata.Tid}
                request.session['context']=context
                print(name)     
                request.session['tloginsuccess']=True       
                print(request.session.get('tloginsuccess'))     
                return render(request,'home/thome.html',context)
            else:
                messages.error(request,10,'invalid credentials',)            
                print('login fail')
                return redirect('login/tlogin.html')
        else:
            return render(request,'login/tlogin.html')

# home page
def thome(request):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        print(context)
        return render(request,'home/thome.html',context)
    return render(request,'login/tlogin.html')


def register(request):
    if request.method=="POST":   
        print('post')     
        First_Name=request.POST['inputFirstName']
        sLast_Name=request.POST['inputLastName']
        emailid=request.POST['inputEmailAddress']
        spassword=request.POST['inputPassword']
        spassword=request.POST['inputConfirmPassword']
        regemail=models.Teacherlogin.objects.filter(email=emailid).exists()
        if(regemail is False ):
            data=models.Teacherlogin(first_name=First_Name,last_name=sLast_Name,email=emailid,password=spassword)
            data.save()
            print('data inserted success')
            return render(request,'login/tlogin.html')
        else:
            return render(request,'login/tregister.html')
    return render(request,'login/tregister.html')


# materials==========================================================================================================================================================
def Addmaterials(request):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="GET":            
            data=models.tcourse.objects.filter(tid=context['tid']).values()
            context['cnames']=data            
            return render(request,'materials/taddmaterials.html',context)        
        if request.method=="POST":                 
            print(context)           
            cid=request.POST['courseName']                       
            mtitle=request.POST['materialTitle']
            mdesc=request.POST['materialDescription']                        
            tid=context['tid']
            if models.material.objects.exists() :
                mid=models.material.objects.last()                
                print("mid=",int(mid.mid+1) )

            else:
                mid=1
            mdoc = request.FILES['mydoc'] if 'mydoc' in request.FILES else None    
            fileurl=None  
            if 'mydoc' in request.FILES:
                mid=int(mid.mid+1)
                mdocname=str(mid)+ mdoc.name
                fs= FileSystemStorage()
                file = fs.save(mdocname, mdoc) 
                print("document name",mdocname)
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed. 
                # fileurl = fs.url(file)                
                # print('last mid',mid.mid)                        
                print('file url',fileurl,'dovumentname=',mdocname)    
                mdoc=mdocname        
                # return HttpResponse('waiy')                                       
            data=models.material(tid=tid,mtitle=mtitle,mdecription=mdesc,cid=cid, createdat=datetime.datetime.now(),mdocs=mdoc)
            data.save()
            text='Materials added successfully'
            messages.success(request, text) 
            # return HttpResponse("work")

            return redirect('taddmaterials.html',context)                                                    
    else:        
        return redirect('/tlogin')
 
def tmaterials(request):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="GET":
            tid=context['tid']
            data=models.material.objects.filter(tid=tid).exists()       
            if data is False :
                data=None
                print('no data found')
                context={'name':context['name'],'tid':context['tid'],'data':data}                 
                return render(request,'materials/tmaterials.html',context)
            else:
                data=models.material.objects.filter(tid=tid).values()                     
                print(data)
                context={'name':context['name'],'tid':context['tid'],'data':data}                
                return render(request,'materials/tmaterials.html',context)
    else:
        return redirect("/teacher/")   

def deleteMaterial(request,mid):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="GET":
            models.material.objects.filter(mid=mid).delete()
            text='Material Deleted Successfully'
            messages.success(request, text) 
            return redirect('/teacher/tmaterials.html',context)
    else:
        return redirect("/teacher/") 

def updatepostmaterials(request):
    if request.session.has_key('tloginsuccess') :
        if request.method=="POST":  
            context=request.session['context']                  
            print(context)           
            cid=request.POST['courseName']  
            print("cis=", cid)      
            mid=request.POST['midval']
            print("mid=", mid)                       
            mtitle=request.POST['materialTitle']
            mdesc=request.POST['materialDescription']                        
            tid=context['tid']                        
            mdoc = request.FILES['mydoc'] if 'mydoc' in request.FILES else None      
            fileurl=None
            if 'mydoc' in request.FILES:
                mdocname=str(mid)+ mdoc.name
                fs= FileSystemStorage()
                file = fs.save(mdocname, mdoc) 
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed. 
                fileurl = fs.url(file)                
                # print('last mid',mid.mid)                        
                print('file url',fileurl,'dovumentname=',mdocname)                     
                # return HttpResponse('waiy')                                       
            data=models.material.objects.filter(mid=mid).update(mid=mid,tid=tid,mtitle=mtitle,mdecription=mdesc,cid=cid, createdat=datetime.datetime.now(),mdocs=fileurl)
            
            text='material updated successfully'
            messages.success(request, text) 
            # return HttpResponse("work")

            return redirect('/teacher/taddmaterials.html',context)                                                    
    else:        
        return redirect('/')


def updateMaterials(request,mid):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="GET":              
            courses=models.tcourse.objects.all()          
            data=list(models.material.objects.filter(mid=mid).values())
            context['cnames']=data  
            print('context names stored data',context['cnames'])        
            context['courses']=courses            
            return render(request,'materials/updatematerial.html',context)        
        
    else:        
        return redirect('/')
# course        =============================================================================   =============================================================================  
def detailedCourse(request,cid):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="GET":
            tid=context['tid']
            data=models.material.objects.filter(tid=tid,cid=cid).values()
            context={'name':context['name'],'tid':context['tid'],'data':data}                
            return render(request,'materials/tmaterials.html',context)  
    else:
        return redirect('/tlogin')


def AddCourse(request):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="GET":
            return render(request,'course/taddcourse.html',context)        
        if request.method=="POST":                
            print(context)           
            cname=request.POST['coursename']
            cdesc=request.POST['coursedescription']
            tid=context['tid']
            print(tid,"coursename",cname,"dec",cdesc)
            data=models.tcourse(tid=tid,cinfo=cdesc,cname=cname)
            data.save()
            text='course added successfully'
            messages.success(request, text) 
            # return HttpResponse("work")
            return redirect('tcourse.html',context)                                                    
    else:
        return redirect('/tlogin')

def ViewCourse(request):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="GET":
            tid=context['tid']
            data=models.tcourse.objects.filter(tid=tid).exists()       
            if data is False :
                data=None
                print('no data found')
                context={'name':context['name'],'tid':context['tid'],'data':data}  
                
                return render(request,'course/tcourse.html',context)        
            else:
                data=models.tcourse.objects.filter(tid=tid).values()     
                print('mydata')
                print(data)
                context={'name':context['name'],'tid':context['tid'],'data':data}                
                return render(request,'course/tcourse.html',context)
    else:
        return redirect("/teacher/")


def updateGetCourse(request,cid):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="GET":                                       
            data=models.tcourse.objects.filter(cid=cid).values()
            context['cname']=data
            print(data)
            return render(request,'course/tupdatecourse.html',context)                           
    else:        
        return redirect('/')


def updatePostCourse(request):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="POST":                                         
            cid=request.POST['cidval']
            cname=request.POST['courseTitle']
            cdec=request.POST['courseDescription']                            
            models.tcourse.objects.filter(cid=cid).update(cname=cname,cinfo=cdec)
            text='Course Updated Successfully'
            messages.success(request, text) 
            return redirect('/teacher/tcourse.html',context)        
                   
    else:        
        return redirect('/')

def deleteCourse(request,cid):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="GET":
            models.tcourse.objects.filter(cid=cid).delete()
            models.material.objects.filter(cid=cid).delete()
            text='Course Deleted Successfully'
            messages.success(request, text) 
            return redirect('/teacher/tcourse.html',context)
    else:
        return redirect("/teacher/") 

#attendance part=============================================================================

def attendancecourses(request):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="GET":
            tid=context['tid']
            data=models.tcourse.objects.filter(tid=tid).exists()       
            if data is False :
                data=None
                print('no data found')
                context={'name':context['name'],'tid':context['tid'],'data':data}  
                
                return render(request,'course/tcourse.html',context)        
            else:
                data=models.tcourse.objects.filter(tid=tid).values()     
                print('mydata')
                print(data)
                context={'name':context['name'],'tid':context['tid'],'data':data}                
                return render(request,'attendance/attendancecourses.html',context)
    else:
        return redirect("/teacher/")



def viewattendance(request,cid):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="GET":
            data=models.tcourse.objects.raw( "SELECT * FROM `studentsportal_studentlogin` JOIN studentsportal_scourse ON studentsportal_studentlogin.Sid=studentsportal_scourse.sid WHERE studentsportal_scourse.cid=%s ORDER BY studentsportal_studentlogin.Sid ",[cid])
            for d in data:
                print(d.first_name)
            if not data:                
                data=None 
            context['students']=data
            print(datetime.datetime.today().date())
            courseinfo=models.tcourse.objects.filter(cid=cid).values()
            context['courses']=courseinfo            
            return render(request,'attendance/studentsattendance.html',context)
    else:
        return redirect("/teacher/") 

def attendance(request):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="POST":
            cid=request.POST['cid']
            tid=context['tid']
            
            today=request.POST['date']
            if(today==""):
                today=datetime.datetime.today().date()
            print("date",today)

            data=models.attendance.objects.filter(date=today,cid=cid).exists()
            data=models.attendance.objects.raw('SELECT * FROM `teachersportal_attendance` WHERE teachersportal_attendance.cid=%s AND teachersportal_attendance.date=%s',[cid,today])
            studdata=smodel.scourse.objects.filter(cid=cid)
            print("student data=",studdata)            
            for student in data:
                print(" student sid",student.sid)
            
            if data :
                for student in studdata:
                    present=request.POST[str(student.sid)]
                    models.attendance.objects.filter(cid=cid,sid=student.sid,date=today).update(present=present)
                    

            else:
                for student in studdata :
                    print(student.sid)
                    present=request.POST[str(student.sid)]
                    data=models.attendance(sid=student.sid,cid=cid,tid=tid,present=present,date=today)
                    data.save()

            text="attendance recorded"
            messages.success(request,text)
            return redirect('/teacher/attendancecourses.html',context)
    else:
        return redirect("/teacher/") 


def fullattendance(request,cid):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="GET":
            cid=cid
            
            studdata=smodel.scourse.objects.filter(cid=cid)
            data=models.attendance.objects.raw('SELECT   DISTINCT(date) ,id FROM `teachersportal_attendance` WHERE cid=%s ORDER BY date ASC',[cid])           
            dict={}            
            for student in studdata:
                li=[]
                print("list type",type(li))
                for d in data:
                    stdexist=models.attendance.objects.raw('SELECT present,id FROM `teachersportal_attendance` WHERE cid=%s AND sid=%s AND date=%s',[str(cid),str(student.sid),str(d.date)])
                    if not stdexist:
                        li.append(0)
                    else:
                        temp=0
                        for i in stdexist:
                            if(i.present==1):
                                temp=1
                            else:
                                temp=0                            
                        li.append(temp)
                    print(str(d.date))
                dict[str(student.sid)]=li
            print(dict)
            context['attendanceinfo']=dict
            context['dates']=data
            context['studdata']=studdata          
            return render(request,'attendance/fullreprtattendance.html',context)  
            return HttpResponse('fullatendance',context)          
    else:
        return redirect("/teacher/")     




def Upadateattendance(request,cid,date):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="GET":
            date=date
            data=models.tcourse.objects.raw( "SELECT studentsportal_studentlogin.Sid ,teachersportal_tcourse.cid , studentsportal_studentlogin.first_name,studentsportal_studentlogin.last_name,teachersportal_attendance.present ,teachersportal_attendance.date FROM `teachersportal_attendance` JOIN studentsportal_studentlogin on teachersportal_attendance.sid=studentsportal_studentlogin.Sid join teachersportal_tcourse on teachersportal_tcourse.cid=teachersportal_attendance.cid WHERE teachersportal_attendance.cid=%s AND teachersportal_attendance.date=%s",[cid,date])
            for d in data:
                print(d.first_name)
            if not data:                
                data=None 
            context['students']=data
            print(datetime.datetime.today().date())
            courseinfo=models.tcourse.objects.filter(cid=cid).values()
            context['courses']=courseinfo
            context['date']=date            
            return render(request,'attendance/updateattendance.html',context)
   


#assignment part=============================================================================      
def taddassignment(request):
    context=request.session['context']
    return render(request,'assignment/taddassignment.html',context)  

def tViewAssignment(request):
    context=request.session['context']
    return render(request,'assignment/taddassignment.html',context)  



def temppost(request):
    if request.session.has_key('tloginsuccess') :
        context=request.session['context']
        if request.method=="GET":
            data=smodel.Studentlogin.objects.raw()
            
            return redirect('/teacher/tcourse.html',context)
    else:
        return redirect("/teacher/") 
   
# Create your views here.
