from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator,ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

class Property(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    features = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Feature(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Unit(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    type_choices = [('1BHK', '1BHK'), ('2BHK', '2BHK'), ('3BHK', '3BHK'), ('4BHK', '4BHK')]
    size = models.CharField(max_length=4, choices=type_choices)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    available = models.BooleanField(default=True)
    features = models.ManyToManyField(Feature)
    tenant = models.OneToOneField('Tenant', null=True,blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.property.name} {self.size} "


class Tenant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    properties = models.ManyToManyField(Property, through='Agreement')

    def __str__(self):
        return self.name


class Agreement(models.Model):
    unit = models.OneToOneField(Unit, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)  # Add this line
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent_date = models.DateField()

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.monthly_rent_date:
            if not (self.start_date <= self.monthly_rent_date <= self.end_date):
                raise ValidationError("Rent date should be within the start and end date.")

class Document(models.Model):
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.tenant.name} - {self.description}"
