import datetime
from datetime import timedelta
from typing import override

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from expenses import serializers

from .filters import ExpenseFilter
from .models import Expense
from .serializers import ExpenseSerializer, UserRegistrationSerializer


class UserRegistrationView(APIView):
    """
    API View for user registration.
    Allows unauthenticated users to create a new account via POST request.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """
        Handles POST requests for user registration.
        Validates data using UserRegistrationSerializer and creates a new user.
        """
        serializer = UserRegistrationSerializer(data=request.data)

        # Validate the serializer. If invalid, it raises a ValidationError,
        # which DRF catches and returns as a 400 Bad Request response automatically.
        serializer.is_valid(raise_exception=True)

        # If validation passes, save the serializer
        user = serializer.save()

        # Prepare a success response
        response_data = {
            'message': 'User registered sucessfully',
            'user':{
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Expense instances.
    Provides list, create, retrieve, update, partial_update, and destroy actions.
    """

    serializer_class = ExpenseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = ExpenseFilter
    
    @override
    def get_queryset(self):
        """
        This view should return only expenses for the currently authenticated user.
        """
        user = self.request.user
        queryset = Expense.objects.filter(user=user) # Base queryset filtered by user

        time_period = self.request.query_params.get('time_period')

        if time_period:
            today = datetime.date.today()
            start_date = None

            if time_period == 'past_week':
                start_date = today - timedelta(days=7)
            elif time_period == 'last_month':
                start_date = today - timedelta(days=30)
            elif time_period == 'last_3_months':
                start_date = today - timedelta(days=90)

            if start_date:
                queryset = queryset.filter(date__gte=start_date, date__lte=today)
            else:
                print(f"Warning: Unrecognized time_period '{time_period}'")

        queryset = queryset.order_by('-date', '-created_at')
        return queryset


    @override
    def perform_create(self,serializer):
        """
        Assign the authenticated user to the expense instance upon creation.
        """
        serializer.save(user=self.request.user)

