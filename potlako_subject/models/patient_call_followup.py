from datetime import timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_is_future
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO
from edc_protocol.validators import date_not_before_study_start

from ..choices import DATE_ESTIMATION, APPT_CHANGE_REASON
from ..choices import DISPOSITION, FACILITY, SCALE, PAIN_SCORE
from .list_models import CallAchievements
from .model_mixins import CrfModelMixin


class PatientCallFollowUp(CrfModelMixin):

    encounter_date = models.DateField(
        verbose_name='Date of research staff encounter',
        validators=[date_not_future])

    start_time = models.TimeField(
        verbose_name='Patient follow up: start time',
    )

    patient_residence_change = models.CharField(
        verbose_name=('Has there been any change in patient '
                      'residence and contact information?'),
        choices=YES_NO,
        max_length=3)

    next_kin_contact_change = models.CharField(
        verbose_name=('Any changes to be made to next of kin contact '
                      'information?'),
        choices=YES_NO,
        max_length=3)

    perfomance_status = models.IntegerField(
        verbose_name='Patient performance status',
        default=1,
        choices=SCALE,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    pain_score = models.IntegerField(
        verbose_name='Patient pain score',
        default=0,
        choices=PAIN_SCORE,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    new_complaints = models.CharField(
        verbose_name=('Does the patient have any new complaints?'),
        choices=YES_NO,
        max_length=3)

    new_complaints_description = models.TextField(
        verbose_name=('If yes, please describe'),
        max_length=100,
        blank=True,
        null=True)

    interval_visit = models.CharField(
        verbose_name=('Has there been an interval visit(s) to any facility(s) '
                      'since the enrollment visit?'),
        choices=YES_NO,
        max_length=3,
        help_text=('If yes, details should be verified with clinician at next '
                   'clinician check-in call and reconciled with clinician '
                   'call encounter records'))

    facility_visited_count = models.IntegerField(
        verbose_name='How many facilities were visited?',
        default=0,
        validators=[MinValueValidator(0)])

    last_visit_date = models.DateField(
        verbose_name='When was your last clinic visit?',
        validators=[date_not_future, ])

    last_visit_date_estimated = models.CharField(
        verbose_name='Is the last visit date estimated?',
        choices=YES_NO,
        max_length=3)

    last_visit_date_estimation = models.CharField(
        verbose_name='Which part of the date was estimated, if any?',
        choices=DATE_ESTIMATION,
        max_length=15,
        blank=True,
        null=True,)

    last_visit_facility = models.CharField(
        verbose_name='Which health facility did the patient visit?',
        max_length=30)

    appt_change = models.CharField(
        verbose_name=('Since we last talked, has the patient\'s appointment '
                      'changed?'),
        max_length=3,
        choices=YES_NO)

    appt_change_reason = models.CharField(
        verbose_name='If yes, how was the appointment changed?',
        max_length=30,
        choices=APPT_CHANGE_REASON,
        blank=True,
        null=True,)

    appt_change_reason_other = OtherCharField()

    investigation_ordered = models.CharField(
        verbose_name=('Have there been any interval investigations '
                      'ordered or resulted?'),
        choices=YES_NO,
        max_length=3,
        help_text='(IF YES, COMPLETE \'INVESTIGATION FORM\')')

    transport_support = models.CharField(
        verbose_name=('Does the patient need transport support?'),
        choices=YES_NO,
        max_length=3,
        help_text='(IF YES, COMPLETE \'TRANSPORT FORM\')')

    next_appointment_date = models.DateField(
        verbose_name='Next appointment date (per patient report)',
        validators=[date_is_future])

    next_ap_facility = models.CharField(
        verbose_name='Next appointment facility and type',
        choices=FACILITY,
        max_length=40)

    next_ap_facility_other = OtherCharField()

    transport_support_received = models.CharField(
        verbose_name=('Did patient receive expected transportation support '
                      'for his/her last visit?'),
        choices=YES_NO,
        max_length=3,
        help_text='e.g. funds transferred, vehicle arrived, etc.')

    transport_details = models.TextField(
        verbose_name=('Please provide details'),
        max_length=100,
        blank=True,
        null=True)

    clinician_communication_issues = models.CharField(
        verbose_name=('Has there been any issues in communicating with '
                      'clinicians, or with the patient\'s care in general?'),
        choices=YES_NO,
        max_length=3)

    clinician_issues_details = models.TextField(
        verbose_name=('Please provide details'),
        max_length=100,
        blank=True,
        null=True)

    communication_issues = models.CharField(
        verbose_name=('Has there been any issues in communicating with '
                      'research team?'),
        choices=YES_NO,
        max_length=3)

    issues_details = models.TextField(
        verbose_name=('Please provide details'),
        max_length=100,
        blank=True,
        null=True)

    other_issues = models.CharField(
        verbose_name='Has there been any other issues?',
        choices=YES_NO,
        max_length=3)

    other_issues_details = models.TextField(
        verbose_name=('Please provide details'),
        max_length=100,
        blank=True,
        null=True)

    call_achievements = models.ManyToManyField(
        CallAchievements,
        verbose_name='What has been achieved during the call')

    medical_evaluation_understanding = models.CharField(
        verbose_name=('Does patient have fair understanding of next '
                      'steps regarding medical evaluation?'),
        choices=YES_NO,
        max_length=3)

    next_step_understanding = models.TextField(
        verbose_name=('Give a detailed summary of the pateint\'s understanding '
                      'of the next steps (details)'),
        max_length=100,
        blank=True,
        null=True)

    sms_received = models.CharField(
        verbose_name=('Did patient receive SMS reminder for last scheduled '
                      'visit?'),
        choices=YES_NO,
        max_length=3)

    additional_comments = models.TextField(
        verbose_name='Provide any additional comments',
        max_length=100,
        blank=True,
        null=True)

    patient_followup_end_time = models.TimeField(
        verbose_name='Patient follow up: end time',
    )

    encounter_duration = models.DurationField(
        verbose_name='Duration of encounter',
        help_text='Minutes'
    )

    def get_call_duration(self):
        call_end = timedelta(hours=self.patient_followup_end_time.hour,
                             minutes=self.patient_followup_end_time.minute,
                             seconds=self.patient_followup_end_time.second,
                             microseconds=self.patient_followup_end_time.microsecond)

        call_start = timedelta(hours=self.start_time.hour,
                               minutes=self.start_time.minute,
                               seconds=self.start_time.second,
                               microseconds=self.start_time.microsecond)

        return call_end - call_start

    def save(self, *args, **kwargs):
        self.encounter_duration = self.get_call_duration()
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Patient call - FollowUp'


class FacilityVisit(BaseUuidModel):

    patient_call_followup = models.ForeignKey(PatientCallFollowUp, on_delete=PROTECT)

    interval_visit_date = models.DateField(
        verbose_name='Date of interval visit',
        validators=[date_not_before_study_start, date_not_future],
        null=True,
        blank=True)

    interval_visit_date_estimated = models.CharField(
        verbose_name='Is the interval visit date estimated?',
        choices=YES_NO,
        max_length=3)

    interval_visit_date_estimation = models.CharField(
        verbose_name='Which part of the date was estimated, if any?',
        choices=DATE_ESTIMATION,
        max_length=15,
        blank=True,
        null=True,
    )

    visit_facility = models.CharField(
        verbose_name=('What facility was visited (per patient report)?'),
        choices=FACILITY,
        max_length=40)

    visit_facility_other = OtherCharField()

    visit_reason = models.CharField(
        verbose_name=('What was the reason for the visit?'),
        max_length=50,
        null=True,
        blank=True)

    visit_outcome = models.CharField(
        verbose_name='What was the outcome of the visit?',
        choices=DISPOSITION,
        max_length=15)

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Facility Visit'
        unique_together = ('patient_call_followup', 'interval_visit_date',
                           'visit_facility')
