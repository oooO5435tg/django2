from django.contrib import admin
from .models import User, Category
from .models import Request


admin.site.register(User)
admin.site.register(Request)
admin.site.register(Category)
