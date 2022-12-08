from django.contrib import admin
from .models import Bids, Listing, Comments, User

# Register your models here.
admin.site.register(Listing)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(User)