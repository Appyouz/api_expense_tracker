from django.conf import settings
from django.db import models


class ExpenseCategory(models.Model):
    """
    Represents a category for expenses (e.g., Groceries, Leisure).
    """
    name = models.CharField(max_length=100, unique=True)
     
    class Meta:
        verbose_name_plural = 'Expense Categories'

    def __str__(self) -> str:
        """
        Represents a category for expenses (e.g., Groceries, Leisure).
        """
        return self.name

class Expense(models.Model):
    """
    Represents a single expense record for a user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        """
        String representation of the expense.
        """
        category_name = self.category.name if self.category else "Ucategorized"
        return f"{self.user.username} (${self.amount}) - {category_name} - {self.date}"
