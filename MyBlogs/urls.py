from django.urls import path
from MyBlogs.views import home ,createBlog, updateBlog, deleteBlog, showMyBlogs, logout, allBlogs



urlpatterns = [
    path('', home, name = 'home'),
    path('MyBlogs/createBlog/', createBlog, name = 'createBlog'),
    path('updateBlog<int:blog_id>/', updateBlog, name = 'updateBlog'),
    path('deleteBlog/<int:blog_id>/', deleteBlog, name = 'deleteBlog'),
    path('showMyBlogs/', showMyBlogs, name = 'myBlogs'),
    path('logout/', logout, name = 'logout'),
    path('allBlogs/', allBlogs, name = 'allBlogs')
]