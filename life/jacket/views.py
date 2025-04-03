from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, TravelPost, Review, Location
from .forms import UserRegistrationForm, LoginForm, TravelPostForm, ReviewForm, LocationForm
from django.db.models import Q
from .forms import SearchForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    travel_posts = TravelPost.objects.all().order_by('-posted')
    return render(request, 'home.html', {'travel_posts': travel_posts})

@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = TravelPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = TravelPostForm()
    
    return render(request, 'create_post.html', {'form': form})

@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(TravelPost, id=post_id)
    reviews = Review.objects.filter(travel_post=post).order_by('-posted')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user_id = request.user
            review.travel_post = post
            review.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = ReviewForm()
    
    return render(request, 'post_detail.html', {
        'post': post, 
        'reviews': reviews,
        'form': form
    })

@login_required
def create_location_view(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = LocationForm()
    
    return render(request, 'create_location.html', {'form': form})

@login_required
def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = TravelPost.objects.filter(user=user).order_by('-posted')
    reviews = Review.objects.filter(user_id=user).order_by('-posted')
    
    return render(request, 'user_profile.html', {
        'profile_user': user,
        'posts': posts,
        'reviews': reviews
    })

def search_view(request):
    query = request.GET.get('query', '')
    search_type = request.GET.get('search_type', 'all')
    
    results = {
        'users': [],
        'posts': [],
        'locations': []
    }
    
    if query:
        # Search users
        if search_type in ['all', 'users']:
            users = User.objects.filter(
                Q(username__icontains=query) | 
                Q(name__icontains=query)
            )
            results['users'] = users
        
        # Search posts
        if search_type in ['all', 'posts']:
            posts = TravelPost.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            )
            results['posts'] = posts
        
        # Search locations
        if search_type in ['all', 'locations']:
            locations = Location.objects.filter(
                Q(location_name__icontains=query) | 
                Q(district__icontains=query) | 
                Q(nearest_railway_station__icontains=query) | 
                Q(nearest_airport__icontains=query)
            )
            results['locations'] = locations
    
    form = SearchForm(initial={'query': query, 'search_type': search_type})
    
    return render(request, 'search_results.html', {
        'form': form,
        'query': query,
        'results': results,
        'search_type': search_type
    })