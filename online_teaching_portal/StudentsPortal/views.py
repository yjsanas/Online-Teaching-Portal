from django.shortcuts import render,redirect
from django.http import HttpResponse
from  . import models
from  TeachersPortal import models as tmodel
from django.contrib.auth.models import User, auth
from django.contrib import messages

def Logout(request):
    del request.session['context']
    del request.session['sloginsuccess']
    return render(request,'login/login.html')
    

def Login(request):    
    if request.session.has_key('sloginsuccess') :
        context=request.session['context']
        return render(request,'home/home.html',context)
        
    if request.method=="POST":
        emailid=request.POST['inputEmailAddress']
        ipassword=request.POST['inputPassword']            
        data=models.Studentlogin.objects.filter(email=emailid,password=ipassword).exists()
        print(data)
        if data is True:
            sdata=models.Studentlogin.objects.get(email=emailid,password=ipassword)
            fname=sdata.first_name
            lname=sdata.last_name
            name=fname+' '+lname
            context={'name':name}
            context['sid']=sdata.Sid
            request.session['context']=context
            print('success')     
            request.session['sloginsuccess']=True            
            return render(request,'home/home.html',context)
        else:
            text="Invalid Credentials" 
            messages.error(request, text) 
            return render(request,'login/login.html')

        
    else:
        return render(request,'login/login.html')

def register(request):
    if request.method=="POST":    
        First_Name=request.POST['inputFirstName']
        sLast_Name=request.POST['inputLastName']
        emailid=request.POST['inputEmailAddress']
        spassword=request.POST['inputPassword']
        scpassword=request.POST['inputConfirmPassword']
        if(spassword == scpassword ):
            data=models.Studentlogin(first_name=First_Name,last_name=sLast_Name,email=emailid,password=spassword)
            data.save()
            return render(request,'login/login.html')
        else:
            text="password and confirm password not same"
            messages.error(request, text) 
            return render(request,'login/register.html')

        # data=models.Studentlogin.objects.all()
        # data=models.Studentlogin.objects.get(first_name='kartik')
        # print(data.first_name, data.email,data.last_name)
    else:
        return render(request,'login/register.html')

def home(request):
    if request.session.has_key('sloginsuccess') :
        context=request.session['context']
        return render(request,'home/home.html',context)
    else:
        return render(request,'login/login.html')

def temp(request):
    var= request.GET.get('t1')
    print(var)
    return HttpResponse(var)

def temppost(request):
    var= request.POST('t1')
    print(var)
    return  HttpResponse("Hello,this is the login page.")
# Create your views here.

# Student course 
def joincourse(request):
    if request.session.has_key('sloginsuccess') :
        context=request.session['context']
        sid=context['sid']
        if request.method=="POST": 
            cid=request.POST['joincourse']
            cidcheck=tmodel.tcourse.objects.filter(cid=cid).exists()
            if cidcheck == False:
                text="invalid course id"
                messages.error(request, text) 
                context={'name':context['name'],'sid':context['sid']}                
                return redirect("/students/slistcourse.html",context)
            joinexist=models.scourse.objects.raw("SELECT * FROM `studentsportal_scourse` WHERE `sid`=%s and`cid`=%s",[sid,cid])
            
            if joinexist:
                text="all ready registered"
                messages.error(request, text) 
            else:
                data=models.scourse(cid=cid,sid=sid)   
                data.save()  
                text='course added successfully'
                messages.success(request, text)                 
            context={'name':context['name'],'sid':context['sid']}                
            return redirect("/students/slistcourse.html",context)
    else:
        return redirect("/students/")
def unenrolcourse(request,cid):
    if request.session.has_key('sloginsuccess') :
        context=request.session['context']
        sid=context['sid']
        if request.method=="GET":             
            data=models.scourse.objects.filter(cid=cid,sid=sid).delete()               
            text='course unenrolled successfully'
            messages.success(request, text) 
            context={'name':context['name'],'sid':context['sid']}                
            return redirect("/students/slistcourse.html",context)
    else:
        return redirect("/students/")


def sviewmaterial(request,cid):
    if request.session.has_key('sloginsuccess') :
        context=request.session['context']
        if request.method =="GET":
            if models.scourse.objects.filter(cid=cid,sid=context['sid']).exists():
                data=tmodel.material.objects.filter(cid=cid).values()
                coursedata=tmodel.tcourse.objects.filter(cid=cid).values()
                context['courses']=coursedata
                context['data']=data
                return render(request,'scourse/coursematerials.html',context)
            else: 
                text="You are not enrolled in that course"
                messages.error(request, text) 
                context={'name':context['name'],'sid':context['sid']}                
                return redirect("/students/slistcourse.html",context)

    else:
        return render(request,'login/login.html')

def slistcourse(request):
    if request.session.has_key('sloginsuccess') :
        context=request.session['context']
        sid=context['sid']
        if request.method=="GET": 
            data=models.scourse.objects.raw("SELECT * FROM `teachersportal_tcourse` join studentsportal_scourse ON teachersportal_tcourse.cid=studentsportal_scourse.cid AND studentsportal_scourse.sid=%s",[sid])
            print(sid)
            for d in data:
                print(d.sid,d.cname,d.cinfo)
            print(data)  
            if not data:
                data=None              
            context={'name':context['name'],'sid':context['sid'],'data':data}                
            return render(request,'scourse/slistcourse.html',context)
    else:
        return redirect("/students/")



#materials
def smaterialinfo(request,cid,mid):
    if request.session.has_key('sloginsuccess') :
        context=request.session['context']
        if request.method =="GET":
            if models.scourse.objects.filter(cid=cid,sid=context['sid']).exists():
                data=tmodel.material.objects.filter(mid=mid).values()
                coursedata=tmodel.tcourse.objects.filter(cid=cid).values()
                context['courses']=coursedata
                context['cnames']=data
                return render(request,'materials/viewmaterial.html',context)
            else: 
                text="You are not enrolled in that course"
                messages.error(request, text) 
                context={'name':context['name'],'sid':context['sid']}                
                return redirect("/students/slistcourse.html",context)

    else:
        return render(request,'login/login.html')

def allmaterials(request):
    if request.session.has_key('sloginsuccess') :
        context=request.session['context']
        if request.method =="GET":            
            data=tmodel.material.objects.raw("SELECT * FROM `teachersportal_material` JOIN studentsportal_scourse ON studentsportal_scourse.cid=teachersportal_material.cid AND studentsportal_scourse.sid=%s",[context['sid']])           
            if not data:
                data=None            
            context['data']=data
            return render(request,'materials/allmaterials.html',context)
            
    else:
        return render(request,'login/login.html')

#attendance

def viewattendance(request):
    if request.session.has_key('sloginsuccess') :
        context=request.session['context']
        sid=context['sid']
        q=models.scourse.objects.none()
        if request.method=="GET":
            
            allcourse=tmodel.tcourse.objects.raw("SELECT teachersportal_tcourse.cid, teachersportal_tcourse.cname , COUNT(teachersportal_attendance.cid) AS total FROM `studentsportal_scourse` JOIN teachersportal_tcourse ON teachersportal_tcourse.cid=studentsportal_scourse.cid JOIN teachersportal_attendance ON teachersportal_attendance.cid=studentsportal_scourse.cid  where studentsportal_scourse.sid=%s GROUP BY teachersportal_attendance.cid",[sid])
            adddata=[]
            for course in allcourse:
                data=models.Studentlogin.objects.raw('SELECT teachersportal_attendance.id,studentsportal_studentlogin.Sid,  cid, studentsportal_studentlogin.first_name,studentsportal_studentlogin.last_name, SUM(present) as present FROM `teachersportal_attendance` JOIN studentsportal_studentlogin on studentsportal_studentlogin.Sid=teachersportal_attendance.sid WHERE teachersportal_attendance.sid=%s AND teachersportal_attendance.cid=%s',[sid,course.cid])
                
                for d in data:                    
                    temp=d.present
                adddatatemp={
                    'cid':course.cid,
                    'sub':course.cname,
                    'present':temp,
                    'totallec':course.total,
                }
                adddata.append(adddatatemp)
            print(adddata)
            context['attendance']=adddata
            
            return render(request,'attendance/viewattendance.html',context)
    else:
        return redirect("/students/") 


#genral structure
def temp1(request):
    if request.session.has_key('sloginsuccess') :
        context=request.session['context']
        sid=context['sid']
        if request.method=="GET":
            data=model.Studentlogin.objects.raw()
            
            return redirect('/teacher/tcourse.html',context)
    else:
        return redirect("/teacher/") 
   

