from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from . models import User

def index(request):
	return render(request, 'loginreg/index.html')

def register(request):
    if request.method == "POST":
        # print request
        request.session['firstname'] = request.POST['firstname']
        success, user_manager_response = User.objects.register(request.POST)
        print success
        print user_manager_response
        if success: # user registered
            print "success user registered"
            msg = "You have successfully registered and are currently logged in."
            messages.success(request, msg)
            return redirect('/success', msg)
        else:
            request.session['lastname'] = request.POST['lastname']
            request.session['email'] = request.POST['email']
            for error in user_manager_response:
                messages.error(request, error)
            return redirect('/')
    else: #request.method != POST
        return redirect('/')

def success(request):
    return render(request, "loginreg/success.html")

def show(request): #show existing users
    users = User.objects.all()
    print users
    context = {
        "users": users
    }
    return render(request, "loginreg/show.html", context)

def destroy(request, id):
    if request.method == "POST":
        action = User.objects.deleteuser(id)
        msg = "User deleted."
        messages.success(request, msg)
        # return redirect('/show')
        return redirect(review('show'))
    else: #request.method != POST
        return redirect('/')

def login(request):
    if request.method == "POST":
        print "in login"
        # email named differently to prevent automatic populating during register
        request.session['loginemail'] = request.POST['loginemail']
        success = User.objects.login(request.POST)

        if success == True: # login successful
            msg = "You are now logged in."
            messages.success(request, msg)
            return redirect('/success', msg)
        else: #errors
            request.session['msg'] = "Incorrect email address or password."
            return render(request, 'loginregistration/index.html')
    else: #request.method != POST
        return redirect('/')
