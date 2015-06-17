
from datetime import datetime, timedelta
from django import forms
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from Edum.settings import TOKEN_LENGTH, EMAIL_HOST_USER
from app.models import UserProfile
from usersys.models import ConfirmationToken
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.models import ModelForm

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit = True):
        user = super(RegistrationForm, self).save(commit=False)
        self.save_user(user, commit)
        confirmation_token = self.create_token(user)

        send_mail(
            'Edum registration', 
            'http://localhost:8085/users/%s/token/%s' % (user.id,confirmation_token.token),
            EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
        return user

    def save_user(self, user, commit):
        user.is_active = False
        if commit:
            user.save()
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.save()

    def create_token(self, user):
        confirmation_token = ConfirmationToken()
        confirmation_token.user = user
        confirmation_token.expiry_date = datetime.now() + timedelta(days=2)
        confirmation_token.token = get_random_string(length=TOKEN_LENGTH)
        confirmation_token.save()
        return confirmation_token

    def is_valid(self):
        valid = super(RegistrationForm, self).is_valid()
        if not valid:
            raise ValidationError('Wrong login or password!')
        email = self.cleaned_data['email']
        if email is "":
            raise ValidationError('Enter email please!')
        user = User.objects.filter(email=email)
        if len(user) > 0:
            raise ValidationError('User with this email already exists!')
        return True

#Add decline with sending email?
class PetitionForm(forms.Form):
    field_of_study = forms.CharField(max_length=250)
    university_representative = forms.CharField(max_length=250)
    work_experience = forms.CharField(widget=forms.Textarea())

    def submit(self, username):
        accept_url = 'http://localhost:8085/users/petition/accept/%s' % (username)
        send_mail(
            'Teacher petition', 
            ("%s, requested a petition with following explanations:\n"
            "Field of study: %s\n"
            "University that he represents: %s\n"
            "Work experience: %s\n"
            "Accept: %s") % (
                username, 
                self.cleaned_data['field_of_study'],
                self.cleaned_data['university_representative'],
                self.cleaned_data['work_experience'],
                accept_url
            ),
            EMAIL_HOST_USER,
            [EMAIL_HOST_USER],
            fail_silently=False
        )

class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)