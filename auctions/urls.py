from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.activeListings, name="activeListings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listings, name="listings"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("removeFromWatchlist/<int:listing_id>", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("watchlist", views.displayWatchlist, name="displayWatchlist"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("closeAuction/<int:listing_id>", views.closeAuction, name="closeAuction"),
    path("saveListing", views.saveListing, name="saveListing"),
    path("saveComment/<int:listing_id>", views.saveComment, name="saveComment"),
    path("submitBid/<int:listing_id>", views.submitBid, name="submitBid"),
    path("categories", views.categories, name="categories"),
    path('accounts/login/', views.login_view, name="login"),
    path("category/<str:category>", views.displayCategoryListings, name="displayCategoryListings")


]
