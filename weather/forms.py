from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from weather.models import Cities

class SignupForm(UserCreationForm):  
    #Overwrite form fields
    password1 = forms.CharField(
        label="password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    username = forms.CharField(
        label="username",
        widget=forms.TextInput(attrs={"autocomplete":""}),
        help_text=None,
    )
    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput(),
        required=False,
    )
    first_name = forms.CharField(
        label="name",
        widget=forms.TextInput,
        required=False,
    )
    last_name = forms.CharField(
        label="lastname",
        widget=forms.TextInput,
        required=False,
    )
    is_staff = forms.BooleanField(
        label="is admin",
        widget=forms.CheckboxInput,
        help_text=None,
        required=False,
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        #check username
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            self.add_error(None, u'username : "%s" is in use.' % username)
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        ####### uncomment for more password restriction
        #number restriction
        # if not re.findall('\d', password1):
        #     self.add_error(None,"*password must contain at least one number.")
        #capital letter restriction
        # if not re.findall('[A-Z]', password1):
        #     self.add_error(None,"*password must contain at least one capital letter.")
        #small letter restriction
        # if not re.findall('[a-z]', password1):
        #     self.add_error(None,"*password must contain at least one small letter.")
        #######

        
        #check password length
        if len(password1) < 10:
            self.add_error(None,"*password must be 10 characters or more.")
        return password1
    
    class Meta:  
        model = User
        fields = ('username','first_name','last_name','email','is_staff')

    def __init__(self, *args, **kwargs):
        super(SignupForm,self).__init__(*args, **kwargs)
        del self.fields['password2'] #delete this for password verification field


class LoginForm(forms.Form):
    username = forms.CharField(
        label="username",
        widget=forms.TextInput(attrs={"autocomplete":""}),
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={'autocomplete': ''}),
    )

    
class UpdateUserForm(forms.ModelForm):
    ## update password ##
    ## search for update password and uncomment -> you need to uncomment things in views.py too.
    # password = forms.CharField(
    #     label="password",
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={'autocomplete':'off'}),
    # )
    username = forms.CharField(
        label="username",
        widget=forms.TextInput(),
        help_text=None,
    )
    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput(),
        required=False,
    )
    first_name = forms.CharField(
        label="name",
        widget=forms.TextInput,
        required=False,
    )
    last_name = forms.CharField(
        label="lastname",
        widget=forms.TextInput,
        required=False,
    )
    is_staff = forms.BooleanField(
        label="is admin",
        widget=forms.CheckboxInput,
        help_text=None,
        required=False,
    )
    is_active = forms.BooleanField(
        label="is active",
        widget=forms.CheckboxInput,
        help_text=None,
        required=False,
    )
    class Meta:
        model = User
        ## update password ##
        fields = ['username','first_name','last_name','email','is_staff','is_active'] # add 'password' for update password. search for update password and uncomment -> you need to uncomment things in views.py too.

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm,self).__init__(*args, **kwargs)


class CityUpdateForm(forms.ModelForm):

    city = forms.CharField(
        label="city name",
        widget=forms.TextInput(),
        help_text=None,
    )

    class Meta:
        model = Cities
        fields = ['city']

    def __init__(self, *args, **kwargs):
        super(CityUpdateForm,self).__init__(*args, **kwargs)