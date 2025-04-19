from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create_schedule/', views.create_schedule, name='create_schedule'),
    path('schedule/<int:schedule_id>/', views.schedule_detail, name='schedule_detail'),
    path('recommend_study_time/', views.recommend_study_time, name='recommend_study_time'),
    path('test-ai/', views.test_ai, name='test_ai'),
    path('analytics/', views.analytics, name='analytics'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
]
