from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileForm, ListingForm, ListingSearchForm
from .models import Listing, Category, Profile

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'marketplace/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'marketplace/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    featured_listings = Listing.objects.all()[:6]  # Get first 6 listings
    categories = Category.objects.all()
    return render(request, 'marketplace/home.html', {
        'featured_listings': featured_listings,
        'categories': categories
    })

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'marketplace/profile.html', {'form': form})

def listing_list(request):
    form = ListingSearchForm(request.GET)
    listings = Listing.objects.all()
    if form.is_valid():
        if form.cleaned_data['query']:
            listings = listings.filter(title__icontains=form.cleaned_data['query'])
        # Add more filters as needed
    return render(request, 'marketplace/listing_list.html', {
        'listings': listings,
        'form': form
    })

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'marketplace/listing_detail.html', {'listing': listing})

@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            form.save_m2m()
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, 'marketplace/listing_form.html', {'form': form})

@login_required
def listing_edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'marketplace/listing_form.html', {'form': form})

@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if request.method == 'POST':
        listing.delete()
        return redirect('listing_list')
    return render(request, 'marketplace/listing_delete.html', {'listing': listing})

def support(request):
    return render(request, 'marketplace/support.html')

def faq(request):
    return render(request, 'marketplace/faq.html')
