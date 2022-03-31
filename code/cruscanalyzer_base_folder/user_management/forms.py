from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """
    Registration form where the user entering: username, email, name, last name
    and password can create a new profile to access the application
    """
    username = forms.CharField(max_length=50, label='Username',
                               widget=forms.TextInput(attrs={'placeholder': 'Es: mario.rossi'}))
    first_name = forms.CharField(max_length=50, label='Nome',
                                 widget=forms.TextInput(attrs={'placeholder': 'Es: Mario'}))
    last_name = forms.CharField(max_length=50, label='Cognome',
                                widget=forms.TextInput(attrs={'placeholder': 'Es: Rossi'}))
    email = forms.EmailField(label='Email')

    helper = FormHelper()
    helper.form_id = 'utente-crispy-form'
    helper.form_method = 'POST'

    error_messages = {
        'password_mismatch': "Le password non corrispondono!",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set style-input class for the dark-theme
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'style-input'

        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group mb-0'),
                Column('first_name', css_class='form-group mb-0'),
                Column('last_name', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name",)

    def clean_username(self):
        """
        Cheks if the inserted username is already present in the database (only if it's been changed from the original).
        :returns: username
        :raises: forms.ValidationError
        """
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).count():
            raise forms.ValidationError(
                'Un utente con questo username è già presente.')
        return username

    def clean_email(self):
        """
        Cheks if the inserted mail is already present in the database (only if it's been changed from the original).
        :returns: mail
        :raises: forms.ValidationError
        """
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).count():
            raise forms.ValidationError(
                'Un utente con questa mail è già presente.')
        return email


class LoginForm(AuthenticationForm):
    """
    Login form where an already registered user can enter the username and password to authenticate
    """
    helper = FormHelper()
    helper.form_id = 'utente-login-crispy-form'
    helper.form_method = 'POST'

    error_messages = {
        'invalid_login': "Username o password errati. Perfavore, controlla i tuoi dati.",
        'inactive': "Questo account non è più attivo.",
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None

        super().__init__(*args, **kwargs)

        self.fields['username'].label = "Nome utente/email"

        # set style-input class for the dark-theme
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'style-input'

        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password', css_class='form-group mb-0'),
                css_class='form-row'
            ),
        )


class UpdateUserForm(forms.Form):
    """
    Form for updating the user data.
    Not inheritance of ModelForm because otherwise it wouldn't be possible to update the user data because the username
    is already present in the database.
    """
    username = forms.CharField(required=True, label='Username')
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(required=True, label='Nome')
    last_name = forms.CharField(required=True, label='Cognome')

    helper = FormHelper()
    helper.form_id = 'update-user-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit(
        'cancel',
        'Annulla',
        css_class='btn-secondary',
        formnovalidate='formnovalidate',
    ))
    helper.add_input(Submit(
        'submit',
        'Salva',
        css_class='btn btn-success',
    ))

    # class Meta:
    #     fields = ('username', 'email', 'first_name', 'last_name')
    #     labels = {
    #         'username': 'Username',
    #         'email': 'Email',
    #         'first_name': 'Nome',
    #         'last_name': 'Cognome',
    #     }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set style-input class for the dark-theme
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'style-input'

    def clean_username(self):
        """
        Checks if the inserted username is already present in the database (only if it's been changed from the original).
        :returns: username
        :raises: forms.ValidationError
        """
        username = self.cleaned_data.get('username')

        if username != self.files.username and User.objects.filter(username=username).count():
            raise forms.ValidationError(
                'Un utente con questo username è già presente.')
        return username

    def clean_email(self):
        """
        Checks if the inserted mail is already present in the database (only if it's been changed from the original).
        :returns: mail
        :raises: forms.ValidationError
        """
        email = self.cleaned_data.get('email')

        if email != self.files.email and User.objects.filter(email=email).count():
            raise forms.ValidationError(
                'Un utente con questa mail è già presente.')
        return email

    def save(self, commit=True):
        """
        Updates the authenticated user data on the database.
        :param commit: If save the new data.
        :returns: authenticated user.
        """
        # Accessing the authenticated user passed from the View in "files".
        current_user = self.files
        current_user.username = self.cleaned_data['username']
        current_user.email = self.cleaned_data['email']
        current_user.first_name = self.cleaned_data['first_name']
        current_user.last_name = self.cleaned_data['last_name']

        if commit:
            current_user.save()

        return current_user
