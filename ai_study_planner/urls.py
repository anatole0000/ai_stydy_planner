
from django.contrib import admin
from django.urls import path, include
from planner import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('planner/', include('planner.urls')),
]
