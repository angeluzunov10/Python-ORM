from django.core.exceptions import ValidationError


def validate_phone_number(value):
    for v in value:
        if not v.isdigit():
            raise ValidationError('Value must be a digit')
