from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm, TextInput, CheckboxInput, NumberInput, Textarea
from django import forms
from .models import LibraryExtensions, LibraryTypes, LibraryProcess, LibraryServices, LibraryStatus, LibraryLevel, \
    DetailsAttribute, WorkerAttribute, Forms, FormVersions


class SignUpForm(UserCreationForm):
    username = forms.CharField(min_length=4, max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    email = forms.EmailField(required=False, label='Enter email',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    first_name = forms.CharField(required=False, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(required=False, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))
    password1 = forms.CharField(min_length=6, label='Enter password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    password2 = forms.CharField(min_length=6, label='Confirm password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))
    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox_animated'}))
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox_animated'}))
    is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox_animated'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control', 'style': 'width:100%'}))

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'groups', 'is_active', 'is_staff',
            'is_superuser')

    def clean_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError("Password does not match!")
        else:
            return password1


class UpdateUserForm(ModelForm):
    username = forms.CharField(min_length=4, max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    email = forms.EmailField(required=False, label='Enter email',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    first_name = forms.CharField(required=False, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(required=False, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))
    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox_animated'}))
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox_animated'}))
    is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox_animated'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False,
                                   widget=forms.Select(attrs={'class': 'form-control', 'style': 'width:100%'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'groups', 'is_active', 'is_staff', 'is_superuser')


class ExtensionForm(ModelForm):
    STATUS_CHOICES = [
        ('', ''),
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = LibraryExtensions
        fields = ['name', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter extension name'}),
        }

    def clean_extension(self):
        name = self.cleaned_data['name']
        r = LibraryExtensions.objects.filter(name=name).first()
        if r:
            raise ValidationError("Extension name already exists")
        return name


class ProcessForm(ModelForm):
    STATUS_CHOICES = [
        ('', ''),
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = LibraryProcess
        fields = ['name', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter process name'})
        }

    def clean_process(self):
        name = self.cleaned_data['name']
        r = LibraryProcess.objects.filter(name=name).first()
        if r:
            raise ValidationError("Process name already exists")
        return name


class ServicesForm(ModelForm):
    STATUS_CHOICES = [
        ('', ''),
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = LibraryServices
        fields = ['name', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter services name'})
        }

    def clean_service(self):
        name = self.cleaned_data['name']
        r = LibraryServices.objects.filter(name=name).first()
        if r:
            raise ValidationError("Services name already exists")
        return name


class TypeForm(ModelForm):
    STATUS_CHOICES = [
        ('', ''),
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    HAS_WORKER_CHOICES = [
        (1, 'Yes'),
        (0, 'No'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    has_worker = forms.ChoiceField(choices=HAS_WORKER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    is_worker = forms.ChoiceField(choices=HAS_WORKER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = LibraryTypes
        fields = ['name', 'acronym', 'status', 'has_worker', 'is_worker']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter type name'}),
            'acronym': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter type acronym'}),
        }

    def clean_type(self):
        name = self.cleaned_data['name']
        r = LibraryTypes.objects.filter(name=name).first()
        if r:
            raise ValidationError("Type name already exists")
        return name

    def clean_acronyms(self):
        acronym = self.cleaned_data['acronym']
        r = LibraryTypes.objects.filter(acronym=acronym).first()
        if r:
            raise ValidationError("Type acronym already exists")
        return acronym


class StatusForm(ModelForm):
    STATUS_CHOICES = [
        ('', ''),
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = LibraryStatus
        fields = ['name', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter status name'})
        }

    def clean_status_name(self):
        name = self.cleaned_data['name']
        r = LibraryStatus.objects.filter(name=name).first()
        if r:
            raise ValidationError("Status name already exists")
        return name


class LevelForm(ModelForm):
    STATUS_CHOICES = [
        ('', ''),
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = LibraryLevel
        fields = ['name', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter level name'})
        }

    def clean_level(self):
        name = self.cleaned_data['name']
        r = LibraryLevel.objects.filter(name=name).first()
        if r:
            raise ValidationError("Level name already exists")
        return name


class Form(ModelForm):
    STATUS_CHOICES = [
        ('', ''),
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    ORIENTATION_CHOICES = [
        ('', ''),
        ('landscape', 'Landscape'),
        ('portrait', 'Portrait'),
    ]

    FORM_TYPE_CHOICES = [
        ('', ''),
        ('individual', 'Individual'),
        ('multiple', 'Multiple'),
        ('special', 'Special')
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    org_type = forms.ModelChoiceField(queryset=LibraryTypes.objects.filter(status=1).all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    orientation = forms.ChoiceField(choices=ORIENTATION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    form_type = forms.ChoiceField(choices=FORM_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Forms
        fields = ['name', 'status', 'org_type', 'orientation', 'form_type']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter form name'})
        }

    def clean_form_name(self):
        name = self.cleaned_data['name']
        r = Forms.objects.filter(name=name).first()
        if r:
            raise ValidationError("Form name already exists")
        return name


class VersionsForm(ModelForm):
    STATUS_CHOICES = [
        ('', ''),
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    form = forms.ModelChoiceField(queryset=Forms.objects.filter(status=1).all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = FormVersions
        fields = ['name', 'form', 'status', 'template']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter version name'}),
            'template': Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter template script'})
        }

    def clean_form_version_name(self):
        name = self.cleaned_data['name']
        r = FormVersions.objects.filter(name=name).first()
        if r:
            raise ValidationError("Form version name already exists")
        return name


class DetailsAttributeForm(ModelForm):
    INPUT_TYPE_CHOICES = [
        ('', ''),
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('email', 'Email'),
    ]

    STATUS_CHOICES = [
        ('', ''),
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    IS_REQUIRED_CHOICES = [
        ('', ''),
        (1, 'Yes'),
        (0, 'No'),
    ]

    input_type = forms.ChoiceField(choices=INPUT_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    type = forms.ModelChoiceField(empty_label='Select', queryset=LibraryTypes.objects.filter(status=1),
                                  widget=forms.Select(attrs={'class': 'form-control', 'style': 'width:100%'}))
    is_required = forms.ChoiceField(choices=IS_REQUIRED_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = DetailsAttribute
        fields = ['name', 'input_type', 'width', 'order', 'type', 'is_required', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter attribute name'}),
            'order': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter order'}),
            'width': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter width'}),
        }


class WorkerAttributeForm(ModelForm):
    INPUT_TYPE_CHOICES = [
        ('', ''),
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('email', 'Email'),
    ]

    STATUS_CHOICES = [
        ('', ''),
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    IS_REQUIRED_CHOICES = [
        ('', ''),
        (1, 'Yes'),
        (0, 'No'),
    ]

    input_type = forms.ChoiceField(choices=INPUT_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    type = forms.ModelChoiceField(empty_label='Select', queryset=LibraryTypes.objects.filter(status=1),
                                  widget=forms.Select(attrs={'class': 'form-control', 'style': 'width:100%'}))
    is_required = forms.ChoiceField(choices=IS_REQUIRED_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = WorkerAttribute
        fields = ['name', 'input_type', 'width', 'order', 'type', 'is_required', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter attribute name'}),
            'order': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter order'}),
            'width': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter width'}),
        }


class TransactionAttributeForm(ModelForm):
    INPUT_TYPE_CHOICES = [
        ('', ''),
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('email', 'Email'),
    ]

    STATUS_CHOICES = [
        ('', ''),
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    IS_REQUIRED_CHOICES = [
        ('', ''),
        (1, 'Yes'),
        (0, 'No'),
    ]

    input_type = forms.ChoiceField(choices=INPUT_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    type = forms.ModelChoiceField(empty_label='Select', queryset=LibraryTypes.objects.filter(status=1),
                                  widget=forms.Select(attrs={'class': 'form-control', 'style': 'width:100%'}))
    is_required = forms.ChoiceField(choices=IS_REQUIRED_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = WorkerAttribute
        fields = ['name', 'input_type', 'width', 'order', 'type', 'is_required', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter attribute name'}),
            'order': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter order'}),
            'width': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter width'}),
        }
