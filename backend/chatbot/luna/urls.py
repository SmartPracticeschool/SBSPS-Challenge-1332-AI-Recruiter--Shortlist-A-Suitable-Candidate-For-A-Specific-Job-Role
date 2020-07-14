from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.render_home, name='luna-home'),
    path('botpage/',views.render_botpage,name='luna-bot-welcome'),
    path('botpage/login/',auth_views.LoginView.as_view(template_name='luna/login.html'),name='luna-bot-login'),
    path('botpage/signup/',views.render_signup,name='luna-bot-signup'),
    path('botpage/logout/',views.render_logout,name='logout'),
    path('botpage/welcome',views.render_welcome,name='profile'),
    path('botpage/upload',views.render_upload,name='upload'),
   
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    