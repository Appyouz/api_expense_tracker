from typing import override

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
