from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget

# Admin workaround for AbstractUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from api.models import User

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

@admin.register(User)
class MyUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('custom_data',)}), # input custom fields here
    )

# Import your models for the Admin Interface
# from app.models import YourModel

# Register your models here, ex.:
# admin.site.register(NameOfModel)

# class WolfPageAdminForm(forms.ModelForm):
#     body = forms.CharField(widget=CKEditorWidget())
#     class Meta:
#         model = WolfPage
#         fields = '__all__'
#
# class WolfPageAdmin(admin.ModelAdmin):
#     form = WolfPageAdminForm
#
# admin.site.register(WolfPage, WolfPageAdmin)
