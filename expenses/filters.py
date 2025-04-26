
import django_filters

from .models import Expense


class ExpenseFilter(django_filters.FilterSet):
    """
    FilterSet for the Expense model.
    Allows filtering by date range (gte, lte) and category.
    """
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact') # Example: ?date=2025-04-26
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte') # Example: ?start_date=2025-04-01
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')   # Example: ?end_date=2025-04-30


    class Meta:
        model = Expense # Specify the model this FilterSet is for
        fields = {
            'category': ['exact'], # Allows filtering by category ID: ?category=1
            'amount': ['exact', 'gte', 'lte'], # Optionally allow filtering by amount range: ?amount__gte=50
        }
