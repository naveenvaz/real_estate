from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address', 'location', 'features']

    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'address',
            'location',
            'features',
            Submit('submit', 'Create Property')
        )
        self.helper.form_method = 'post'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['property', 'size', 'rent_cost', 'available', 'features', 'tenant']

    def __init__(self, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'property',
            'size',
            'rent_cost',
            'available',
            'features',
            'tenant',
            Submit('submit', 'Create Unit')
        )
        self.helper.form_method = 'post'
        self.fields['property'].empty_label = 'Please choose the property'
        self.fields['tenant'].empty_label = 'Please choose the tenant'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        property_id = cleaned_data.get('property').id
        size = cleaned_data.get('size')
        tenant = cleaned_data.get('tenant')
        unit_id = cleaned_data.get('id')
        rent_cost = cleaned_data.get('rent_cost')

        if property_id and size:
            existing_unit = Unit.objects.exclude(id=unit_id).filter(property=property_id, size=size).first()
            if existing_unit:
                raise ValidationError("A unit with the same property and size already exists.")
        return cleaned_data

class AgreementForm(forms.ModelForm):
    class Meta:
        model = Agreement
        fields = ['unit', 'tenant', 'property', 'start_date', 'end_date','monthly_rent_date']
        labels = {
            'unit': 'Unit',
            'tenant': 'Tenant',
            'property': 'Property',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'monthly_rent_date':'Rent Date'
        }
    def __init__(self, *args, **kwargs):
        super(AgreementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'unit',
            'tenant',
            'property',
            'start_date',
            'end_date',
            'monthly_rent_date',
            Submit('submit', 'Create Agreement')
        )
        self.helper.form_method = 'post'
        self.fields['tenant'].empty_label = 'Please choose the tenant'
        self.fields['unit'].empty_label = 'Please choose the unit'
        self.fields['property'].empty_label = 'Please choose the property'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        monthly_rent_date = cleaned_data.get('monthly_rent_date')

        if start_date and end_date and start_date > end_date:
            raise ValidationError("Start date cannot be greater than end date.")

        if monthly_rent_date and (monthly_rent_date < start_date or monthly_rent_date > end_date):
            raise ValidationError("Rent date should be between start date and end date.")

        return cleaned_data

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'address']

    def __init__(self, *args, **kwargs):
        super(TenantForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'address',
            Submit('submit', 'Create Tenant')
        )
        self.helper.form_method = 'post'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['tenant', 'document', 'description']

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'tenant',
            'document',
            'description',
            Submit('submit', 'Save'),
            Submit('add_another', 'Save and Add Another')
        )
        self.helper.form_method = 'post'
        self.fields['tenant'].empty_label = 'Please choose the tenant'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_document(self):
        document = self.cleaned_data.get('document')

        if not document:
            raise forms.ValidationError("This field is required.")

        allowed_extensions = ['.png', '.jpg', '.jpeg']
        file_extension = document.name.lower().endswith(tuple(allowed_extensions))

        if not file_extension:
            raise forms.ValidationError("Allowed formats are .png, .jpg, .jpeg.")

        return document

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(FeatureForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            Submit('submit', 'Create Feature')
        )
        self.helper.form_method = 'post'

        # Add classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
