

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
            print("quality_rating_count",quality_rating_count)
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
