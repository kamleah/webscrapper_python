from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)


class RegistrationForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    process_type = forms.CharField(required=True)
    user_role = forms.IntegerField(required=True)
    user_created_by = forms.IntegerField(required=True)
