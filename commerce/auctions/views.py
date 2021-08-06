from typing import List
from django.contrib import messages
from django.contrib.messages.constants import SUCCESS
from auctions.forms import NewListing
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


from .models import Bid, Comment, User, Listing, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.exclude(closed=True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def newListing(request):
    form = NewListing(request.POST or None)
    if form.is_valid():
        listing = form.save(commit=False)
        listing.user = request.user
        form.save()
        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id':listing.id}))
    return render(request, "auctions/new.html", {
        'form': form
    })

def listing_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == 'POST':
        if 'close' in request.POST and request.user == listing.user and not listing.closed:
            listing.closed = True
            listing.save()
            messages.add_message(request, messages.SUCCESS, "You closed this Listing successfully!")
            return HttpResponseRedirect(reverse('listing', kwargs={'listing_id':listing_id}))
    comments = Comment.objects.filter(listing=listing)
    in_watchlist = False if not Watchlist.objects.filter(user=request.user, listing=listing) else True
    # current highest Bid or Starting Bid if no Bids exist
    latest_bid = Bid.objects.filter(listing=listing).latest('date') if Bid.objects.filter(listing=listing) else listing.starting_bid 
    if listing.closed and request.user == latest_bid.user:
        messages.add_message(request, messages.SUCCESS, "You Won This Auction!")
    return render(request, "auctions/listing.html", {
        'listing': listing,
        'comments': comments,
        'in_watchlist': in_watchlist,
        'latest_bid': latest_bid
    })

@login_required
def comment(request, listing_id):
    comment = Comment(comment=request.POST["comment"], user=request.user, listing=Listing.objects.get(id=listing_id))
    comment.save()
    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id':listing_id}))

@login_required
def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.user == listing.user:
        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id':listing_id}))
    bid_amount = float(request.POST['bid'])
    listing = Listing.objects.get(pk=listing_id)
    if request.user.is_authenticated and bid_amount >= listing.starting_bid:
        if((Bid.objects.filter(listing=listing) and not Bid.objects.filter(listing=listing, bid__gt=bid_amount)) or not Bid.objects.filter(listing=listing)):
            bid = Bid(listing=listing, bid=bid_amount, user=request.user)
            bid.save()
            messages.add_message(request, messages.SUCCESS, 'Your Bid was added successfully!')
            return HttpResponseRedirect(reverse('listing', kwargs={'listing_id':listing_id}))
    messages.add_message(request, messages.ERROR, 'Error: Your Bid was to low!')
    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id':listing_id}))

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.filter(user=request.user)
    })

@login_required
def add_to_watchlist(request, listing_id):
    item = Watchlist.objects.filter(user=request.user, listing=Listing.objects.get(pk=listing_id))
    if not item:
        watchlist = Watchlist(user=request.user, listing=Listing.objects.get(pk=listing_id))
        watchlist.save()
        return HttpResponseRedirect(reverse('watchlist'))
    else:
        item.delete()
        return HttpResponseRedirect(reverse("watchlist"))

def categories_view(request):
    return render(request, 'auctions/categories.html', {
        'categories': Listing.CATEGORIES
    })

def category_view(request, category):
    listings = Listing.objects.filter(category=category).exclude(closed=True)
    return render(request, "auctions/category.html", {
        'listings': listings,
        'category': category
    })