from django.contrib import admin

from .models import User, AccountDetails, UserAddress

# admin.site.site_title="Lignes Maritimes Congolaises"
admin.site.site_header="Lignes Maritimes Congolaises"


admin.site.register(User)
admin.site.register(AccountDetails)
admin.site.register(UserAddress)
