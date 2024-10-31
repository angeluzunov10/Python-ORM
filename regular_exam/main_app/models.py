from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from main_app.managers import AstronautManager
from main_app.validators import validate_phone_number


# Create your models here.


class Astronaut(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            validate_phone_number
        ]
    )

    is_active = models.BooleanField(default=True)

    date_of_birth = models.DateField(null=True, blank=True)

    spacewalks = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    updated_at = models.DateTimeField(auto_now=True)

    objects = AstronautManager()


class Spacecraft(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )

    manufacturer = models.CharField(max_length=100)

    capacity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    weight = models.FloatField(
        validators=[
            MinValueValidator(0.0)
        ]
    )

    launch_date = models.DateField()

    updated_at = models.DateTimeField(auto_now=True)


class Mission(models.Model):
    class StatusChoices(models.TextChoices):
        PLANNED = 'Planned', 'Planned'
        ONGOING = 'Ongoing', 'Ongoing'
        COMPLETED = 'Completed', 'Completed'

    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )

    description = models.TextField(null=True, blank=True)

    status = models.CharField(
        max_length=9,
        choices=StatusChoices.choices,
        default=StatusChoices.PLANNED
    )

    launch_date = models.DateField()

    updated_at = models.DateTimeField(auto_now=True)

    spacecraft = models.ForeignKey(     # ManyToOne
        to=Spacecraft,
        on_delete=models.CASCADE,
        related_name='spacecraft_mission'
    )

    astronauts = models.ManyToManyField(Astronaut, related_name='missions')

    commander = models.ForeignKey(      # ManyToOne
        to=Astronaut,
        on_delete=models.SET_NULL,
        related_name='commander_mission',
        null=True,
        blank=True
    )



