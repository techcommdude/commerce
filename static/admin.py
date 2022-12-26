from django.contrib import admin
from .models import Bids, Listings, Comments, User

# Register your models here.
admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(User)