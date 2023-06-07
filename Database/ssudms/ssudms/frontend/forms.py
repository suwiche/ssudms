from django import forms
from django.forms import DateInput

from .models import PdsProvince, PdsCity, PdsBarangay, Designation


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter username'}
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter password'}
    ))

    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))


class CSOForm(forms.Form):
    EXTENSION_CHOICES = [
        ('', 'None'),
        ('Junior', 'Jr.'),
        ('Senior', 'Sr.'),
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III')
    ]

    org_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter organization name'}))

    province = forms.ModelChoiceField(queryset=PdsProvince.objects.all(), widget=forms.Select(attrs={
        'class': 'csoSelectProvince form-control', 'style': 'width:100%'}))

    email = forms.CharField(max_length=100, required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter email'}))

    landline = forms.CharField(max_length=13, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter landline'}))

    fax = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter fax'}))

    cellphone = forms.CharField(max_length=13, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter cellphone'}))

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter first name'}))

    middle_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter middle name'}))

    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter last name'}))

    extension = forms.ChoiceField(required=False, choices=EXTENSION_CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-control'}))

    designation = forms.ModelChoiceField(queryset=Designation.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}))

    ga = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter GA'}))

    approved_program = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter approved program'}))


class CSOOrgDetailsForm(forms.Form):
    cso = forms.IntegerField(widget=forms.HiddenInput())

    org_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter organization name'}))

    ga = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter GA'}))

    approved_program = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter approved program'}))

    province = forms.ModelChoiceField(queryset=PdsProvince.objects.all(), widget=forms.Select(attrs={
        'class': 'csoSelectProvince form-control', 'style': 'width:100%'}))


class CSOOrgContactForm(forms.Form):
    cso = forms.IntegerField(widget=forms.HiddenInput())

    email = forms.CharField(max_length=100, required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter email'}))

    landline = forms.CharField(max_length=13, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter landline'}))

    fax = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter fax'}))

    cellphone = forms.CharField(max_length=13, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter cellphone'}))


class CSOOrgContactPersonForm(forms.Form):
    EXTENSION_CHOICES = [
        ('', 'None'),
        ('Jr', 'Jr.'),
        ('Sr', 'Sr.'),
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III')
    ]

    cso = forms.IntegerField(widget=forms.HiddenInput())

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter first name'}))

    middle_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter middle name'}))

    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter last name'}))

    extension = forms.ChoiceField(required=False, choices=EXTENSION_CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-control'}))

    designation = forms.ModelChoiceField(queryset=Designation.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}))


class CSOTransactionForm(forms.Form):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    cso = forms.IntegerField(widget=forms.HiddenInput())
    transaction = forms.IntegerField(widget=forms.HiddenInput())
    control_no = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter control no.', 'readonly': True}))

    date_issued = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'date', 'readonly': True}))
    date_expired = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'date', 'readonly': True}))
    status = forms.ChoiceField(required=True, choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

'''
class CDCForm(forms.Form):
    STATUS_CHOICES = [
        ('7', 'New'),
        ('6', 'Renewal')
    ]
    LEVEL_CHOICES = [
        ('1', '1'),
        ('2', '2')
    ]
    center_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Center name'}))
    province = forms.ModelChoiceField(queryset=PdsProvince.objects.all(), widget=forms.Select(attrs={'class': 'cdcSelectProvince form-control', 'style': 'width:100%'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    level = forms.ChoiceField(choices=LEVEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    accreditation_no = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Accreditation no'}))
    date_issued = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))


class CDWForm(forms.Form):
    EXTENSION_CHOICES = [
        ('', 'None'),
        ('Junior', 'Jr.'),
        ('Senior', 'Sr.'),
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III')
    ]
    STATUS_CHOICES = [
        ('7', 'New'),
        ('6', 'Renewal')
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Rather_not_to_say', 'Rather not to say')
    ]
    LEVEL_CHOICES = [
        ('1', '1'),
        ('2', '2')
    ]
    cdc = forms.ModelChoiceField(queryset=CdcTable.objects.filter(details__status=1).all(), widget=forms.Select(attrs={'class': 'cdcSelect form-control', 'style': 'width:100%'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    middle_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter middle name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))
    extension = forms.ChoiceField(required=False, choices=EXTENSION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    province = forms.ModelChoiceField(queryset=PdsProvince.objects.all(), widget=forms.Select(attrs={'class': 'cdwSelectProvince form-control', 'style': 'width:100%'}))
    level = forms.ChoiceField(choices=LEVEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    accreditation_no = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Accreditation no'}))
    date_issued = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    date_complete = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    date_of_assessment = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))


class SwdaCategoryForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}))


class SwdaSubCategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=CategoryTable.objects.all(), widget=forms.Select(attrs={'class': 'categorySelect form-control', 'style': 'width:100%'}))
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter sub category name'}))


class SWDAForm(forms.Form):
    EXTENSION_CHOICES = [
        ('', 'None'),
        ('Junior', 'Jr.'),
        ('Senior', 'Sr.'),
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III')
    ]

    CLASSIFICATION_CHOICES = [
        ('Swa', 'Swa'),
        ('Auxiliary', 'Auxiliary')
    ]
    sub_category = forms.ModelChoiceField(queryset=SubCategoryTable.objects.all(), widget=forms.Select(attrs={'class': 'subCategorySelect form-control', 'style': 'width:100%'}))
    agency = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter agency name'}))
    province = forms.ModelChoiceField(queryset=PdsProvince.objects.all(), widget=forms.Select(attrs={'class': 'swdaSelectProvince form-control', 'style': 'width:100%'}))
    email = forms.CharField(max_length=100, required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    landline = forms.CharField(max_length=13, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter landline'}))
    cellphone = forms.CharField(max_length=13, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cellphone'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    middle_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter middle name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))
    extension = forms.ChoiceField(required=False, choices=EXTENSION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    designation = forms.ModelChoiceField(queryset=OrgDesignationTable.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    accreditation_no = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Accreditation no'}))
    date_issued = forms.CharField(required=False, widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    registration_no = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registration no'}))
    rdate_issued = forms.CharField(required=False, widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    license_no = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'License no'}))
    ldate_issued = forms.CharField(required=False, widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    services = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}))
    classification = forms.ChoiceField(required=False, choices=CLASSIFICATION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    clientele_served = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Clientele Served'}))
    delivery_mode = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Service Delivery Mode'}))
    aoo_province = forms.ModelChoiceField(queryset=PdsProvince.objects.all(), widget=forms.Select(attrs={'class': 'aooSelectProvince form-control', 'style': 'width:100%'}))
    remarks = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Remarks'}))



class CSOForm(ModelForm):
    class Meta:
        model = CsoTable
        fields = ['ga', 'approve_program', 'details', 'worker']
        
        DESIGNATION_CHOICES = [
            ('President', 'President')
        ]
        CERTIFICATE_CHOICES = [
            ('Accreditation', 'Accreditation')
        ]
        
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'business_address': TextInput(attrs={'class': 'form-control', 'required': False}),
            'email_address': EmailInput(attrs={'placeholder': 'Please input email address', 'class': 'form-control'}),
            'landline': TextInput(attrs={'class': 'form-control'}),
            'fax': TextInput(attrs={'class': 'form-control'}),
            'cellphone': TextInput(attrs={'class': 'form-control'}),
            'contact_person': TextInput(attrs={'class': 'form-control'}),
            'designation': forms.Select(choices=DESIGNATION_CHOICES, attrs={'class': 'form-control'}),
            'certificate': forms.Select(choices=CERTIFICATE_CHOICES, attrs={'class': 'form-control'}),
            'dswd_certificate_accreditation_no': TextInput(attrs={'class': 'form-control'}),
            'date_issued': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ga': TextInput(attrs={'class': 'form-control'}),
            'caap': TextInput(attrs={'class': 'form-control'}),

        }

        labels = {
            'dswd_certificate_accreditation_no': 'DSWD Certificate Accreditation No'
        }
        '''
