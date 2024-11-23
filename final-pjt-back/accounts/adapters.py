from allauth.account.adapter import DefaultAccountAdapter

class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):

        from allauth.account.utils import user_field

        user = super().save_user(request, user, form, False)
        print(request.data.get('ph'))
        user_field(user, 'nickname', request.data.get('nickname'))
        user.save()
        return user