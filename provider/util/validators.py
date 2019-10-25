"""
Validators for numeric values go here
"""
from django.core.validators import MinValueValidator, MaxValueValidator

NOT_NEGATIVE_VALIDATOR = [
    MinValueValidator(0)
]