from django.db import models
from django.utils import timezone
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_is_future, datetime_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_constants.choices import YES_NO

from ..choices import RESULTS_PERSONNEL, SPECIALIST_CLINIC


class BaselineRoadMap(SiteModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=timezone.now,
        validators=[datetime_not_future, ],
        help_text='Date and time of report.')

    investigations_turnaround_time = models.DateField(
        verbose_name='What is the investigations turn-around time?',
        validators=[date_is_future, ])

    specialty_clinic = models.CharField(
        verbose_name='Does the patient need a specialty clinic?',
        max_length=3,
        choices=YES_NO)

    specialist_clinic_type = models.CharField(
        verbose_name='If yes, which specialist clinic?',
        max_length=15,
        choices=SPECIALIST_CLINIC,
        blank=True,
        null=True,)

    specialist_clinic_type_other = OtherCharField()

    specialist_turnaround_time = models.DateField(
        verbose_name='What is the specialist clinic turn-around time?',
        validators=[date_is_future, ],
        blank=True,
        null=True,)

    results_review_personnel = models.CharField(
        verbose_name=('Who is responsible for next patient\'s appointment'
                      '/results review?'),
        max_length=10,
        choices=RESULTS_PERSONNEL)

    results_review_personnel_other = OtherCharField()

    review_turnaround_time = models.DateField(
        verbose_name='What is the results review turn-around time?',
        validators=[date_is_future, ])

    oncology_visit = models.DateField(
        verbose_name='When is the expected oncology visit?',
        validators=[date_is_future, ])

    oncology_turnaround_time = models.DateField(
        verbose_name='What is the oncology visit turn-around time?',
        validators=[date_is_future, ])

    treatment_initiation_visit = models.DateField(
        verbose_name='When is the expected treatment initiation visit?',
        validators=[date_is_future, ])

    treatment_initiation_turnaround_time = models.DateField(
        verbose_name='What is the treatment initiation visit turn-around time?',
        validators=[date_is_future, ])
