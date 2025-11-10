from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Bid, AuctionListings, Comments


def index(request):
    listings = AuctionListings.objects.filter(is_closed=False)
    listingC = []
    for list in listings:
        if list.category not in listingC:
            listingC.append(list.category)
    return render(request, "auctions/index.html",{"listing":listings,"listC":listingC})


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

@login_required
def create_listing(request):
    listingcategory = AuctionListings.objects.all()
    if request.method == "POST":
        user = request.user 
        nameitem = request.POST['nameitem'].capitalize() 
        description = request.POST['description'].capitalize() 
        bid = Bid(bid=request.POST["bid"], user=user)
        bid.save()
        url = request.POST['image']
        categoryS = request.POST['categoryS'].capitalize() 
        categoryC = request.POST['categoryC'].capitalize() 
        if categoryS != "Open this select menu":
            category = categoryS
        else:
            category = categoryC
        listingS = AuctionListings(owner=user,nameitem=nameitem, description=description, bid = bid,  url = url, category = category,is_closed = False)
        listingS.save()
        return HttpResponseRedirect(reverse("index"))
    listings = AuctionListings.objects.filter(is_closed=False)
    listingC = []
    for list in listings:
        if list.category not in listingC:
            listingC.append(list.category)
    return render(request, "auctions/create_listing.html",{"listing":listingcategory,"listC":listingC})


def view_listing(request,auction_id):
    listings = AuctionListings.objects.get(id=auction_id)
    comments = listings.comments.all()
    return render(request, "auctions/view_listing.html",{"listing":listings,"comments":comments})

@login_required   
def watchlist(request):
    user = request.user
    if request.method == "POST":
        id = request.POST['add_watchlist']
        listing = AuctionListings.objects.get(pk=id)
        listing.watchlist.add(user)
        listing.save()
        comments = listing.comments.all()
        return render(request, "auctions/view_listing.html",{"listing":listing,"comments":comments,"message":"Item added to the wathclist :)"})
    else:
        userlist = user.watch_listings.all()
        return render(request, "auctions/watchlist.html",{"listing":userlist})
    
@login_required   
def remove_watchlist(request):
    user = request.user
    if request.method == "POST":
        id = request.POST['remove_watchlist']
        listing = AuctionListings.objects.get(pk=id)
        listing.watchlist.remove(user)
        listing.save()
        comments = listing.comments.all()
        return render(request, "auctions/view_listing.html",{"listing":listing,"comments":comments,"message":"Item removed from the wathclist :("})

    
@login_required   
def new_bid(request):
    user = request.user
    if request.method == "POST":
        id = request.POST['id_bid']
        newbid = float(request.POST['newbid'])
        listing = AuctionListings.objects.get(pk=id)
        comments = listing.comments.all()
        if listing.bid.bid < newbid:
            bid = Bid(bid=newbid , user=user)
            bid.save()
            listing.bid = bid
            listing.save()
            return render(request, "auctions/view_listing.html",{"listing":listing,"comments":comments,"message":"Success:Bid register"})
        else:
            return render(request, "auctions/view_listing.html",{"listing":listing,"comments":comments,"message":"Error:The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed"})

@login_required   
def close_auction(request):
    user = request.user
    if request.method == "POST":
        id = request.POST['close']
        listing = AuctionListings.objects.get(pk=id)
        listing.is_closed = True
        listing.save()
        comments = listing.comments.all()
        return render(request, "auctions/view_listing.html",{"listing":listing,"comments":comments,"message":"The auction is closed"})

@login_required   
def comment(request):
    user = request.user
    if request.method == "POST":
        newcomment = request.POST['new_comment']
        id = request.POST['id_comment']
        listing = AuctionListings.objects.get(pk=id)
        Comment = Comments(writer = user, listing = listing, text = newcomment)
        Comment.save()
        comments = listing.comments.all()
        return render(request, "auctions/view_listing.html",{"listing":listing,"comments":comments,"message":"Comment has been added"})

  
def category(request):
    if request.method == "POST":
        Scategory = request.POST['Scategory']
        listings = AuctionListings.objects.filter(category=Scategory)
        return render(request, "auctions/category.html",{"listing":listings,"category":Scategory})