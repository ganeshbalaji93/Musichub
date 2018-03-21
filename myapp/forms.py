from django import forms


class DisplayForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control input-sm', 'placeholder': 'Username'})
    )

    email = forms.CharField(
        required=True,
        label='Email',
        max_length=32,
        widget=forms.EmailInput(attrs={'class': 'form-control input-sm', 'placeholder': 'Mail Address'})
    )

    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput(attrs={'class': 'form-control input-sm', 'placeholder': 'Password'})
    )
