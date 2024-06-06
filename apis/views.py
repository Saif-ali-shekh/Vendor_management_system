from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


class VendorSignupView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses={
            201: openapi.Response('Vendor created successfully.', SignupSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error',
        }
    )
    def post(self,request):
        try:
            serializer  =SignupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                return Response(
                        {
                            'responseCode': status.HTTP_201_CREATED,
                            'responseMessage': "Vendor  created successfully.",
                            'responseData': serializer.data,
                        },
                        status=status.HTTP_201_CREATED
                        )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': [f"{error[1][0]}" for error in dict(serializer.errors).items()][0],
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except serializers.ValidationError as e:
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': [f"{error[1][0]}" for error in dict(e).items()][0],
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return  Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': "Something went wrong",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(description='OK', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'responseCode': status.HTTP_200_OK,
                        'responseMessage': 'Login successful.',
                        'responseData': {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': 'Bad Request',
                    'responseData': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Internal Server Error',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ConsumerSignupView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        request_body=ConsumerSignupSerializer,
        responses={
            201: openapi.Response('Consumer created successfully.', ConsumerSignupSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error',
        }
    )
    def post(self,request):
        try:
            serializer  =ConsumerSignupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                return Response(
                        {
                            'responseCode': status.HTTP_201_CREATED,
                            'responseMessage': "Consumer  created successfully.",
                            'responseData': serializer.data,
                        },
                        status=status.HTTP_201_CREATED
                        )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': [f"{error[1][0]}" for error in dict(serializer.errors).items()][0],
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except serializers.ValidationError as e:
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': [f"{error[1][0]}" for error in dict(e).items()][0],
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return  Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': "Something went wrong",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ConsumerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True, default='Bearer ')
        ],
        responses={
            200: openapi.Response('Consumer details retrieved successfully.', ConsumerSerializer),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Permission Denied",
            404: "Not Found",
            500: "Internal Server Error"
        }
    )
    def get(self, request):
        try:
            consumer = request.user.consumer
            serializer = ConsumerSerializer(consumer)
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Consumer details retrieved successfully.',
                    'responseData': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': str(e),
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True, default='Bearer ')
        ],
        request_body=ConsumerSerializer,
        responses={
            200: openapi.Response('Consumer updated successfully.', ConsumerSerializer),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Permission Denied",
            404: "Not Found",
            500: "Internal Server Error"
        }
    )
    def put(self, request):
        try:
            consumer = request.user.consumer
            serializer = ConsumerSerializer(consumer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_200_OK,
                        'responseMessage': 'Consumer updated successfully.',
                        'responseData': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': [f"{error[1][0]}" for error in dict(serializer.errors).items()][0],
                    'responseData': None
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': str(e),
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True, default='Bearer ')
        ],
        responses={
            200: "Consumer deleted successfully.",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Permission Denied",
            404: "Not Found",
            500: "Internal Server Error"
        }
    )
    def delete(self, request):
        try:
            consumer = request.user.consumer
            user = consumer.user
            consumer.delete()
            user.delete()
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Consumer and associated user deleted successfully.',
                    'responseData': None
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': str(e),
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
            
################## Purchase Order

class CreatePurchaseOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True,default='Bearer ')
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'item_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the product to purchase'),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity of the product to purchase'),
            }
        ),
        responses={
            201: 'Purchase order created successfully.',
            400: 'Failed to create purchase order.'
        }
    )
    def post(self, request):
        try:
            if request.user.user_type != 'Consumer':
                return Response({'responseCode':status.HTTP_400_BAD_REQUEST,
                                 'responseMessage':'Only Consumer can purchase products.'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = PurchaseOrderSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                purchase_order = serializer.save()
                print("serializer",serializer.data)
                
                return Response(
                    {
                        'responseCode': status.HTTP_201_CREATED,
                        'responseMessage': 'Purchase order created successfully.',
                        # 'responseData': serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        'responseCode': status.HTTP_400_BAD_REQUEST,
                        'responseMessage': 'Failed to create purchase order.',
                        'responseData': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': str(e),
                    
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListConsumerPurchaseOrdersView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('vendor_id', openapi.IN_QUERY, description="Filter by vendor ID", type=openapi.TYPE_INTEGER, required=False),
        ],
        responses={
            200: 'List of purchase orders retrieved successfully.',
            400: 'Bad request.',
            500: 'Internal server error.'
        }
    )
    def get(self, request):
        try:
            consumer = request.user.consumer
            vendor_id = request.GET.get('vendor_id', None)

            if vendor_id:
                purchase_orders = PurchaseOrder.objects.filter(consumer=consumer,  vendor_id=vendor_id)
            else:
                purchase_orders = PurchaseOrder.objects.filter(consumer=consumer)

            serializer = PurchaseOrderListSerializer(purchase_orders, many=True)
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'List of purchase orders retrieved successfully.',
                    'responseData': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': str(e),
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PurchaseOrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, consumer, purchase_order_id):
        try:
            return PurchaseOrder.objects.get(id=purchase_order_id, consumer=consumer)
        except PurchaseOrder.DoesNotExist:
            return None

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=False)
        ],
        responses={
            200: 'Purchase order details retrieved successfully.',
            404: 'Purchase order not found.',
            500: 'Internal server error.'
        }
    )
    def get(self, request, purchase_order_id):
        try:
            consumer = request.user.consumer
            purchase_order = self.get_object(consumer, purchase_order_id)

            if not purchase_order:
                return Response(
                    {
                        'responseCode': status.HTTP_404_NOT_FOUND,
                        'responseMessage': ' order not found.',
                        'responseData': None
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = PurchaseOrderDetailSerializer(purchase_order)
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Purchase order details retrieved successfully.',
                    'responseData': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': str(e),
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=False)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity of the product'),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the order', enum=['pending', 'acknowledged', 'issued', 'completed', 'canceled']),
                'quality_rating': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', description='Quality rating'),
            }
        ),
        responses={
            200: 'Purchase order updated successfully.',
            404: 'Purchase order not found.',
            400: 'Invalid data provided.',
            500: 'Internal server error.'
        }
    )
    def put(self, request, purchase_order_id):
        try:
            consumer = request.user.consumer
            purchase_order = self.get_object(consumer, purchase_order_id)

            if not purchase_order:
                return Response(
                    {
                        'responseCode': status.HTTP_404_NOT_FOUND,
                        'responseMessage': 'Purchase order not found.',
                        'responseData': None
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = PurchaseOrderDetailSerializer(purchase_order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_200_OK,
                        'responseMessage': 'Purchase order updated successfully.',
                        'responseData': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': 'Invalid data provided.',
                    'responseData': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': str(e),
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=False)
        ],
        responses={
            200: 'Purchase order deleted successfully.',
            404: 'Purchase order not found.',
            500: 'Internal server error.'
        }
    )
    def delete(self, request, purchase_order_id):
        try:
            consumer = request.user.consumer
            purchase_order = self.get_object(consumer, purchase_order_id)
            if purchase_order.status not in ['canceled', 'pending']:
                return Response(
                    {
                        'responseCode': status.HTTP_400_BAD_REQUEST,
                        'responseMessage': 'Purchase order cannot be deleted unless it is canceled or pending.',
                        'responseData': None
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not purchase_order:
                return Response(
                    {
                        'responseCode': status.HTTP_404_NOT_FOUND,
                        'responseMessage': 'Purchase order not found.',
                        'responseData': None
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            purchase_order.delete()
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Purchase order deleted successfully.',
                    'responseData': None
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': str(e),
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

class RatePurchaseOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='consumer Bearer  ', type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('purchase_order_id', openapi.IN_PATH, description='ID of the purchase order to be rated', type=openapi.TYPE_INTEGER,required=True),
            openapi.Parameter('quality_rating', openapi.IN_QUERY, description='Quality rating out of 5 (float with up to 1 decimal point)', type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT,required=True)
        ],
        responses={
            200: 'Purchase order rated successfully.',
            400: 'Bad Request',
            403: 'Forbidden - You are not authorized to rate this purchase order.',
            404: 'Not Found - Purchase order does not exist.',
            409: 'Conflict - Purchase order status is not completed or rating has already been provided.',
            500: 'Internal Server Error'
        }
    )
    def post(self, request, purchase_order_id):
        try:
            purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)

            if purchase_order.consumer.user != request.user:
                return Response(
                    {
                        'responseCode': status.HTTP_403_FORBIDDEN,
                        'responseMessage': 'Forbidden - You are not authorized to rate this purchase order.',
                        'responseData': None
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            if purchase_order.status != 'completed':
                return Response(
                    {
                        'responseCode': status.HTTP_409_CONFLICT,
                        'responseMessage': 'Conflict - Purchase order status is not completed.',
                        'responseData': None
                    },
                    status=status.HTTP_409_CONFLICT
                )

            if purchase_order.quality_rating is not None:
                return Response(
                    {
                        'responseCode': status.HTTP_409_CONFLICT,
                        'responseMessage': 'Conflict - Rating has already been provided for this purchase order.',
                        'responseData': None
                    },
                    status=status.HTTP_409_CONFLICT
                )

            quality_rating = request.query_params.get('quality_rating')
            if quality_rating is not None:
                quality_rating = float(quality_rating)
                if 0 <= quality_rating <= 5:
                    purchase_order.quality_rating = quality_rating
                    purchase_order.save()
                    return Response(
                        {
                            'responseCode': status.HTTP_200_OK,
                            'responseMessage': 'Purchase order rated successfully.',
                            
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    raise ValidationError('Quality rating must be between 0 and 5.')
            else:
                raise ValidationError('Quality rating is required.')

        except PurchaseOrder.DoesNotExist:
            return Response(
                {
                    'responseCode': status.HTTP_404_NOT_FOUND,
                    'responseMessage': 'Not Found - Purchase order does not exist.',
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except ValidationError as e:
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': 'Bad Request',
                    'responseData': {'error': str(e)}
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Internal Server Error',
                    'responseData': {'error': 'Something went wrong! Please try again.'}
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
##########################################
class VendorListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=False,)
        ],
        responses={
            200: openapi.Response('List of vendors', VendorSerializer(many=True)),
            401: "Unauthorized",
            403: "Permission Denied",
            500: "Internal Server Error"
        }
    )
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class VendorDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=False)
        ],
        responses={
            200: openapi.Response('Vendor details retrieved successfully.', VendorSerializer),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Permission Denied",
            404: "Not Found",
            500: "Internal Server Error"
        }
    )
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            serializer = VendorSerializer(vendor)
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Vendor details retrieved successfully.',
                    'responseData': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Vendor.DoesNotExist:
            return Response(
                {
                    'responseCode': status.HTTP_404_NOT_FOUND,
                    'responseMessage': 'Vendor not found.',
                    'responseData': None
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': str(e),
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=False)
        ],
        request_body=VendorSerializer,
        responses={
            200: openapi.Response('Vendor updated successfully.', VendorSerializer),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Permission Denied",
            404: "Not Found",
            500: "Internal Server Error"
        }
    )
    def put(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            serializer = VendorSerializer(vendor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_200_OK,
                        'responseMessage': 'Vendor updated successfully.',
                        'responseData': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': [f"{error[1][0]}" for error in dict(serializer.errors).items()][0],
                    'responseData': None
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Vendor.DoesNotExist:
            return Response(
                {
                    'responseCode': status.HTTP_404_NOT_FOUND,
                    'responseMessage': 'Vendor not found.',
                    'responseData': None
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': str(e),
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=False)
        ],
        responses={
            200: "Vendor deleted successfully.",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Permission Denied",
            404: "Not Found",
            500: "Internal Server Error"
        }
    )
    def delete(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            user = vendor.user
            vendor.delete()
            user.delete()
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Vendor and associated user deleted successfully.',
                    'responseData': None
                },
                status=status.HTTP_200_OK
            )
        except Vendor.DoesNotExist:
            return Response(
                {
                    'responseCode': status.HTTP_404_NOT_FOUND,
                    'responseMessage': 'Vendor not found.',
                    'responseData': None
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': str(e),
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        try:
            # Retrieve the vendor object
            vendor = Vendor.objects.get(id=vendor_id)
            
            if vendor.user.user_type != 'Vendor':
                return Response(
                    {
                        'responseCode': status.HTTP_403_FORBIDDEN,
                        'responseMessage': 'User type is not Vendor',
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Retrieve the vendor's historical performance records
            performance_records = HistoricalPerformance.objects.filter(vendor=vendor)
            
            # Serialize the performance metrics
            serializer = VendorPerformanceSerializer(performance_records, many=True)
            
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Vendor performance metrics retrieved successfully.',
                    'responseData': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Vendor.DoesNotExist:
            return Response(
                {
                    'responseCode': status.HTTP_404_NOT_FOUND,
                    'responseMessage': 'Vendor not found.',
                    'responseData': None
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': str(e),
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class PurchaseOrderAcknowledgmentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING,default='Bearer '),
        ],
        responses={
            200: 'Purchase order acknowledged successfully.',
            400: 'Bad request.',
            401: 'Unauthorized.',
            404: 'Purchase order not found.',
            409: 'Purchase order already acknowledged.',
            500: 'Internal server error.'
        }
    )
    def post(self, request, id):
        try:
            if request.user.user_type != 'Vendor':
                return Response(
                    {
                        'responseCode': status.HTTP_403_FORBIDDEN,
                        'responseMessage': 'Forbidden - Only vendors can acknowledge purchase orders.',
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            vendor = request.user.vendor   
            purchase_orders = PurchaseOrder.objects.get(id=id)

            if purchase_orders.vendor.user != request.user:
                return Response(
                    {
                        'responseCode': status.HTTP_403_FORBIDDEN,
                        'responseMessage': 'Forbidden - You are not authorized to complete this purchase order.',
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            purchase_order = get_object_or_404(PurchaseOrder, id=id, vendor=vendor)
            if purchase_order.status == 'acknowledged' or purchase_order.status == 'completed' or purchase_order.status == 'canceled':
                return Response(
                    {
                        'responseCode': status.HTTP_409_CONFLICT,
                        'responseMessage': 'Purchase order already acknowledged or cancelled.',
                    },
                    status=status.HTTP_409_CONFLICT
                )

            purchase_order.status = 'acknowledged'
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Purchase order acknowledged successfully.',
                },
                status=status.HTTP_200_OK
            )
        except PurchaseOrder.DoesNotExist:
            return Response(
                {
                    'responseCode': status.HTTP_404_NOT_FOUND,
                    'responseMessage': 'Purchase order not found.',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Internal server error.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

class IssuePurchaseOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token of consumer", type=openapi.TYPE_STRING ,default="Bearer"),
        ],
        responses={
            200: 'Purchase order issued successfully.',
            400: 'Bad request.',
            401: 'Unauthorized.',
            404: 'Purchase order not found.',
            409: 'Purchase order already issued.',
            500: 'Internal server error.'
        }
    )
    def post(self, request, purchase_order_id):
        try:
            
            # Check if the user has a consumer type
            if  request.user.user_type != 'Consumer':
                return Response(
                    {
                        'responseCode': status.HTTP_403_FORBIDDEN,
                        'responseMessage': 'Forbidden - Only consumers can issue a purchase order.',
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            
            consumer = request.user.consumer 

            purchase_orders = PurchaseOrder.objects.get(id=purchase_order_id)

            if purchase_orders.consumer.user != request.user:
                return Response(
                    {
                        'responseCode': status.HTTP_403_FORBIDDEN,
                        'responseMessage': 'Forbidden - You are not authorized to complete this purchase order.',
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            purchase_order = get_object_or_404(PurchaseOrder, id=purchase_order_id, consumer=consumer)

            if purchase_order.status in ['pending' ,'issued', 'acknowledged','canceled']:
                return Response(
                    {
                        'responseCode': status.HTTP_409_CONFLICT,
                        'responseMessage': 'Purchase order not completed.',
                    },
                    status=status.HTTP_409_CONFLICT
                )
            purchase_order.status = 'issued'
            purchase_order.issue_date = timezone.now()
            purchase_order.save()
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Purchase order issued successfully.',
                },
                status=status.HTTP_200_OK
            )
        except PurchaseOrder.DoesNotExist:
            return Response(
                {
                    'responseCode': status.HTTP_404_NOT_FOUND,
                    'responseMessage': 'Purchase order not found.',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Internal server error.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CompletePurchaseOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Bearer <token>', type=openapi.TYPE_STRING),
            openapi.Parameter('purchase_order_id', openapi.IN_PATH, description='ID of the purchase order to be completed', type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: 'Purchase order status updated to "completed".',
            400: 'Bad Request',
            403: 'Forbidden - You are not authorized to complete this purchase order.',
            404: 'Not Found - Purchase order does not exist.',
            409: 'Conflict - Purchase order status is already completed or cancelled.',
            500: 'Internal Server Error'
        }
    )
    def post(self, request, purchase_order_id):
        try:
            purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)

            if purchase_order.vendor.user != request.user:
                return Response(
                    {
                        'responseCode': status.HTTP_403_FORBIDDEN,
                        'responseMessage': 'Forbidden - You are not authorized to complete this purchase order.',
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            if purchase_order.status not in ['pending', 'acknowledged', 'issued']:
                return Response(
                    {
                        'responseCode': status.HTTP_409_CONFLICT,
                        'responseMessage': 'Purchase order status is already completed or cancelled.',
                    },
                    status=status.HTTP_409_CONFLICT
                )

            purchase_order.status = 'completed'
            purchase_order.completed_date = timezone.now()
            purchase_order.save()

            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Purchase order status updated to completed.',
                },
                status=status.HTTP_200_OK
            )

        except PurchaseOrder.DoesNotExist:
            return Response(
                {
                    'responseCode': status.HTTP_404_NOT_FOUND,
                    'responseMessage': 'Not Found - Purchase order does not exist.',
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Internal Server Error',
                    'responseData': {'error': 'Something went wrong! Please try again.'}
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class PerformanceMetricsAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'vendor_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the vendor'
                    )
            },
            required=['vendor_id']   
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'on_time_delivery_rate': openapi.Schema(type=openapi.TYPE_STRING, description='On-Time Delivery Rate'),
                    'quality_rating_avg': openapi.Schema(type=openapi.TYPE_NUMBER, description='Quality Rating Average'),
                    'average_response_time': openapi.Schema(type=openapi.TYPE_STRING, description='Average Response Time'),
                    'fulfillment_rate': openapi.Schema(type=openapi.TYPE_STRING, description='Fulfillment Rate'),
                }
            ),
            400: 'Bad Request',
            404: 'Vendor with this ID does not exist.',
            500: 'Internal Server Error'
        }
    )
    def post(self, request):
        try:
            vendor_id = request.data.get('vendor_id')

            if not vendor_id:
                return Response(
                    {
                        'responseCode': status.HTTP_400_BAD_REQUEST,
                        'responseMessage': 'Vendor ID is required.',
                        'responseData': None
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                vendor = Vendor.objects.get(id=vendor_id)
            except ObjectDoesNotExist:
                return Response(
                    {
                        'responseCode': status.HTTP_404_NOT_FOUND,
                        'responseMessage': 'Vendor not found.',
                        'responseData': None
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            on_time_delivery_rate = round(vendor.on_time_delivery_rate * 100, 2)
            quality_rating_avg = round(vendor.quality_rating_avg, 2)

            total_seconds = vendor.average_response_time
            days = total_seconds // (24 * 3600)
            total_seconds %= (24 * 3600)
            hours = total_seconds // 3600
            total_seconds %= 3600
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            average_response_time = f"{int(days)} days {int(hours)} hours {int(minutes)} mins {int(seconds)} seconds"

            fulfillment_rate = round(vendor.fulfillment_rate * 100, 2)

            return Response({
                'responseCode': status.HTTP_200_OK,
                'responseMessage': 'Performance metrics retrieved successfully.',
                'responseData': {
                    'on_time_delivery_rate': f"{on_time_delivery_rate}%",
                    'quality_rating_avg': quality_rating_avg,
                    'average_response_time': average_response_time,
                    'fulfillment_rate': f"{fulfillment_rate}%"
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Internal server error.',
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VendorHistoricalPerformance(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('vendor_id', openapi.IN_QUERY, description="Vendor ID", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('page_number', openapi.IN_QUERY, description="Page Number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Page Size", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response(description='Successful', schema=HistoricalPerformanceSerializer(many=True)),
            400: 'Bad request.',
            404: 'Vendor not found.',
            500: 'Internal server error.'
        }
    )
    def get(self, request):
        vendor_id = request.query_params.get('vendor_id')
        page_number = request.query_params.get('page_number', 1)
        page_size = request.query_params.get('page_size', 10)

        if not vendor_id:
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': 'Vendor ID is required.',
                    'responseData': None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except ObjectDoesNotExist:
            return Response(
                {
                    'responseCode': status.HTTP_404_NOT_FOUND,
                    'responseMessage': 'Vendor not found.',
                    'responseData': None
                },
                status=status.HTTP_404_NOT_FOUND
            )

        historical_performances = HistoricalPerformance.objects.filter(vendor=vendor).order_by('-id')
        paginator = Paginator(historical_performances, page_size)

        try:
            historical_performances_page = paginator.page(page_number)
        except PageNotAnInteger:
            historical_performances_page = paginator.page(1)
        except EmptyPage:
            historical_performances_page = paginator.page(paginator.num_pages)

        serializer = HistoricalPerformanceSerializer(historical_performances_page, many=True)
        response_data = serializer.data

        return Response(
            {
                'responseCode': status.HTTP_200_OK,
                'responseMessage': 'Success',
                'responseData': response_data
            },
            status=status.HTTP_200_OK
        )
        
#############
class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the item'),
                'available_quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Available quantity of the item'),
            }
        ),
        responses={
            201: 'Item created successfully.',
            400: 'Failed to create item.'
        }
    )
    def post(self, request):
        try:
            serializer = ItemCreateSerializer(data=request.data)
            if serializer.is_valid():
                vendor = Vendor.objects.get(user=request.user)
                serializer.save(vendor=vendor)                
                return Response(
                    {
                        'responseCode': status.HTTP_201_CREATED,
                        'responseMessage': 'Item created successfully.',
                        'responseData': serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        'responseCode': status.HTTP_400_BAD_REQUEST,
                        'responseMessage': 'Failed to create item.',
                        'responseData': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Vendor.DoesNotExist:
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': 'Vendor does not exist.',
                    'responseData': None
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': str(e),
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    


class ProductListAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Bearer', required=False,default='Bearer'),
            openapi.Parameter('product_name', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Filter by product name', required=False),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number', required=False),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page size', required=False),
        ],
        responses={
            200: "Items retrieved successfully",
            400: "Bad Request",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        try:
            product_name = request.query_params.get('product_name')
            page_number = request.query_params.get('page')
            page_size = request.query_params.get('page_size')

            if 'Authorization' in request.headers and request.headers['Authorization'].startswith('Bearer '):
                vendor = request.user.vendor
                items = Product.objects.filter(vendor=vendor)
                if product_name:
                    items = items.filter(product_name__icontains=product_name)
            else:
                items = Product.objects.all()
                if product_name:
                    items = items.filter(product__name_icontains=product_name)

            paginator = Paginator(items, page_size) if page_size else Paginator(items, 10)
            page_obj = paginator.get_page(page_number)

            serializer = ItemSerializer(page_obj, many=True)

            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Items retrieved successfully.',
                    'responseData': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Bearer <token>', required=True),
            openapi.Parameter('item_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='ID of the item to be updated', required=True),
            openapi.Parameter('product_name', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='New name of the item'),
            openapi.Parameter('available_quantity', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='New available quantity of the item'),
        ],
        responses={
            200: "Item updated successfully",
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def put(self, request):
        try:
            item_id = request.query_params.get('item_id')
            if not item_id:
                return Response(
                    {'responseCode': status.HTTP_400_BAD_REQUEST, 'responseMessage': 'Item ID is required in the query parameters.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                item = Product.objects.get(id=item_id)
            except Product.DoesNotExist:
                return Response(
                    {'responseCode': status.HTTP_404_NOT_FOUND, 'responseMessage': 'Item does not exist.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            product_name = request.query_params.get('product_name', item.product_name)
            available_quantity = request.query_params.get('available_quantity', item.available_quantity)

            if product_name:
                item.product_name = product_name
            if available_quantity is not None:
                item.available_quantity = available_quantity
            item.save()

            return Response(
                {'responseCode': status.HTTP_200_OK, 'responseMessage': 'Item updated successfully.'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR, 'responseMessage': 'Something went wrong! Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Bearer <token>', type=openapi.TYPE_STRING),
            openapi.Parameter('product_id', openapi.IN_PATH, description='ID of the Product to be deleted', type=openapi.TYPE_INTEGER)
        ],
        responses={
            204: 'Item deleted successfully.',
            400: 'Bad Request',
            403: 'Forbidden - You are not authorized to delete this item.',
            404: 'Not Found - Item does not exist or does not belong to you.',
            500: 'Internal Server Error'
        }
    )
    def delete(self, request, product_id):  
        try:
            item = Product.objects.get(id=product_id)

            if item.vendor.user == request.user:
                item.delete()
                return Response(
                    {'responseCode': status.HTTP_204_NO_CONTENT, 'responseMessage': 'Item deleted successfully.'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'responseCode': status.HTTP_403_FORBIDDEN, 'responseMessage': 'Forbidden - You are not authorized to delete this item.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        except Product.DoesNotExist:
            return Response(
                {'responseCode': status.HTTP_404_NOT_FOUND, 'responseMessage': 'Not Found - Item does not exist or does not belong to you.'},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR, 'responseMessage': 'Internal Server Error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

