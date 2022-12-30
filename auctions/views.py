from django import forms
from django.contrib import messages
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

    # The template filters out those items that are Inactive with an If statement.
    returned_listing = Listings.objects.all()

    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all().order_by('-createdDate')
    })


@login_required
def listings(request, listing_id):

    # TODO: The creation of the form with the base values could be sent to a different function since the saveComment method
    # also uses much of the same functionality.
    # TODO: For Submitting the Bid, closing the auction, Adding to watchlist?, you could display the listing again and
    # just display the message above as I do now.

    # Create the comment form from the forms.py file
    commentForm = forms.CommentForm()

    # Create the bid form
    bidForm = forms.BidForm()

    # Returns all comments from all users for a specific listing when displaying that listing.
    # Just display this in the template.  Do this in the 'listings' view.
    # Add all of the comments to the context as well.
    commentsForListing = Comments.objects.filter(
        listing=listing_id)

    # Get the user ID of the logged in user for the User object
    user_id = request.user.id
    userName = User.objects.get(id=user_id)
    currentObject = Listings.objects.get(id=listing_id)

    # Tests if the watcher is already in the queryset for watchers on the current object.
    if userName in currentObject.watchers.all():
        print("Watcher is already in the list!")
        # Send this in context and do not  display the Add to Watchlist button
        watcher = True

    else:
        print("Watcher is not in the list!")
        # Send this in context and display the REmove from Watchlist button.
        watcher = False

    returnedBids = Bids.objects.get(auction=listing_id)
    currentBidForContext = returnedBids.currentBid

    # Get all the listings and add to context.
    listing = Listings.objects.get(id=listing_id)
    # This returns objects and Querysets.
    return render(request, "auctions/listing.html", {"listing": listing, "commentForm": commentForm, "bidForm": bidForm, "commentsForListing":
                                                     commentsForListing, "watcher": watcher, "currentBidForContext": currentBidForContext})


@login_required
def createlisting(request):
    # Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing,
    # a text-based description, and what the starting bid should be. Users should also optionally be able to provide a
    # URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).

    # Render the create listing form here.  After they create the listing.  Return them to the home page.

    form = forms.AuctionListingForm()

    return render(request, "auctions/createlisting.html", {"form": form})


@login_required
def saveListing(request):

    # Need to get the information from the form here, clean it and then save it to Listings object.
    if request.method == "POST":

        form = forms.AuctionListingForm(request.POST)

        if form.is_valid():

            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            price = form.cleaned_data.get('price')
            category = form.cleaned_data.get('category')
            image_url = form.cleaned_data.get('image_url')

            # Get the user ID of the logged in user for the User object
            user_id = request.user.id
            userName = User.objects.get(id=user_id)

            newListing = Listings(creator=userName, title=title, description=description,
                                  startingBid=price, category=category, url=image_url)
            newListing.save()

            # This is the primary key of the new listing.
            pkNewListing = newListing.id

            # This retrieves the new Listings object that was just created.
            listObjectForBids = Listings.objects.get(id=pkNewListing)

            currentMinBid = float(price)

            # Probably need to create the Bids object since it doesn't currently exist.
            newBidObject = Bids(auction=listObjectForBids,
                                currentBid=currentMinBid)
            newBidObject.save()
            messages.success(request, 'Your listing has been created.')
            # Redirect to activeListings page.
            return HttpResponseRedirect(reverse("activeListings"))


@login_required
def saveComment(request, listing_id):

    if request.method == "POST":

        form = forms.CommentForm(request.POST)

        if form.is_valid():
            # This retries and cleans the data for the comment. 'text' is the name of the comment form field in forms.py.
            newComment = form.cleaned_data.get('text')
            # If there is a comment, then do something.
            if len(newComment) > 0:
                # Save the comment to the model and then redisplay the page with the comment below.

                # Get the user ID of the logged in user for the User object
                user_id = request.user.id
                userName = User.objects.get(id=user_id)

                # Get the ID for the Listings object that has the comment.
                listing = Listings.objects.get(id=listing_id)

                # 'user' must be a User object.  'listing' must be a Listings object.  Save
                # the comment that the user entered.
                savedComment = Comments(
                    comment=newComment, user=userName, listing=listing)
                savedComment.save()


# Get the information to display on the form from this reusable function.
        commentForm, bidForm, commentsForListing, watcher, currentBidForContext = prepareListing(
            request, listing_id)

        return render(request, "auctions/listing.html", {"listing": listing, "commentForm": commentForm, "bidForm": bidForm, "commentsForListing":
                                                         commentsForListing, "watcher": watcher, "currentBidForContext": currentBidForContext})


@login_required
def submitBid(request, listing_id):

    if request.method == "POST":

        form = forms.BidForm(request.POST)

        if form.is_valid():
            # This is the currentBid in the Bids model.
            bidAmount = form.cleaned_data.get('bid')

            # This works!!!!  This is the object that I need to update.
            currentObject = Bids.objects.get(auction=listing_id)

            # When you first create the listing, currentBid needs to be set to the same as startingBid

            # Next, need to update the currentBid in the Bids.currentBid model so that it will work next time
            # you go in and it starts at the previous bids amount.
            # Also need to make sure that the user is not bidding on their own listing.

            # currentObject.currentBid = bidAmount
            curentBid = currentObject.currentBid

            # The currently bidded value must be greater than the last stored bid in currentBid.
            # CurrentBid is set when the listing is created.
            if float(bidAmount) >= curentBid:

                currentObject.bidAmount = bidAmount
                currentObject.save()

                # Update the current bid to the latest value
                currentObject.currentBid = bidAmount
                currentObject.save()

                # TODO: recreate the form and display it again with the message.
                # Pass a flag to a method for bid success or failure.

                messages.success(request, 'Your bid was successful.')
                # Redirect to activeListings page.
                return HttpResponseRedirect(reverse("activeListings"))

            else:
                # Need to issue an error message here per requirements.
                # Redirect to activeListings page.  Need to pass the currentBid somehow.

                # return render(request, "auctions/listing.html", {"listing": listing, "commentForm": commentForm, "bidForm": bidForm, "commentsForListing":
                #                                      commentsForListing, "watcher": watcher, "currentBidForContext": currentBidForContext})
                messages.error(request, 'Your bid was not successful.')
                return HttpResponseRedirect(reverse("activeListings"))


@login_required
def categories(request):

    # Users should be able to visit a page that displays a list of all listing categories.  Do that logic here and then pass the
    # category names to the html page.
    # Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.
    # Go to another view to display the active listings for the category.

    # Gets all the listings.
    # May need to refine this further so that  it only returns listings that are active.
    listing = Listings.objects.filter(active=True)

    # This loops through all listings and returns unique categories.  Then pass these to the page for categories.
    category = listing.order_by().values('category').distinct()

    # Cast it to a list although this is not necessary.
    categories = list(category)

    # Need to make sure that the listings that have the categories are active.  This is
    # currently not the case

    # In the HTML need a for loop where you do "for category in categories"  Create the hyperlinks.
    return render(request, "auctions/categories.html", {"categories": categories})


# This displays all the listings for a particular category.
@login_required
def displayCategoryListings(request, category):

    # Get all the listings and filter out those that are inactive on the template.
    # Only display those listings that have the category name with another if statement on template.

    listings = Listings.objects.all()

    return render(request, "auctions/categoryListing.html", {"listings": listings, "category": category})

# This just displays the full watchlist for a user.


@login_required
def displayWatchlist(request):

    # This displays the watchlist for the user that is logged in.  Need to get all of the objects
    # in the listings and if a user is in the watchlist for the listing, then display it.

    # Watchers is a many to many field that is associated with User object, so
    # need to pass that.
    # Get the user ID of the logged in user for the User object.
    user_id = request.user.id
    userLoggedIn = request.user.username

    watchers = User.objects.get(id=user_id)
    # This returns a QuerySet for the current logged in user.  Returns those listings that have that user as a watcher.
    listingsForWatcher = Listings.objects.filter(watchers=watchers)

    # Need an If statement for display the "Add to watchlist" and "Remove from watchlist" buttons.  Check if the user is in the watchlist
    # to determine which button to display and which method to call.

    # This function now works.  Need to work on the add to watchlist method.
    return render(request, "auctions/watchlist.html", {"userLoggedIn": userLoggedIn, "listingsForWatcher": listingsForWatcher})


@login_required
def watchlist(request, listing_id):
    # This adds a listing to the watchlist for a particular listing ID.
    # Need to update the instance of the object and just add the user as a watcher to the object.
    # Get the user ID of the logged in user for the User object
    user_id = request.user.id
    userName = User.objects.get(id=user_id)
    currentObject = Listings.objects.get(id=listing_id)

    # Tests if the watcher is already in the queryset for watchers on the current object.
    if userName in currentObject.watchers.all():
        print("Watcher is already in the list!")
        # The item has been added to the watchlist, so display the items on the user's watchlist.
        # May want to issue an error message as well.
        messages.error(
            request, 'Listing is already in your watchlist.')
        return HttpResponseRedirect(reverse("displayWatchlist"))
    else:
        print("Watcher is not in the list!")
        # Add the watcher to the list.  Get the current object and add the userName to the watchers
        # field.  do this with a many to many field.
        currentObject.watchers.add(userName)
        print(currentObject.watchers.all())

        # The item has been added to the watchlist, so display the items on the user's watchlist.
        messages.success(
            request, 'Listing has been added to your watchlist.')
        return HttpResponseRedirect(reverse("displayWatchlist"))


@login_required
def removeFromWatchlist(request, listing_id):
    # Removes the item from the watchlist.
    user_id = request.user.id
    userName = User.objects.get(id=user_id)
    # Get the instance of the object based on the user id from the User object.
    currentObject = Listings.objects.get(id=listing_id)
    # Remvoe the object from the instance.
    currentObject.watchers.remove(userName)

    # Go back to the active listings page.
    messages.success(
        request, 'Listing has been removed from your watchlist.')
    return HttpResponseRedirect(reverse("activeListings"))


@login_required
def closeAuction(request, listing_id):

    # user = request.user.username
    user_id = request.user.id
    userName = User.objects.get(id=user_id)

    # Need to get the original price.

    # This works!!!!  This is the object that I need to update.
    currentBidObject = Bids.objects.get(auction=listing_id)
    # Get the current highest bid.
    currentBid = currentBidObject.currentBid

    # bidAmount = currentBidObject.bidAmount

    # Current Listings object.
    currentListingsObject = Listings.objects.get(id=listing_id)
    price = currentListingsObject.startingBid
    creator = currentListingsObject.creator

    if userName == creator:

        if float(currentBid) >= float(price):

            currentListingsObject.active = False
            currentListingsObject.save()
            currentListingsObject.buyer = userName
            currentListingsObject.save()

        # TODO: Pass a flag to a central method and redisplay the same page again with the message below.

            messages.success(
                request, 'You have successfully closed the auction.')
            return HttpResponseRedirect(reverse("activeListings"))
        else:

            messages.error(request, 'You cannot close the auction.')
            return HttpResponseRedirect(reverse("activeListings"))

    # Only display button if the current user is the user that created the listing.

    # If the current bid is higher than the initial price, then the auction can be closed and the listing can be made inactive.

    messages.error(
        request, 'You cannot close this auction since you are not the owner of the listing.')

    return HttpResponseRedirect(reverse("activeListings"))


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


def prepareListing(request, listing_id):

    # TODO: Alot of this could be put into another method since the comment is already saved.
    # Create the comment form from the forms.py file
    commentForm = forms.CommentForm()

    # Create the bid form
    bidForm = forms.BidForm()

    # Get the user ID of the logged in user for the User object
    user_id = request.user.id
    userName = User.objects.get(id=user_id)

    # Returns all comments from all users for a specific listing when displaying that listing.
    # Just display this in the template.  Do this in the 'listings' view.
    # Add all of the comments to the context as well.
    commentsForListing = Comments.objects.filter(
        listing=listing_id).order_by('-createdDate')

    returnedBids = Bids.objects.get(auction=listing_id)
    currentBidForContext = returnedBids.currentBid

    # Tests if the watcher is already in the queryset for watchers on the current object.
    currentObject = Listings.objects.get(id=listing_id)
    if userName in currentObject.watchers.all():
        print("Watcher is already in the list!")
        # Send this in context and do not  display the Add to Watchlist button
        watcher = True

    else:
        print("Watcher is not in the list!")
        # Send this in context and display the REmove from Watchlist button.
        watcher = False

    return commentForm, bidForm, commentsForListing, watcher, currentBidForContext


def handler404(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 404
    return response
