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
    path("createlisting", views.createlisting, name="createlisting"),
    path("categories", views.categories, name="categories")
]
