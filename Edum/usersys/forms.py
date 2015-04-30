#from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta
from django import forms
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from Edum.settings import TOKEN_LENGTH, EMAIL_HOST_USER
from app.models import UserProfile
from usersys.models import ConfirmationToken

#class BootstrapAuthenticationForm(AuthenticationForm):
#    """Authentication form which uses boostrap CSS."""
#    username = forms.CharField(max_length=254,
#                               widget=forms.TextInput({
#                                   'class': 'form-control',
#                                   'placeholder': 'User name'}))
#    password = forms.CharField(label=_("Password"),
#                               widget=forms.PasswordInput({
#                                   'class': 'form-control',
#                                   'placeholder':'Password'}))

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit = True):
        user = super(RegistrationForm, self).save(commit)
        user.is_active = False
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.save()

        confirmation_token = ConfirmationToken()
        confirmation_token.user = user
        confirmation_token.expiry_date = datetime.now() + timedelta(days=2)
        confirmation_token.token = get_random_string(length=TOKEN_LENGTH)
        confirmation_token.save()
        send_mail(
            'Edum registration', 
            'http://localhost:8085/users/%s/token/%s' % (user.id,confirmation_token.token),
            EMAIL_HOST_USER,
            [user.email, EMAIL_HOST_USER],
            fail_silently=False
        )
        return user