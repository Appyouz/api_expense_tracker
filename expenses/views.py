from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from expenses import serializers

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
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = (permissions.IsAuthenticated,)
