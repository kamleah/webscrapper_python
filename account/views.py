from django.shortcuts import render

# """ Import from rest framework here """

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.settings import api_settings
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics

# """ Import from django here """

from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from django.contrib.auth import authenticate

""" Import Django Filters """
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

# """ Import models here """
from django.contrib.auth.models import User
from django.db.models import Q
from .models import UserRoleModel, RoleModel, CustomUser

# """ Import from forms """
from .forms import LoginForm, RegistrationForm

# """ Debugger Import """
import pdb

# """ Import from Utils here """
from utils.response import (
    create_bad_request_response,
    create_internal_server_error_response,
    create_success_response,
)
from utils.helper_function import BasicPagination

# """ Import from account app here """
from account.tokens import create_jwt_pair_for_user

# """ Import Serializers here """
from .serializers import (
    UserViewSerializer,
    UserListViewSerializer,
    UserRegistrationSerializer,
    RoleModelSerializer,
    GetUserDetailSerializer,
    PutUserDetailSerializer
)

# """ Import schema here """
from .schema import registration_schema, login_schema

""" Import Swagger here """
from drf_yasg.utils import swagger_auto_schema

class UserRegistrationView(APIView):
    """API for User Registration"""

    @swagger_auto_schema(
        tags=["Account Auth"],
        request_body=registration_schema["request_body"],
        responses=registration_schema["responses"],
    )
    def post(self, request):
        try:
            # Validate registration form
            registration_form = RegistrationForm(data=request.data)
            if not registration_form.is_valid():
                return create_bad_request_response(errors=registration_form.errors)

            role_id, created_by = request.data.get("user_role"), request.data.get(
                "user_created_by"
            )

            # Validate role and created_by user existence
            if not RoleModel.objects.filter(id=role_id).exists():
                return create_bad_request_response(message="Invalid role ID provided")

            if not CustomUser.objects.filter(id=created_by).exists():
                return create_bad_request_response(
                    message="Invalid created by ID provided"
                )

            # Validate and save user
            user_serializer = UserRegistrationSerializer(data=request.data)
            if not user_serializer.is_valid():
                return create_bad_request_response(errors=user_serializer.errors)

            user = user_serializer.save()
            return create_success_response(message="Registration successful")

        except Exception as e:
            return create_internal_server_error_response(exception=e)

class UserRegistrationEditView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user_id = kwargs["user_id"]
            user_details = CustomUser.objects.get(id = user_id)
            serialized_user_details = GetUserDetailSerializer(user_details).data
            user_data = serialized_user_details
            del user_data["password"]
            del user_data["username"]
            del user_data["is_staff"]
            del user_data["groups"]
            del user_data["user_permissions"]
            return create_success_response(message="Registration successful", data=user_data)
        except CustomUser.DoesNotExist:
            return create_bad_request_response(errors="User Does Not Exists")
        except Exception as e:
            return create_internal_server_error_response(exception=e)
    
    def put(self, request, *args, **kwargs):
        try:
            user_id = kwargs["user_id"]
            user_details = CustomUser.objects.get(id = user_id)
            serialized_user_details = PutUserDetailSerializer(user_details, data=request.data)
            if serialized_user_details.is_valid():
                serialized_user_details.save()
                user_data = serialized_user_details.data

                del user_data["password"]
                del user_data["username"]
                del user_data["is_staff"]
                del user_data["groups"]
                del user_data["user_permissions"]

                return create_success_response(message="User Details Update Successfull", data=user_data)
            else:
                return create_bad_request_response(errors=serialized_user_details.errors)
        
        except Exception as e:
            return create_internal_server_error_response(exception=e)
        
    def delete(self, request, *args, **kwargs):
        try:
            user_id = kwargs["user_id"]
            user_details = CustomUser.objects.get(id = user_id)
            user_details.delete()
            return create_success_response(message="User Details Deleted Successfull")
        
        except CustomUser.DoesNotExist:
            return create_bad_request_response(errors="User Does Not Exists")
        
        except Exception as e:
            return create_internal_server_error_response(exception=e)


class UserLoginView(APIView):
    @swagger_auto_schema(
        tags=["Account Auth"],
        request_body=login_schema["request_body"],
        responses=login_schema["responses"],
    )
    def post(self, request):
        try:
            data = request.data
            login_form = LoginForm(data)
            if not login_form.is_valid():
                return create_bad_request_response(errors=login_form.errors)
            email = request.data.get("email")
            password = request.data.get("password")
            user = CustomUser.objects.filter(email__iexact=email).first()
            if user is not None:
                if check_password(password, user.password):
                    tokens = create_jwt_pair_for_user(user)
                    user_data = UserViewSerializer(user).data

                    CustomUser.objects.filter(email__iexact=user.email).update(
                        last_login=timezone.now()
                    )

                    del user_data["password"]
                    del user_data["username"]
                    del user_data["is_staff"]
                    del user_data["groups"]
                    del user_data["user_permissions"]

                    user_data["access"] = tokens["access"]
                    user_data["refresh"] = tokens["refresh"]
                    return create_success_response(
                        message="Login is successfull", data=user_data
                    )
                else:
                    return create_bad_request_response(message="Invalid credentials")
            else:
                return create_bad_request_response(message="Invalid credentials")
        except Exception as e:
            return create_internal_server_error_response(e)


class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr="icontains")
    last_name = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")
    user_role = django_filters.CharFilter(
        lookup_expr="icontains", field_name="user_role__name"
    )
    user_created_by = django_filters.CharFilter(method="filter_created_by")

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "user_role", "user_created_by"]

    def filter_created_by(self, queryset, name, value):
        """
        Filter by user_created_by's email, first_name, or last_name in a single filter.
        """
        return queryset.filter(
            Q(user_created_by__email__icontains=value) |
            Q(user_created_by__first_name__icontains=value) |
            Q(user_created_by__last_name__icontains=value)
        )


# """ API to list admin user with filter """

@swagger_auto_schema(tags=["Search Users"])
class UserPaginatedListView(generics.ListAPIView):
    queryset = CustomUser.objects.all().order_by("id")
    serializer_class = UserListViewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    pagination_class = BasicPagination


class RoleView(APIView):
    @swagger_auto_schema(
        tags=["Account Auth"],
    )
    def get(self, request):
        try:
            roles = RoleModel.objects.all()
            serialized_roles = RoleModelSerializer(roles, many=True).data
            return create_success_response(message="Roles fetched successfully", data=serialized_roles)
        except Exception as error:
            return create_internal_server_error_response(error)