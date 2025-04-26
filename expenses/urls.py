from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExpenseViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('', include(router.urls)),
]
