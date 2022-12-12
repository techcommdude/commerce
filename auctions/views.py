from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Bids
from .models import Comments
from .models import Listings


def activeListings(request):
    # active = Listings.objects.get(active=True)
    returned_listing = Listings.objects.all()
    print(returned_listing)
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()
    })


def listings(request, listing_id):

    listing = Listings.objects.get(id=listing_id)
    return render(request, "auctions/listing.html", {"listing": listing})

# TODO: This needs work.  users where watchlist = true.  Change watchlist to Boolean.  Need to look at the examples.


def watchlist(request, listing_id):

    print(listing_id)
    test = Listings.objects.get(id=listing_id)
    # This prints the listing.
    print(test)
    test2 = test.watchers.all()
    # This prints the watchers for the listing id.
    print(test2)

    #Turn the queryset into a list.
    userList = list(test2)





    user = request.user.username

    # This loops through the watcher queryset.
    for x in userList:


        if x.username == user:
            # print("This item is already on the user's watchlist!")
            return HttpResponseRedirect(reverse("activeListings"))
            #Need to exit at this point and not do anything.


   #Add the item to the watchlist.

    return HttpResponse("Need to add item to watchlist!")










    # TODO:
    # Need to search through queryset tests for 'gfarnell'
    # test4 = Listings.objects.filter(user=user)
    # print(test4)

    # # This gets the current username.
    # username2 = request.user.username
    # print(username2)

    # listings = Listings.objects.all().values()
    # print(listings)

    # usernameWatchlist = Listings.objects.values('watchlist')
    # print(usernameWatchlist)

    # # Need the id here.
    # usernameWatchlist = Listings.objects.filter(watchers=1)
    # print(usernameWatchlist)

    # getUserName = User.objects.filter(username=request.user.username)
    # if getUserName:
    #     print("That username")

    # for x in listings:
    #     print(x)
    #     print(test.watchers.all().values())
    #     # This prints all the values of the User object
    #     print(User.objects.all().values())

    # print(listings)

    # print(test2)
    # test = Listings.objects.filter()
    # test = Listings.objects.get(User.username)
    # print(test)




def new_func(listings):
    listings.id


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("activeListings"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("activeListings"))


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
        return HttpResponseRedirect(reverse("activeListings"))
    else:
        return render(request, "auctions/register.html")
