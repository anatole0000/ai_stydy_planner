from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from planner.models import Schedule  # Import the Schedule model
from .models import StudySession
from collections import Counter
from .ai import recommend_topic
from django.http import HttpResponse
from datetime import date
from .models import Schedule
from django.db.models import Sum
from django.utils.timezone import now
import datetime
from .models import Profile
from .models import Friendship
from .models import ActivityFeed

# Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            messages.success(request, "Registration successful!")
            return redirect('dashboard')  # Redirect to the dashboard after login
        else:
            messages.error(request, "There was an error in your registration.")
    else:
        form = UserCreationForm()
    return render(request, 'planner/register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')  # Redirect to the dashboard after login
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'planner/login.html', {'form': form})

# Profile View

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.bio = request.POST['bio']
        profile.profile_picture = request.FILES.get('profile_picture', profile.profile_picture)
        profile.save()
        return redirect('profile')  # Redirect to profile page after saving

    return render(request, 'planner/profile.html', {'profile': profile})

# Logout View
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to login page after logout

@login_required
def dashboard(request):
    user = request.user
    
    # Get all schedules for the user
    user_schedule = Schedule.objects.filter(user=user)
    today_schedule = user_schedule.filter(date=date.today())
    
    # Get all study sessions for the user
    study_sessions = StudySession.objects.filter(user=user)
    
    # Calculate total study time
    total_study_time = sum(session.study_time for session in study_sessions)
    
    # Define a study goal (e.g., 500 minutes)
    study_goal = 500
    
    # Calculate progress percentage
    progress_percentage = (total_study_time / study_goal) * 100 if study_goal > 0 else 0
    
    # Get AI recommendation for study topic
    suggestion = recommend_topic(user)
    if not suggestion:
        suggestion = "Keep up the momentum! Try studying more."
    
    return render(request, 'planner/dashboard.html', {
        'user_schedule': user_schedule,
        'today_schedule': today_schedule,
        'suggestion': suggestion,
        'recommendations': suggestion,
        'total_study_time': total_study_time,
        'study_goal': study_goal,
        'progress_percentage': progress_percentage,
    })


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect to the dashboard if logged in
    return render(request, 'planner/home.html')  # Render homepage if not logged in

@login_required
def create_schedule(request):
    if request.method == 'POST':
        # Get the data from the form
        topic = request.POST.get('topic')
        date = request.POST.get('date')
        estimated_time = request.POST.get('estimated_time')

        # Create and save the schedule
        schedule = Schedule.objects.create(
            user=request.user,  # Assuming the Schedule model has a user field
            topic=topic,
            date=date,
            estimated_time=estimated_time
        )

        add_activity(request.user, f"Created a new study schedule for {topic}")

        # Redirect to the newly created schedule's detail page or the dashboard
        return redirect('schedule_detail', schedule_id=schedule.id)

    return render(request, 'planner/create_schedule.html')

@login_required
def schedule_detail(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    return render(request, 'planner/schedule_detail.html', {'schedule': schedule})


@login_required
def recommend_study_time(request):
    # Fetch the user's past study sessions
    past_sessions = StudySession.objects.filter(user=request.user)
    
    if not past_sessions:
        return render(request, 'planner/no_sessions.html')  # If no sessions, show a message
    
    # Calculate the average study time across all sessions
    total_time = sum(session.study_time for session in past_sessions)
    total_sessions = past_sessions.count()
    average_study_time = total_time / total_sessions
    
    # Recommend the same average time for a new session (you can modify this logic later)
    recommended_time = round(average_study_time)
    
    return render(request, 'planner/study_recommendation.html', {'recommended_time': recommended_time})

def test_ai(request):
    suggestion = recommend_topic(request.user)
    return HttpResponse(f"AI Suggestion: {suggestion}")

from django.shortcuts import render
from .models import StudySession

def analytics(request):
    user = request.user  # Get the currently logged-in user
    
    # Get all study sessions for the user
    study_sessions = StudySession.objects.filter(user=user)
    
    # Calculate total study time for the user
    total_study_time = sum(session.study_time for session in study_sessions)
    
    # Define your study goal (e.g., 500 minutes)
    study_goal = 500
    
    # Calculate the progress percentage
    progress_percentage = (total_study_time / study_goal) * 100 if study_goal > 0 else 0
    
    # Pass data to the template
    return render(request, 'planner/analytics.html', {
        'study_sessions': study_sessions,
        'total_study_time': total_study_time,
        'study_goal': study_goal,
        'progress_percentage': progress_percentage,
        'user': user,  # Pass the user data to the template
    })

@login_required
def follow_user(request, user_id):
    friend = User.objects.get(id=user_id)
    
    if not Friendship.objects.filter(user=request.user, friend=friend).exists():
        Friendship.objects.create(user=request.user, friend=friend)
    
    return redirect('profile')  # Redirect to profile page after following

@login_required
def unfollow_user(request, user_id):
    friend = User.objects.get(id=user_id)
    Friendship.objects.filter(user=request.user, friend=friend).delete()
    return redirect('profile')  # Redirect to profile page after unfollowing

def add_activity(user, action):
    ActivityFeed.objects.create(user=user, action=action)

# Example usage in the schedule creation view


@login_required
def update_profile(request):
    if request.method == "POST":
        bio = request.POST['bio']
        profile_picture = request.FILES.get('profile_picture', None)
        
        # Update profile
        request.user.profile.bio = bio
        if profile_picture:
            request.user.profile.profile_picture = profile_picture
        request.user.profile.save()

        # Log the profile update activity
        add_activity(request.user, "Updated profile")

        return redirect('profile')

    return render(request, 'planner/update_profile.html')
