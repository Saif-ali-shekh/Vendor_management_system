
from rest_framework import serializers
from vendor_models.models import *
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta


class SignupSerializer(serializers.ModelSerializer):
    name =serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
            'blank': 'email cannot be blank',
        }
    )
    password = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 6 characters long.',
        },
        write_only=True,
        min_length=6  # Minimum length validation
    )
    confirm_password = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Confirm Password is required.',
        },
        write_only=True
    )
    address = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Address is required.',
        }
    )
    
    class Meta:
        model=VendorBaseUser
        fields = ['name', 'email','password', 'confirm_password',  'contact_details','address']
        
    def validate(self, data):
       
        if VendorBaseUser.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError("This email has already been registered.")
        confirm_password = data.get('confirm_password')
        password = data.get('password')
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords don't match.")
        return data
    
    def create(self,validated_data):
        user_data = {
            'user_type': 'Vendor',
            'name': validated_data.get('name'),
            'email': validated_data.get('email'),
            'contact_details':validated_data.get('contact_details'),
            'address': validated_data.get('address'),
        }
        
        user=VendorBaseUser.objects.create(**user_data)
        user.set_password(validated_data.get('password'))
        user.is_active = True
        user.save()
        
        vendor_obj=Vendor.objects.create(user=user)
        return user


# serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from vendor_models.models import VendorBaseUser

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
            'blank': 'Email cannot be blank',
        }
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={
            'required': 'Password is required.',
            'blank': 'Password cannot be blank',
        }
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            print("user auth",user)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        
        return user
    
class ConsumerSignupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
            'blank': 'Email cannot be blank',
        }
    )
    password = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 6 characters long.',
        },
        write_only=True,
        min_length=6  # Minimum length validation
    )
    confirm_password = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Confirm Password is required.',
        },
        write_only=True
    )
    address = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Address is required.',
        }
    )
    
    class Meta:
        model = VendorBaseUser
        fields = ['name', 'email', 'password', 'confirm_password', 'contact_details', 'address']
        
    def validate(self, data):
        if VendorBaseUser.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError("This email has already been registered.")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords don't match.")
        return data
    
    def create(self, validated_data):
        user_data = {
            'user_type': 'Consumer',
            'name': validated_data.get('name'),
            'email': validated_data.get('email'),
            'contact_details': validated_data.get('contact_details'),
            'address': validated_data.get('address'),
        }
        
        user = VendorBaseUser.objects.create(**user_data)
        user.set_password(validated_data.get('password'))
        user.is_active = True
        user.save()
        
        consumer_obj=Consumer.objects.create(user=user)
        consumer_obj.save()
        
        return user
        
#######################Purchas Order

class PurchaseOrderSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(write_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ['item_id', 'quantity']

    def validate_item_id(self, value):
        try:
            product = Product.objects.get(id=value)
            return product
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product with this ID does not exist.")

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value

    def create(self, validated_data):
        product = validated_data.pop('item_id')
        quantity = validated_data['quantity']
        if quantity > product.available_quantity:
            raise serializers.ValidationError("Selected quantity is greater than available quantity.")
        
        product.available_quantity -= quantity
        product.save()

        validated_data['vendor'] = product.vendor
        validated_data['consumer'] = self.context['request'].user.consumer
        validated_data['order_date'] = timezone.now()
        validated_data['delivery_date'] = timezone.now() + timedelta(days=7)
        validated_data['items'] = product
        return PurchaseOrder.objects.create(**validated_data)
    
class PurchaseOrderListSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.user.name', read_only=True)
    product_name = serializers.CharField(source='items.product_name', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor_name', 'product_name', 'quantity', 'order_date', 'delivery_date', 'status']
    
    

class PurchaseOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor', 'items', 'quantity', 'order_date', 'delivery_date', 'status', 'quality_rating']

    def update(self, instance, validated_data):
        # Update only the allowed fields
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.status = validated_data.get('status', instance.status)
        instance.quality_rating = validated_data.get('quality_rating', instance.quality_rating)
        
        # You might want to add some business logic here for allowed status transitions, etc.
        
        instance.save()
        return instance
##########################################
class VendorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name')
    email = serializers.EmailField(source='user.email')
    address = serializers.CharField(source='user.address')
    contact_details = serializers.CharField(source='user.contact_details')

    class Meta:
        model = Vendor
        fields = ['id', 'vendor_code', 'name', 'email', 'contact_details','address']
        read_only_fields = ['vendor_code']
        
    def update(self, instance, validated_data):
        # Update nested user fields
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        # Update Vendor fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class ConsumerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name')
    email = serializers.EmailField(source='user.email')
    address = serializers.CharField(source='user.address')
    contact_details = serializers.CharField(source='user.contact_details')

    class Meta:
        model = Consumer
        fields = ['id', 'name', 'email', 'contact_details', 'address']
        
    def update(self, instance, validated_data):
        # Update nested user fields
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        # Update Consumer fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    
class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
##########status change
# serializers.py

class PurchaseOrderAcknowledgmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['status', 'acknowledgment_date']
        read_only_fields = ['acknowledgment_date']

    def validate(self, data):
        instance = self.instance  # Access the current instance being updated
        current_status = instance.status

        if current_status in ['completed', 'issues', 'canceled']:
            raise serializers.ValidationError(f"Status cannot be changed because the current status is '{current_status}'.")

        if data['status'] != 'acknowledged':
            raise serializers.ValidationError("Status can only be changed to 'acknowledged' via this endpoint.")
        
        return data

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.acknowledgment_date = timezone.now()
        instance.save()
        return instance

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.user.name', read_only=True)

    class Meta:
        model = HistoricalPerformance
        fields = ['id', 'vendor_name','date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']


class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'available_quantity']

    def validate_available_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'available_quantity']
