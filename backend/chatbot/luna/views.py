from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.template.context import RequestContext
from .parser import parser
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
# Create your views here.
from django.contrib import messages


def render_home(request):
    return render(request,'luna/index.html')

def render_botpage(request):
    logout(request)
    return render(request,'luna/greet.html')



def render_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
                login(request, user)
                return HttpResponseRedirect('/profile.html')
     
        else:
            state = "Your email and/or password were incorrect."

        state = "Please log in below..."

    context = RequestContext(request, {
        'state': state   })
    return render('luna/login.html',{},context)

@login_required
def render_welcome(request):
    return render(request,'luna/profile.html')    



def render_signup(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile')
        
            
    else:
        form=UserRegisterForm()
    return render(request,'luna/signup.html',{'form':form})

@login_required
def render_upload(request):
    if request.method=='POST':
        uploaded_file=request.FILES['document']
        fs=FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        parsed_text = parser.extract_data(os.path.join(settings.MEDIA_ROOT, uploaded_file.name))
        res_name=parser.extract_name(parsed_text)
        res_email=parser.extract_email(parsed_text)
        res_skills=parser.extract_skills(parsed_text)
        
        res_mobile=parser.extract_mobile_number(parsed_text)
        res_ed=parser.extract_education(parsed_text)
        
        edus={
             'BE':'Bachelors in Engineering',
             'B.E.':'Bachelors in Engineering', 
             'B.E.':'Bachelors in Engineering', 
             'BE':'Bachelors in Engineering',
             'BS':'Bachelors in Science', 
             'B.S':'Bachelor in Science', 
             'ME':'Masters in Engineering',
             'M.E':'Masters in Engineering',
             'M.E.':'Masters in Engineering',
             'MS':'Masters in Science', 
             'M.S':'Masters in Science', 
             'BTECH':'Bachelors in Technology', 
             'B.TECH':'Bachelors in Technology',
             'M.TECH':'Masters in Technology',
             'MTECH':'Masterss in Technology', 
             'SSC':'Senio Secondary',
             'HSC':'Higher Secondary', 
             'CBSE':'CBSE',
             'ICSE':'ICSE',
             'X':'X',
             'XII':'XII'
        }
       
        aux_ed=''
        for x in res_ed:
            if edus[x] is not None:
                aux_ed+=' '+ edus[x]
        aux_skills=''
        for x in res_skills:
            aux_skills+=' | '+x
        aux_skills+=' |'
        aux_exp=' '
        
        res_exp=parser.extract_experience(parsed_text)
        for x in res_exp:
            aux_exp+=' '+x
        messages.success(request,'Resume Uploaded')
        context={
            'name':res_name,
            'email':res_email,
            'skills':aux_skills,
            'education':aux_ed,
            'mobile':res_mobile,
            'experience':aux_exp,
        }
        
        return render(request,'luna/profile.html',context)
        
        
    return render(request,'luna/upload.html')
        
def render_logout(request):
    logout(request)
    return render(request,'luna/greet.html')
    
    





    