from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control
from django.contrib import messages
# Create your views here.

#to make it dont go backward
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def HomePage(request):
    if 'username' in request.session:
        return render (request,'home.html')
    else:
        return redirect('login')
    
#coming from the urls when calling views.signuppage
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def SignupPage(request):
    if 'username' in request.session:
        return redirect('home')
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            messages.error(request,'password you re-entered is incorrect')
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
    # first loading this signup.html page
    return render(request,'signup.html')


#to make it dont go backward use this annotation
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Loginpage(request):
    if 'username' in request.session:
        return redirect('home')
    
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        print(user)
        if user is not None:
            login(request,user)
            request.session['username']=username
            return redirect('home')
        else:
            messages.error(request,'username or password is incorrect')
    return render(request,'login.html')


#coming from the urls when calling views.logoutpage
def LogoutPage(request):
    if 'username' in request.session:
        logout(request)
        request.session.flush()
    return redirect('login')
