from django.contrib.auth.forms import UserCreationForm,UserChangeForm 
from django.contrib.auth import get_user_model

class CustomUserCreationsForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email',)


from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    nickname = forms.CharField(max_length=50, label='Nickname')

    def save(self, request):
        # 부모 클래스의 save() 메서드를 호출하여 기본 사용자 저장 로직 실행
        user = super().save(request)
        # nickname 값을 저장
        user.nickname = self.cleaned_data['nickname']
        user.save()
        return user