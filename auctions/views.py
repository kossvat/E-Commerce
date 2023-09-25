from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F


from .models import User, Listing, Bid, Category
from .forms import ListingForm, BidForm, CommentForm


def index(request):
    active_listing = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        'active_listing': active_listing
    })


def closed_listings(request):
    closed_listing = Listing.objects.filter(active=False)
    return render(request, "auctions/closed_listing.html", {
        'closed_listing': closed_listing
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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
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


def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.current_price = listing.starting_bid
            listing.save()
            return redirect('index')
        
    else:
        form = ListingForm()
        
    return render(request, "auctions/create_listing.html", {
        'form': form
    })


def listing_details(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment_instance = form.save(commit=False)
            comment_instance.user = request.user
            comment_instance.listing = listing
            comment_instance.save()
            return redirect('listing_details', listing_id=listing_id)
        
    else:
        form = CommentForm()
    
    bids = Bid.objects.filter(auction=listing).order_by('-date')
    return render(request, "auctions/listing_details.html", {
        'listing': listing,
        'bids': bids,
        'form': form
    })


def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.watchers.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_from_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.watchers.remove(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def users_watchlist(request):
    user_watchlist = Listing.objects.filter(watchers=request.user)
    return render(request, "auctions/user_watchlist.html", {
        'listings': user_watchlist,
        'watchlist_count': user_watchlist.count()
    })


def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    
    # Check if Auction is Active
    if not listing.active:
        messages.error(request, "This auction  is not longer active.")
        return redirect("listing_details", listing_id=listing_id)
    
    # Check if user is the creator of the listing
    if request.user == listing.creator:
        messages.error(request, "You cannot place bid on your own listing.")
        return redirect("listing_details", listing_id=listing_id)
    
    if request.method == "POST":
        form = BidForm(request.POST)

        if form.is_valid():
            # Assign auction and user before validating
            bid_instance = form.save(commit=False)
            
            # Ensure the bid is higher than current price
            if bid_instance.offer <= listing.current_price:
                messages.error(request, f"Your bid must be higher than {listing.current_price}$ .")
                return redirect("listing_details", listing_id=listing_id)
            
            bid_instance.auction = listing
            bid_instance.user = request.user
            
            # Update the current price of the listing
            listing.current_price = F('current_price') + bid_instance.offer - listing.current_price
            listing.save(update_fields=['current_price'])
            
            # Save the bid instance
            bid_instance.save()
            
            messages.success(request, "Your bit has been successfully placed!")
            return redirect("listing_details", listing_id=listing_id)
        
        else:
            messages.error(request, "There was an error with your bid. Please check the provided data.")
    
    else:
        form = BidForm()

    return render(request, "auctions/listing_details.html", {
        "form": form,
        "listing": listing
    })


def end_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    
    if request.user != listing.creator and not request.user.is_staff:
        messages.error(request, "You are not authorize to end this auction.")
        return redirect("listing_details", listing_id=listing_id)
    
    if not listing.active:
        messages.error(request, "The auction is already ended.")
        return redirect("listing_details", listing_id=listing_id)
    
    listing.active = False
    listing.save()
    messages.success(request, "The auction has been successfully ended.")
    return redirect("listing_details", listing_id=listing_id)


def category_list(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        'categories': categories
    })
    

def category_listing(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(category=category, active=True)
    return render(request, "auctions/category_listings.html", {
        'category': category,
        'listings': listings
    })


def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.user != listing.creator:
        messages.error("You are not authorized to edit this listing.")
        return redirect('listing_details', listing_id=listing_id)

    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, "Listing updated successfully!")
            return redirect('listing_details', listing_id=listing_id)
        
    else:
        form = ListingForm(instance=listing)
    
    return render(request, 'auctions/edit_listing.html', {
        'form': form
    })

        


    




        
