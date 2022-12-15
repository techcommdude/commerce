from django import forms
from .import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Bids
from .models import Comments
from .models import Listings


# The template filters out those listings that are not active, so I send everything here.
@login_required
def activeListings(request):
    # active = Listings.objects.get(active=True)
    # get all the listings
    returned_listing = Listings.objects.all()
    print(returned_listing)
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()
    })


@login_required
def listings(request, listing_id):

    # Create the comment form from the forms.py file
    commentForm = forms.CommentForm()

    # Create the bid form
    bidForm = forms.BidForm()

    # TODO: Need to add the comments to the templates as well.
    # Returns all comments from all users for a specific listing when displaying that listing.
    # Just display this in the template.  Do this in the 'listings' view.
    # Add all of the comments to the context as well.
    commentsForListing = Comments.objects.filter(
        listing=listing_id)
    print(commentsForListing)
    # return render(request, "auctions/index.html", {"commentsForListing": commentsForListing})




    # Get all the listings and add to context.
    listing = Listings.objects.get(id=listing_id)
    return render(request, "auctions/listing.html", {"listing": listing, "commentForm": commentForm, "bidForm": bidForm, "commentsForListing": commentsForListing})

# TODO: This needs work.  users where watchlist = true.  Change watchlist to Boolean?  Need to look at the examples.
# TODO: Also need to render the forms here.  the comment form and the bid form.


@login_required
def createlisting(request):
    # Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing,
    # a text-based description, and what the starting bid should be. Users should also optionally be able to provide a
    # URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).

    # TODO: render the create listing form here.  After they create the listing.  Return them to the home page.

    form = forms.AuctionListingForm()

    return render(request, "auctions/createlisting.html", {"form": form})

# Need to display a list of hyperlinked categories.


@login_required
def saveComment(request, listing_id):

    if request.method == "POST":

        form = forms.CommentForm(request.POST)
        print(form)

        if form.is_valid():
            # This retries and cleans the data for the comment. 'text' is the name of the comment form field in forms.py.
            newComment = form.cleaned_data.get('text')
            # If there is a comment, then do something.
            if len(newComment) > 0:
                # print(newComment)
                # TODO: Save the comment to the model and then redisplay the page with the comment below.

                # Get the user ID of the logged in user for the User object
                user_id = request.user.id
                userName = User.objects.get(id=user_id)

                # Get the ID for the Listings object that has the comment.
                listingObject = Listings.objects.get(id=listing_id)
                print(listingObject)

                # 'user' must be a User object.  'listing' must be a Listings object.  Save
                # the comment that the user entered.
                savedComment = Comments(
                    comment=newComment, user=userName, listing=listingObject)
                savedComment.save()

                # this returns a queryset for all users and all comments on all listings.
                #commentObject = Comments.objects.all()

                # Only need to save the comment here and redirect to the active listings page.  Next
                # time when you display the listing you can get the comments. as we've done here.

                # Redirect to activeListings page.
                return HttpResponseRedirect(reverse("activeListings"))


@login_required
def submitBid(request, listing_id):

    if request.method == "POST":

        form = forms.BidForm(request.POST)
        print(form)

        if form.is_valid():
            bidAmount = form.cleaned_data.get('bid')
            print(bidAmount)
            # TODO: Need to save the bidAmount to the model.  Don't need to worry about the user, just that this is the current highest bid.

        # can get the user that submitted it as well.
        return HttpResponse("Submitting the bid! Calling the submitBid view.")


@login_required
def categories(request):

    # Users should be able to visit a page that displays a list of all listing categories.  Do that logic here and then pass the
    # category names to the html page.
    # Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.
    # Go to another view to display the active listings for the category.

    # Gets all the listings.
    listing = Listings.objects.all()
    print(listing)

    # This loops through all listings and returns unique categories.  Then pass these to the page for categories.
    category = listing.order_by().values('category').distinct()
    print(category)
    # Cast it to a list although this is not necessary.
    categories = list(category)

    # In the HTML need a for loop where you do "for category in categories"  Create the hyperlinks.
    return render(request, "auctions/categories.html", {"categories": categories})


# This displays all the listings for a particular category.
@login_required
def displayCategoryListings(request, category):

    # Get all the listings and filter out those that are inactive on the template.
    # Only display those listings that have the category name with another if statement on template.

    listings = Listings.objects.all()
    print(listings)
    print(category)

    return render(request, "auctions/categoryListing.html", {"listings": listings, "category": category})

# This just displays the full watchlist for a user.


@login_required
def displayWatchlist(request):

    watchingUser = request.user.username
    print(watchingUser)

    return render(request, "auctions/watchlist.html", {"watchingUser": watchingUser})

# This has the logic for determinging if an item is in the watchlist and if it isn't to add it.


@login_required
def watchlist(request, listing_id):

    print(listing_id)
    test = Listings.objects.get(id=listing_id)
    # This prints the listing.
    print(test)
    test2 = test.watchers.all()
    # This prints the watchers for the listing id.
    print(test2)

    # Turn the queryset into a list.
    userList = list(test2)

    user = request.user.username
    user = request.user

    # This loops through the watcher queryset.
    for x in userList:

        if x.username == user:
            # This item is already on the user's watchlist, so go to the current active Listings again.
            # May want to display a message at this point.
            return HttpResponseRedirect(reverse("activeListings"))
            # Need to exit at this point and not do anything.

    # TODO: Need to work on this to figure out how to update the watchlist.
    # watchUsername = request.user.username
    # watchUsername.save()
    # print(watchUsername)

   # Add the item to the watchlist.
    # username = request.user.username
    # test6 = Listings(watchers=username)
    # test6.save()

    # test5 = Listings.objects.get(id=listing_id)
    # test5.watchers = request.user.username

    # The item has been added to the watchlist, so display the items on the user's watchlist.
    return HttpResponseRedirect(reverse("displayWatchlist"))
    # return render(request, "auctions/watchlist.html")
    # return HttpResponse("Need to add item to watchlist for this user!")

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


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        print(user)

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
