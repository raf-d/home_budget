from django.contrib import admin
from budget_app.models import FamilyMember, MoneyTransfer, Category

# Register your models here.
admin.site.register(FamilyMember)
admin.site.register(MoneyTransfer)
admin.site.register(Category)