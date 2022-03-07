"""sharemyspace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myfunction import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',indexpage),
    path('home', home),
    path('inputadmin',inputadmin),
    path('addadmin',addadmin),
    path('viewadmin',viewadmin),
    path("edit",editadmin),
    path("delete",removeadmin),
    path('save',save),
    path('login',login),
    path('checklogin',checklogin),
    path('checklogin2',checklogin2),
    path('landing',landing),
    path('addnews',addnews),
    path('insertnews',insertnews),
    path('viewnews',viewnews),
    path('viewpublicnews',viewpublicnews),
    path('deletenews',removenews),
    path('editnews',editnews),
    path('deleteuser',removeuser),
    path('savenews',savenews),
    path('openchangepass', openchangepass),
    path('changepassword', changepassword),
    path('openchangeuserpass', openchangeuserpass),
    path('changeuserpassword', changeuserpassword),
    path('logout',logout),
    path('logoutuser',logoutuser),
    path('signup',signup),
    path('insertuser',insertuser),
    path('userlogin',userlogin),
    path('viewuser',viewuser),
    path('viewuserprofile',viewuserprofile),
    path('addcategory',addcategory),
    path('insertcategory',insertcategory),
    path('viewcategory',viewcategory),
    path('removecategory',removecategory),
    path('editcategory',editcategory),
    path('savecategory',savecategory),
    path('addroom',addroom),
    path('insertroom',insertroom),
    path('viewroom',viewroom),
    path('removeroom',removeroom),
    path('editroom',editroom),
    path('saveroom',saveroom),
    path('EditPhoto',editphoto),
    path('searchroom',searchroom),
    path('getallcityname',getallcityname),
    path('roomsearchaction',roomsearchaction),
    path('roomdetail',roomdetail),
    path('bookingpage',bookingpage),
    path('bookingaction',bookingaction),
    path('checkavailability',checkavailability),
    path('confirmbooking',confirmbooking),
    path('mybooking',mybooking),
    path('addReview',addReview),
    path('showReviews',showReviews),
    path('feedback',feedback),
    path('ajax_avg_rating',ajax_avg_rating),
    path('ajax_addrating',ajax_addrating),
    path('ratingdemo',ratingdemo),
]
