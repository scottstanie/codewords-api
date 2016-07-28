from django.contrib import admin

# Admin workaround for AbstractUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from api.models import User, Game, WordSet, Word, Card, Guess, Clue


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('custom_data',)}),  # input custom fields here
    )


admin.site.register(Game)
admin.site.register(WordSet)
admin.site.register(Word)
admin.site.register(Card)
admin.site.register(Guess)
admin.site.register(Clue)
