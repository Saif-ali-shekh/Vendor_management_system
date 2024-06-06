from django.db import models
from .model_manager import VendorBaseUserManager
from .choices import *
from django.contrib.auth.models import AbstractBaseUser,  PermissionsMixin
from django.conf import settings
import string
import random
from django.core.validators import MinValueValidator, MaxValueValidator




####################################################################### Time Picker Model
class CommonTimePicker(models.Model):
    """
    An abstract model in Django that provides two fields, `created_at` and `updated_at`, which automatically record the date and time when an object is created or updated.
    """
    created_at = models.DateTimeField("Created Date", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("Updated Date", auto_now=True, db_index=True)
    class Meta:
        abstract = True

class VendorBaseUser(AbstractBaseUser,CommonTimePicker,PermissionsMixin):
    
    user_type = models.CharField("User Type", max_length=10, default='Consumer', choices=USER_TYPE_CHOICES)
    name = models.CharField("Name",max_length=255, blank=True, null=True)
    email = models.EmailField("Email Address", null=True, blank=True, unique=True)
    contact_details = models.TextField()
    address=models.TextField("Address",max_length=500)
    is_superuser = models.BooleanField("Super User", default=False)
    is_active = models.BooleanField("Active", default=True)
    is_staff = models.BooleanField("Staff",default=False)
    
    objects = VendorBaseUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return f"id_{self.id}_email_{self.email}"
    
class Vendor(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="vendor")
    vendor_code =models.CharField(max_length=50, unique=True,blank=True)
    on_time_delivery_rate=models.FloatField(default=0.0)
    quality_rating_avg=models.FloatField(default=0.0)
    average_response_time=models.FloatField(default=0.0)
    fulfillment_rate=models.FloatField(default=0.0)
    
    def generate_vendor_code(self):
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"VEN{self.id}{random_chars}"
    def save(self, *args, **kwargs):
        if not self.vendor_code:
            super().save(*args, **kwargs)  # Save to get an id
            self.vendor_code = self.generate_vendor_code()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"id_{self.id}_email_{self.vendor_code}"
    

class Consumer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consumer')

    def __str__(self):
        return f'{self.id}_{self.user.name}_{self.user.email} '
    
class Product(models.Model):
    product_name = models.CharField("Product Name", max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    available_quantity = models.IntegerField("Available Quantity")

    def __str__(self):
        return f"id_{self.id}_Product_{self.product_name}_Vendor_{self.vendor.vendor_code}"
    

class PurchaseOrder(models.Model):
    po_number = models.CharField("PO Number", max_length=100, unique=True)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, related_name='purchase_orders_consumer')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_orders_vendor')
    order_date = models.DateTimeField("Order Date",blank=True, null=True)
    delivery_date = models.DateTimeField("Delivery Date",blank=True, null=True)
    items = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField("Quantity",validators=[MinValueValidator(1),])
    status = models.CharField("Status", max_length=50,  default='pending',choices=[('pending', 'Pending'),('acknowledged', 'Acknowledged') ,('issued','Issued'), ('completed', 'Completed'), ('canceled', 'Canceled')])
    quality_rating = models.FloatField("Quality Rating", null=True, blank=True)
    issue_date = models.DateTimeField("Issue Date",blank=True, null=True)
    acknowledgment_date = models.DateTimeField("Acknowledgment Date", null=True, blank=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    

    def generate_po_number(self):
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"PO{self.id}{random_chars}"

    def save(self, *args, **kwargs):
        if not self.po_number:
            super().save(*args, **kwargs)  # Save to get an id
            self.po_number = self.generate_po_number()
            kwargs['force_insert'] = False  # Allow update
        super().save(*args, **kwargs)

    def __str__(self):
        return f"id_{self.id}_PO_{self.po_number}_Vendor_{self.vendor.vendor_code}"


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='historical_performances')
    date = models.DateTimeField("Date")
    on_time_delivery_rate = models.FloatField("On Time Delivery Rate",default=0.0)
    quality_rating_avg = models.FloatField("Quality Rating Average",default=0.0)
    average_response_time = models.FloatField("Average Response Time",default=0.0)
    fulfillment_rate = models.FloatField("Fulfillment Rate",default=0.0)
    
    class Meta:
        ordering = ['-id'] 


    def __str__(self):
        return f"id_{self.id}_Performance_{self.vendor.vendor_code}_{self.date.strftime('%Y-%m-%d')}"