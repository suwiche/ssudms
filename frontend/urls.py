from django.urls import path

from . views import index_page, records, generate_form, add_new_record, generate_report, account_settings, forms_page, \
    view_record, update_record, forms_page, summary_report, update_charts, update_sms, forms_versions_page


urlpatterns = [
    path('', index_page, name='frontend-index-page'),
    path('update_charts/<slug:type>/<slug:action>/<int:year>', update_charts, name='frontend-update-charts-page'),
    path('update_sms/', update_sms, name='frontend-update-sms-page'),

    path('records/', records, name='frontend-records'),
    path('records/<slug:acronym>', records, name='frontend-records'),
    path('records/<slug:acronym>/<slug:action>', records, name='frontend-records'),
    path('new/form/<str:acronym>', generate_form, name='frontend-generate-form'),

    path('newrecords/add/', add_new_record, name='frontend-add-new-record'),
    path('newrecords/add/<slug:action>', add_new_record, name='frontend-add-new-record'),

    path('view_record', view_record, name='frontend-view'),
    path('view_record/<str:acronym>', view_record, name='frontend-view'),
    path('view_record/<str:acronym>/<slug:action>/<int:pk>', view_record, name='frontend-view'),

    path('update_record/<slug:action>', update_record, name='frontend-update'),

    path('generate_report/', generate_report, name='frontend-generate-report'),
    path('generate_report/<slug:type>/<slug:filter>', generate_report, name='frontend-generate-report'),
    path('summary_report/', summary_report, name='frontend-summary-report'),

    path('account-settings/<str:action>', account_settings, name='frontend-account-settings'),

    path('forms/', forms_page, name='frontend-forms'),
    path('forms/<slug:action>/<int:pk>', forms_page, name='frontend-forms'),

    path('forms-versions/', forms_versions_page, name='frontend-forms-versions'),
    path('forms-versions/<slug:action>/<int:pk>', forms_versions_page, name='frontend-forms-versions'),

]