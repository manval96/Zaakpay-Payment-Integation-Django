from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
# Create your views here.
def register(request):
    
    if request.method == 'POST':
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password']
        password2 = request.POST['re_password']
        email = request.POST['email']
        
        details = [first_name, last_name, username, password1, password2, email]
        for item in details:
            if item is '':
                messages.error(request, 'Please fill all the details')
                return redirect('register')
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                #print('Username already in use')
                messages.error(request, 'username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                #print('email taken')
                messages.error(request, 'email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name,last_name=last_name)
                user.save();
                #print('user created')
                messages.info(request, 'user created')
                return redirect('login')
            
        else:
            messages.error(request, 'password not matching')
            return redirect('register')
        #return redirect('/')
    else:   
        return render(request, 'register.html')

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else:
        
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')