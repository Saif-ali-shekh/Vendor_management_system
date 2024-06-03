
from django.urls import path
from .views import *

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    
    
    ################################ Purchase Order  ################################ 
    # Operations performed create order, list of all orders , list of particular vendor_order, retrive by id , update ,del order
    
    path('api/purchase_orders/create/', CreatePurchaseOrderView.as_view(), name='create_purchase_order'),
    path('api/purchase_orders/<int:purchase_order_id>/', PurchaseOrderDetailView.as_view(), name='purchase-order-detail'),  #get put ,delete
    path('api/purchase_orders/rate/<int:purchase_order_id>/', RatePurchaseOrderView.as_view(), name='rate_purchase_order'),
    path('api/purchase_orders/<int:purchase_order_id>/issue/', IssuePurchaseOrderView.as_view(), name='issue_purchase_order'),
    path('api/purchase_orders/list/', ListConsumerPurchaseOrdersView.as_view(), name='list-consumer-purchase-orders'),
    
    
    #vendor
    path('api/purchase-orders/<int:id>/acknowledge/', PurchaseOrderAcknowledgmentView.as_view(), name='purchase-order-acknowledge'),
    path('api/purchase_orders/<int:purchase_order_id>/complete/',CompletePurchaseOrderView.as_view(), name='complete_purchase_order'),
    
     
    ####################### Vendor Profile  #######################
    
    path('api/vendors/signup/',VendorSignupView.as_view(),name='vendor-signup'),
    path('api/vendors/list', VendorListView.as_view(), name='vendor-list'),
    path('api/vendors/<int:vendor_id>/', VendorDetailView.as_view(), name='vendor-detail'), # get ,put, del
    
    
    ####################### Consumer Profile #######################
    path('api/consumer/signup/',ConsumerSignupView.as_view(),name='consumer-signup'),
    path('api/consumer/details/', ConsumerDetailView.as_view(), name='consumer-details'),
    
    ####################### Purchase ORDER status and issue #######################
    path('api/vendors/purchase_orders/<int:purchase_order_id>/complete/',CompletePurchaseOrderView.as_view(), name='complete_purchase_order'),

    
    #######################  Products #######################

    path('api/product/',ProductCreateAPIView.as_view(), name='product'),
    path('api/product/list/',ProductListAPIView.as_view(), name='product'),
    path('api/product/update',ProductUpdateView.as_view(), name='product-update'),
    path('api/product/delete/<int:product_id>/',ProductDeleteView.as_view(), name='delete-product'),



     ####################### Vendor Performance #######################

    path('api/vendors/performance/', PerformanceMetricsAPIView.as_view(), name='vendor_performance'),
    path('api/vendors/historical-performance/',VendorHistoricalPerformance.as_view(), name='vendor-historical-performance'),

]
