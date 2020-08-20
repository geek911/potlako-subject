from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import CancerDiagnosisAndTreatmentAssessmentForm
from ..models import CancerDiagnosisAndTreatmentAssessment

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(CancerDiagnosisAndTreatmentAssessment, site=potlako_subject_admin)
class CancerDiagnosisAndTreatmentAssessmentAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CancerDiagnosisAndTreatmentAssessmentForm

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'report_datetime',
                       'cancer_evaluation',
                       'diagnosis_date',
                       'diagnosis_date_estimated',
                       'diagnosis_date_estimation',
                       'clinical_impression',
                       'final_cancer_diagnosis',
                       'final_cancer_diagnosis_other',
                       'non_cancer_diagnosis',
                       'non_cancer_diagnosis_other',
                       'cancer_diagnosis',
                       'cancer_histology_code',
                       'cancer_diagnosis_stage',
                       'tumor_stage',
                       'nodal_stage',
                       'distant_metastasis_stage',
                       'cancer_therapy',
                       'treatment_intent',
                       'therapeutic_surgery',
                       'surgery_date',
                       'surgery_date_estimated',
                       'surgery_date_estimation',
                       'chemotherapy',
                       'chemotherapy_date',
                       'chemotherapy_date_estimated',
                       'chemotherapy_date_estimation',
                       'radiation',
                       'radiation_date',
                       'radiation_date_estimated',
                       'radiation_date_estimation'),
        }),
    )

    radio_fields = {
        'cancer_evaluation': admin.VERTICAL,
        'diagnosis_date_estimated': admin.VERTICAL,
        'diagnosis_date_estimation': admin.VERTICAL,
        'clinical_impression': admin.VERTICAL,
        'diagnosis_date_estimated': admin.VERTICAL,
        'final_cancer_diagnosis': admin.VERTICAL,
        'non_cancer_diagnosis': admin.VERTICAL,
        'cancer_diagnosis_stage': admin.VERTICAL,
        'tumor_stage': admin.VERTICAL,
        'nodal_stage': admin.VERTICAL,
        'distant_metastasis_stage': admin.VERTICAL,
        'cancer_therapy': admin.VERTICAL,
        'treatment_intent': admin.VERTICAL,
        'therapeutic_surgery': admin.VERTICAL,
        'surgery_date_estimated': admin.VERTICAL,
        'surgery_date_estimation': admin.VERTICAL,
        'chemotherapy': admin.VERTICAL,
        'chemotherapy_date_estimated': admin.VERTICAL,
        'chemotherapy_date_estimation': admin.VERTICAL,
        'radiation': admin.VERTICAL,
        'radiation_date_estimated': admin.VERTICAL,
        'radiation_date_estimation': admin.VERTICAL,
    }