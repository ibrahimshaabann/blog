from django import forms
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from MyBlogs.forms import Blog_create, Blog_update
from User.models import Author, Blog 
from django.contrib.auth import authenticate, logout as logout_
from datetime import datetime


def home(request):
    """
    Display the home page with all blogs ordered by the newest creation date.

    Returns:
        HttpResponse: Rendered HTML template.
    """
    try:
        allBlogsList = Blog.objects.all().order_by('-creationDate') # order blogs by the newest date
    except Exception as e:
        print(f"Error in retrieving Blog objects: {e}")
    
    return render(request, 'home.html', {'AllBlogs': allBlogsList})


def logout(request):
    """
    Log out the user and redirect to the home page.

    Returns:
        HttpResponse: Redirect to the home page.
    """
    try:
        logout_(request)
        return redirect (reverse('home'))
    except Exception as e:
        print(f"Error in logout: {e}")


def createBlog(request:HttpRequest):
    """
    Create a new blog object and add it to user blogs

    Returns:
        HttpResponse (one of Http responses is an html file): Rendered HTML template --> createBlog.html or
        Redirect to myBlogs page if we sent post request 
    """

    if request.method == 'POST':
        createBlog_form = Blog_create(request.POST,request.FILES)
        loggedUser = request.user
        
        if not loggedUser:
            raise forms.ValidationError('User is not Retrieved!')
        
        print(request.POST) #

        # is_valid() checks if the form contains any missed or invalid information  
        if createBlog_form.is_valid():
            # Extreact data from the form
            retrievedTitle = createBlog_form.cleaned_data['title']
            retrievedContent = createBlog_form.cleaned_data['content']
            retrievedcreationDate = datetime.now()
            retrievedImg = request.FILES.get('img')

            # Get the logged in user's user name and author objct
            loggedInUsername = request.user.username # Getting the user who is logeed in
            author = Author.objects.get(name = loggedInUsername)
            
            # Create a new Blog object
            Blog.objects.create(
                author_id = author,
                title = retrievedTitle,
                content = retrievedContent,
                img = retrievedImg,
                creationDate = retrievedcreationDate
                )
            
        # This return value will be excuted if the request.method is POST method
        return redirect(reverse('myBlogs'))

    # This return value is excuted if we have not sent a post request yet ----> post request is triggerd by pressing the share button in createBlog.html
    return render(request, 'createBlog.html', { 'result' : '' })

    
def updateBlog(request:HttpRequest, blog_id):
    """
    Update an existing blog object 

    Args:
        request (HttpRequest): The HTTP request object.
        blog_id (int): The ID of the blog to be updated sent from HTML.

    Returns:
        HttpResponse: Rendered HTML template or redirect to myBlogs page.
    """
    # print(Blog.objects.filter(id = blog_id).values())
    blog = Blog.objects.get(id = blog_id)
    
    if request.method == 'POST':
        updateBlog_form = Blog_update(request.POST, request.FILES)
        
        if updateBlog_form.is_valid():
            
            # Update the blog object with the new data
            retrievedUpdateDate = datetime.now()
            blog.content =  updateBlog_form.cleaned_data['content']
            blog.title =  updateBlog_form.cleaned_data['title']
            blog.creationDate =  retrievedUpdateDate
            retrievedImg = request.FILES.get('img')
            
            # if there is an image retrieved from request.Files, update the blog object image.
            if retrievedImg != None:
                blog.img = retrievedImg

            # Saving the blog object to database
            blog.save()
            # print(blog.content)

        else:
            return forms.ValidationError(str(updateBlog_form.errors))

        return redirect(reverse('myBlogs'))
        
    return render(request, 'updateBlog.html', {'blogToUpdate': blog, })


def deleteBlog(request:HttpRequest,blog_id):
    """
    Delete an existing blog object
    """
    Blog.objects.filter(id = blog_id).delete()
    return redirect(reverse("myBlogs"))
        

def showMyBlogs(request:HttpRequest):


    """
    Display the blogs created by the logged-in user
    """

    # Retrieveing the logged-in user
    user = request.user
    
    author = Author.objects.get(user = user)
    BlogsList = Blog.objects.filter(author_id = author).order_by('-creationDate')
    return render(request, 'myBlogs.html', {'myBlogsList': BlogsList})


def allBlogs(request: HttpRequest):
    """
    Display the home page with all blogs ordered by the newest creation date.

    Returns:
        HttpResponse: Rendered HTML template.
    """
    try:
        allBlogsList = Blog.objects.all().order_by('-creationDate') # order blogs by the newest date
    except Exception as e:
        print(f"Error in retrieving Blog objects: {e}")
    
    return render (request,'AllBlogs-user.html', {'AllBlogs':allBlogsList })



