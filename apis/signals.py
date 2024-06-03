# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.db import transaction
# from django.db.models import Count, F, Q
# from django.utils import timezone
# from  vendor_models.models import PurchaseOrder, Vendor, HistoricalPerformance,VendorBaseUser
# from django.db.models import Sum

# @receiver(post_save, sender=PurchaseOrder)

# def update_on_time_delivery_rate(sender, instance, created, **kwargs):
#     if instance.status == 'completed':
#         # Calculate On-Time Delivery Rate
#         completed_orders_count = PurchaseOrder.objects.filter(status='completed').count()
#         on_time_orders_count = PurchaseOrder.objects.filter(
#             status='completed',
#             delivery_date__lte=F('order_date') + timezone.timedelta(days=7)
#         ).count()
#         on_time_delivery_rate = (on_time_orders_count / completed_orders_count) * 100 if completed_orders_count > 0 else 0

#         # Update Vendor model
#         vendor = instance.vendor
#         vendor.on_time_delivery_rate = on_time_delivery_rate
#         vendor.save()

#         # Update or create HistoricalPerformance record
#         with transaction.atomic():
#             historical_performance, created = HistoricalPerformance.objects.get_or_create(
#                 vendor=vendor,
#                 date=timezone.now().date()
#             )
#             historical_performance.on_time_delivery_rate = on_time_delivery_rate
#             historical_performance.save()
            

# @receiver(post_save, sender=PurchaseOrder)
# def update_quality_rating_average(sender, instance, created, **kwargs):
    
#     if instance.status == 'completed' and instance.quality_rating is not None:
#         # Get all completed purchase orders for the vendor
#         completed_orders = PurchaseOrder.objects.filter(
#             vendor=instance.vendor,
#             status='completed',
#             quality_rating__isnull=False
#         )

#         # Calculate the Quality Rating Average
#         total_quality_rating = completed_orders.aggregate(total=Sum('quality_rating'))['total']
#         total_orders_count = completed_orders.count()
#         quality_rating_average = total_quality_rating / total_orders_count if total_orders_count > 0 else 0

#         # Update Vendor model
#         vendor = instance.vendor
#         vendor.quality_rating_avg = quality_rating_average
#         vendor.save()

#         # Update or create HistoricalPerformance record
#         with transaction.atomic():
#             historical_performance, created = HistoricalPerformance.objects.get_or_create(
#                 vendor=vendor,
#                 date=timezone.now().date()
#             )
#             historical_performance.quality_rating_avg = quality_rating_average
#             historical_performance.save()


# @receiver(post_save, sender=PurchaseOrder)
# def update_average_response_time(sender, instance, created, **kwargs):
    
#     if instance.status == 'acknowledged' and instance.acknowledgment_date is not None:
#         # Get all acknowledged purchase orders for the vendor
#         acknowledged_orders = PurchaseOrder.objects.filter(
#             vendor=instance.vendor,
#             status='acknowledged',
#             acknowledgment_date__isnull=False
#         )

#         # Calculate the Average Response Time
#         total_response_time = sum((order.acknowledgment_date - order.issue_date).total_seconds() for order in acknowledged_orders)
#         total_orders_count = acknowledged_orders.count()
#         average_response_time = total_response_time / total_orders_count if total_orders_count > 0 else 0

#         # Update Vendor model
#         vendor = instance.vendor
#         vendor.average_response_time = average_response_time
#         vendor.save()

#         # Update or create HistoricalPerformance record
#         with transaction.atomic():
#             historical_performance, created = HistoricalPerformance.objects.get_or_create(
#                 vendor=vendor,
#                 date=timezone.now().date()
#             )
#             historical_performance.average_response_time = average_response_time
#             historical_performance.save()



# from django.db.models.signals import post_save, post_delete


# @receiver([post_save, post_delete], sender=PurchaseOrder)
# def update_fulfilment_rate(sender, instance, **kwargs):
    
#     # Get all purchase orders for the vendor
#     all_orders = PurchaseOrder.objects.filter(vendor=instance.vendor)

#     # Calculate the number of successfully fulfilled POs
#     successful_orders_count = all_orders.filter(status='completed').exclude(quality_rating__isnull=False).count()

#     # Calculate the total number of POs issued to the vendor
#     total_orders_count = all_orders.count()

#     # Calculate the Fulfilment Rate
#     fulfilment_rate = (successful_orders_count / total_orders_count) * 100 if total_orders_count > 0 else 0

#     # Update Vendor model
#     vendor = instance.vendor
#     vendor.fulfilment_rate = fulfilment_rate
#     vendor.save()

#     # Update or create HistoricalPerformance record
#     historical_performance, created = HistoricalPerformance.objects.get_or_create(
#         vendor=vendor,
#         date=timezone.now().date()
#     )
#     historical_performance.fulfilment_rate = fulfilment_rate
#     historical_performance.save()


# ###test
# @receiver(post_save, sender=VendorBaseUser)
# def vendor_base_user_created(sender, instance, created, **kwargs):
#     if created:

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from vendor_models.models import *
from django.db.models import Avg, F, Count ,ExpressionWrapper,fields,Sum
from django.utils import timezone
from django.dispatch import receiver,Signal
from vendor_models.models import *



def create_historical_performance(vendor):
    HistoricalPerformance.objects.create(
       vendor=vendor,
        date=timezone.now(),
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate
    )

# post_save.connect(create_historical_performance,sender=HistoricalPerformance)

def calculate_on_time_delivery_rate(sender, instance, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        completed_orders_count = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed'
        ).count()
        on_time_orders_count = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed',
            completed_date__lte=F('delivery_date')
        ).count()
        if completed_orders_count > 0:
            on_time_delivery_rate = on_time_orders_count / completed_orders_count
            vendor.on_time_delivery_rate = on_time_delivery_rate
            vendor.save()
            create_historical_performance(vendor)
        else:
            on_time_delivery_rate = 0.0
        return on_time_delivery_rate
post_save.connect(calculate_on_time_delivery_rate,sender=PurchaseOrder)



def calculate_quality_rating_avg(sender, instance, **kwargs):

    if instance.status == 'completed' and instance.quality_rating is not None:
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed',
            quality_rating__isnull=False
        )
        if completed_orders.exists():
            quality_rating_sum = completed_orders.aggregate(total=Sum('quality_rating'))['total']
            quality_rating_count = completed_orders.count()
            quality_rating_avg = quality_rating_sum / quality_rating_count
            vendor.quality_rating_avg = quality_rating_avg
            vendor.save()
            create_historical_performance(vendor)
        else:
            quality_rating_avg = 0.0
        return quality_rating_avg
post_save.connect(calculate_quality_rating_avg,sender=PurchaseOrder)


def calculate_average_response_time(sender, instance, **kwargs):
    
    if instance.status == 'acknowledged' and instance.acknowledgment_date:
        vendor = instance.vendor
        acknowledged_orders = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='acknowledged',
            acknowledgment_date__isnull=False
        )
        acknowledged_orders_with_issue_date = acknowledged_orders.filter(issue_date__isnull=False)
        if acknowledged_orders_with_issue_date.exists():
            response_times = acknowledged_orders_with_issue_date.annotate(
                response_time=ExpressionWrapper(
                    F('acknowledgment_date') - F('issue_date'),
                    output_field=fields.DurationField()
                )
            )
            average_response_time = response_times.aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
            if average_response_time:
                vendor.average_response_time = average_response_time.total_seconds()
            else:
                vendor.average_response_time = 0.0
        vendor.save()
        create_historical_performance(vendor)
post_save.connect(calculate_average_response_time,sender=PurchaseOrder)



def calculate_fulfillment_rate(sender, instance, **kwargs):

    vendor = instance.vendor
    total_orders = PurchaseOrder.objects.filter(vendor=vendor)
    fulfilled_orders = total_orders.filter(status='completed', issue_date__isnull=True)
    if total_orders.exists():
        fulfillment_rate = fulfilled_orders.count() / total_orders.count()
    else:
        fulfillment_rate = 0.0
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()
    create_historical_performance(vendor)
post_save.connect(calculate_fulfillment_rate,sender=PurchaseOrder)
