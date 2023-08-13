from django import forms
from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse, HttpRequest
from django.urls import reverse
from Authentication.form import Register, Login
from User.models import Author
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_


def register(request: HttpRequest):
    """
    Request method will be post if we pressed submit in the register.html file
    
    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML template.
    """
    
    # prints the description of the request method
    requestMethodData(request) 
    
    if request.method == 'POST':
        authorRegisterForm = Register(request.POST) # Creating a Register form instance with the data passed from html in request.POST 
        requestMethodData(request)
        
        if authorRegisterForm.is_valid():

            # Retrieving the user name from the form data
            retrievedUsername = authorRegisterForm.cleaned_data['Username'] 
                
            # Retrieving the Author data from the form 
            retrievedPassword = authorRegisterForm.cleaned_data['password']
            retrievedEmail = authorRegisterForm.cleaned_data['email']
            retrievedAge = authorRegisterForm.cleaned_data['age']
            retrievedPhoneNo = authorRegisterForm.cleaned_data['phoneNo']


            # if the username already exists, send a context the html file so the user can seen it
            if  Author.objects.filter(name = retrievedUsername).count()  >= 1:
                return render (request, 'register.html', {
                    'userNameDuplicate' : True,
                    'inputEmail': retrievedEmail,
                    'inputPassword': retrievedPassword,
                    'inputPhone' : retrievedPhoneNo,
                    'inputAge' : retrievedAge
                    })
                #raise forms.ValidationError('This username already exists, try a different one!')

            # Creating a new user object of user model 
            newUser = User.objects.create_user(username = retrievedUsername, email = retrievedEmail, password = retrievedPassword)

            # Creating a new Author object and adding it to database
            Author.objects.create (
                user = newUser,
                name = retrievedUsername,
                age = retrievedAge,
                email = retrievedEmail,
                password = retrievedPassword,
                phoneNo = retrievedPhoneNo  
            )

            return redirect("UserLogin")
            
    return render(request, 'register.html',{'result' : 'user Created'} )


def login (request: HttpRequest):
    """
    View for user login.
    
    Args:
        request (HttpRequest): The HTTP request object.
        
    Returns:
        HttpResponse: Rendered HTML template or redirect to createBlog page if user has logged in succssefulyy
    """
    requestMethodData(request)
    # if request.user.is_authenticated:
    #     return redirect(reverse('home'))

    if request.method == 'POST':

        # Creating a Login form object and passing it the post request method data
        authorLogInForm = Login(request.POST)   

        if authorLogInForm.is_valid():

            # Retrieving data from the authorLogInForm form
            retrievedUsername = authorLogInForm.cleaned_data['Username']
            retrievedPassword = authorLogInForm.cleaned_data['password']

            # attempting to authenticate the user with the provided username and password. If the authentication is successful,
            #  the user object will hold the authenticated user's information. If the authentication fails, user will be None. 
            # This is then used to determine whether the user can be logged in or not, as shown in the next line with the login_ function call.
            user = authenticate(request, username = retrievedUsername, password = retrievedPassword)

            if user:
                # login_: a function provided by Django's authentication system. It's used to log in a user after they've been authenticated. The function takes two arguments: the request 
                login_(request, user)

                return redirect(reverse('createBlog'))
            
            else:
                return render (request, 'login.html', {
                    'userFound' : False,                   
                    })
                raise forms.ValidationError("This username is doesn't exist! ")

        else: 
            return render(request, 'login.html', { 'errors' : str(authorLogInForm.errors)})

    return render (request, 'login.html', {'result' : ''})


def requestMethodData (request):
    
    print(f"\n\n\t Request method name: {request.method} ")
    print(f"\n\n\t Request bode: {request.body} ")
    print(f"\n\n\t Request {request} ")

    if request.method == 'POST':
        print(f"\n\n\t POST request: {request.POST} \n\n")

    elif request.method == 'GET':
        print(f"\n\n\t GET request: {request.GET} \n\n")


    

