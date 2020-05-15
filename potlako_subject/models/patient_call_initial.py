from datetime import timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import PROTECT
from django_crypto_fields.fields import EncryptedCharField
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import CellNumber
from edc_base.model_validators import date_not_future
from edc_constants.choices import POS_NEG_UNKNOWN, YES_NO_NA
from edc_constants.choices import YES_NO, YES_NO_UNSURE
from edc_constants.constants import NOT_APPLICABLE
from edc_protocol.validators import date_not_before_study_start

from ..choices import DATE_ESTIMATION, ENROLLMENT_VISIT_METHOD, FACILITY
from ..choices import DURATION, FACILITY_UNIT, SEVERITY_LEVEL, DISTRICT
from ..choices import PAIN_SCORE, SCALE, EDUCATION_LEVEL, WORK_TYPE
from ..choices import PATIENT_RESIDENCE, UNEMPLOYED_REASON
from .list_models import CallAchievements, TestType
from .model_mixins import CrfModelMixin


class PatientCallInitial(CrfModelMixin):

    patient_call_time = models.TimeField(
        verbose_name='Start of patient initial call (timestamp)')

    patient_call_date = models.DateField(
        verbose_name='Date of initial patient call',
        validators=[date_not_before_study_start, date_not_future])

    age_in_years = models.IntegerField(
        verbose_name='Patient age',
        help_text='(Years)',)

    residential_district = models.CharField(
        verbose_name='where does the patient currently live?',
        choices=DISTRICT,
        max_length=50,
        blank=True,
        null=True)

    patient_kgotla = models.CharField(
        verbose_name='What is the name of the ward where the patient resides?',
        max_length=30,
        blank=True,
        null=True)

    primary_clinic = models.CharField(
        verbose_name=('Nearest primary clinic or health post '
                      'to where patient resides'),
        choices=FACILITY,
        max_length=40)

    primary_clinic_other = OtherCharField()

    education_level = models.CharField(
        verbose_name='What is your highest level of education',
        max_length=15,
        choices=EDUCATION_LEVEL)

    work_status = models.CharField(
        verbose_name='Is the patient currently working?',
        choices=YES_NO,
        max_length=3)

    work_type = models.CharField(
        verbose_name='What kind of work does the patient do?',
        choices=WORK_TYPE,
        max_length=30,
        blank=True,
        null=True)

    work_type_other = OtherCharField()

    unemployed_reason = models.CharField(
        verbose_name='Why is the patient not working?',
        choices=UNEMPLOYED_REASON,
        max_length=30,
        blank=True,
        null=True)

    unemployed_reason_other = OtherCharField()

    social_welfare = models.CharField(
        verbose_name='Is the patient on social welfare support?',
        choices=YES_NO_NA,
        max_length=30,
        default=NOT_APPLICABLE)

    social_welfare = models.CharField(
        verbose_name='Does the patient have any other medical conditions?',
        choices=YES_NO,
        max_length=3)

    patient_residence = models.CharField(
        verbose_name='Who does the patient stay with?',
        choices=PATIENT_RESIDENCE,
        max_length=30,
        blank=True,
        null=True)

    patient_residence_other = OtherCharField()

    patient_contact_change = models.CharField(
        verbose_name=('Any changes to be made to patient contact '
                      ' information (patient phone) since index visit?'),
        choices=YES_NO,
        max_length=3)

    patient_residence_change = models.CharField(
        verbose_name=('Any changes to be made to patient residence '
                      'information since index visit?'),
        choices=YES_NO,
        max_length=3)

    nok_change = models.CharField(
        verbose_name='Any changes to be made to next of kin information?',
        choices=YES_NO,
        max_length=3)

    patient_symptoms = models.TextField(
        max_length=250,
        verbose_name=('What symptom(s) is the patient having for which '
                      'they were seen at the clinic 1 week ago?')
    )

    patient_symptoms_date = models.DateField(
        verbose_name=('Date the symptoms started'),
        validators=[date_not_future, ])

    patient_symptoms_date_estimated = models.CharField(
        verbose_name='Is the symptoms date estimated?',
        choices=YES_NO,
        max_length=3)

    patient_symptoms_date_estimation = models.CharField(
        verbose_name='Which part of the date was estimated, if any?',
        choices=DATE_ESTIMATION,
        max_length=15,
        blank=True,
        null=True,
    )

    symptoms_duration_report = models.IntegerField(
        verbose_name=('How long did it take for the participant to present to '
                      'the facility after experiencing their first symptom?'),
        default=0,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )

    symptoms_duration = models.CharField(
        verbose_name='What is the above number for?',
        choices=DURATION,
        max_length=6,
        blank=True,
        null=True,)

    other_facility = models.CharField(
        verbose_name=('Before enrollment visit, has the patient been '
                      'seen for similar symptoms at other facilities?'),
        choices=YES_NO,
        max_length=3)

    facility_number = models.IntegerField(
        verbose_name='How many facilities?',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        blank=True,
        null=True,
    )

    perfomance_status = models.IntegerField(
        verbose_name='Patient performance status',
        choices=SCALE,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    pain_score = models.IntegerField(
        verbose_name='Patient pain score',
        choices=PAIN_SCORE,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    hiv_status = models.CharField(
        verbose_name=('What is patient\'s current HIV status?'),
        choices=POS_NEG_UNKNOWN,
        max_length=10)

    hiv_test_date = models.DateField(
        verbose_name=('When was patient\'s last HIV test?'),
        validators=[date_not_future, ],
        blank=True,
        null=True,
        help_text=('If positive test, date of positive test, if negative, '
                   'date of most recent negative test'))

    hiv_test_date_estimated = models.CharField(
        verbose_name='Is the HIV test date estimated?',
        choices=YES_NO,
        max_length=3)

    hiv_test_date_estimation = models.CharField(
        verbose_name='Which part of the date was estimated, if any?',
        choices=DATE_ESTIMATION,
        max_length=15,
        blank=True,
        null=True,
    )

    cancer_suspicion_known = models.CharField(
        verbose_name=('Is patient aware that cancer is suspected '
                      'as a diagnosis?'),
        choices=YES_NO,
        max_length=3)

    enrollment_visit_method = models.CharField(
        verbose_name=('How did patient get to enrollment clinic visit?'),
        choices=ENROLLMENT_VISIT_METHOD,
        max_length=30)

    enrollment_visit_method_other = OtherCharField()

    slh_travel = models.CharField(
        verbose_name=('If you had to travel to (referral facility) to see a '
                      'doctor, how would you go about it?'),
        max_length=50,
        help_text='Use referral clinic name')

    tests_ordered = models.CharField(
        verbose_name=('Does patient report any tests being ordered or '
                      'done at or since enrollment visit?'),
        choices=YES_NO_UNSURE,
        max_length=8)

    tests_type = models.ManyToManyField(
        TestType,
        verbose_name=('If yes, type of test'),
        max_length=15,
        blank=True)

    tests_type_other = OtherCharField(
        verbose_name='If other, specify and describe if possible',
        max_length=15,
        blank=True,
        null=True)

    next_appointment_date = models.DateField(
        verbose_name='Next appointment date (per patient report)')

    next_ap_facility = models.CharField(
        verbose_name='Next appointment facility',
        choices=FACILITY,
        max_length=40,
        help_text='per patient report')

    next_ap_facility_other = OtherCharField()

    next_ap_facility_unit = models.CharField(
        choices=FACILITY_UNIT,
        max_length=20)

    next_ap_facility_unit_other = OtherCharField(
        max_length=50)

    transport_support = models.CharField(
        verbose_name=('Has patient expressed need for transport support?'),
        choices=YES_NO,
        max_length=3,
        help_text='IF YES, COMPLETE TRANSPORT FORM')

    call_achievements = models.ManyToManyField(
        CallAchievements,
        verbose_name='What has been achieved during the call')

    call_achievements_other = OtherCharField(
        max_length=100)

    comments = models.TextField(
        verbose_name=('Any other general comments regarding patient encouter'),
        max_length=100,
        blank=True,
        null=True)

    cancer_probability = models.CharField(
        verbose_name='Cancer probability (baseline)',
        choices=SEVERITY_LEVEL,
        max_length=10)

    initial_call_end_time = models.TimeField(
        verbose_name='End of patient initial call (timestamp)',
    )

    call_duration = models.DurationField(
        verbose_name='Duration of patient initial call',
    )

    def get_call_duration(self):
        call_end = timedelta(hours=self.initial_call_end_time.hour,
                             minutes=self.initial_call_end_time.minute,
                             seconds=self.initial_call_end_time.second,
                             microseconds=self.initial_call_end_time.microsecond)

        call_start = timedelta(hours=self.patient_call_time.hour,
                               minutes=self.patient_call_time.minute,
                               seconds=self.patient_call_time.second,
                               microseconds=self.patient_call_time.microsecond)

        return call_end - call_start

    def save(self, *args, **kwargs):
        self.call_duration = self.get_call_duration()
#         age_delta = age(self.dob, get_utcnow())
#         self.age_in_years = age_delta.years
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Patient call - Initial'
        verbose_name_plural = 'Patient call - Initial'


class PreviousFacilityVisit(BaseUuidModel):

    patient_call_initial = models.ForeignKey(PatientCallInitial, on_delete=PROTECT)

    facility_visited = models.CharField(
        choices=FACILITY,
        verbose_name=('Which facilities has the patient '
                      'been seen for similar symptoms?'),
        max_length=40,
        blank=True,
        help_text='(select all that apply)',)

    facility_visited_other = OtherCharField(
        max_length=30,
        blank=True,
        null=True)

    previous_facility_period = models.CharField(
        verbose_name=('For how long was he/she seen at facilities '
                      'before enrollment visit?'),
        max_length=15,
        blank=True,
        null=True,
        help_text='specify variable (days, weeks, months, years)')
