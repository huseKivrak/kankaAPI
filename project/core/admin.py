from django.contrib import admin
from .models import User, Letter, Recipient
# Register your models here.

admin.site.register(User)
admin.site.register(Letter)
admin.site.register(Recipient)


