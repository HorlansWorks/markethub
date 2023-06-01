from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Product)
admin.site.register(User)
# admin.site.register(UserStore)
admin.site.register(UserCategory)
admin.site.register(ProductCategory)
