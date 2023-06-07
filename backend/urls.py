from django.urls import path

from .views import users_page, extensions_page, process_page, services_page, types_page, status_page, level_page, \
    index_page, details_attribute_page, get_citymun, get_barangay, worker_attribute_page

urlpatterns = [
    path('', index_page, name='backend-index-page'),

    path('users/', users_page, name='backend-users-page'),
    path('users/<slug:action>/<int:pk>', users_page, name='backend-users-page'),

    path('extensions/', extensions_page, name='backend-extensions-page'),
    path('extensions/<slug:action>/<int:pk>', extensions_page, name='backend-extensions-page'),

    path('process/', process_page, name='backend-process-page'),
    path('process/<slug:action>/<int:pk>', process_page, name='backend-process-page'),

    path('services/', services_page, name='backend-services-page'),
    path('services/<slug:action>/<int:pk>', services_page, name='backend-services-page'),

    path('types/', types_page, name='backend-types-page'),
    path('types/<slug:action>/<int:pk>', types_page, name='backend-types-page'),

    path('status/', status_page, name='backend-status-page'),
    path('status/<slug:action>/<int:pk>', status_page, name='backend-status-page'),

    path('level/', level_page, name='backend-level-page'),
    path('level/<slug:action>/<int:pk>', level_page, name='backend-level-page'),

    path('details-attribute/', details_attribute_page, name='backend-details-attribute-page'),
    path('details-attribute/<slug:action>/<int:pk>', details_attribute_page, name='backend-details-attribute-page'),

    path('worker-attribute/', worker_attribute_page, name='backend-worker-attribute-page'),
    path('worker-attribute/<slug:action>/<int:pk>', worker_attribute_page, name='backend-worker-attribute-page'),

    path('get/citymun/<int:pk>', get_citymun, name='get-citymun'),
    path('get/barangay/<int:pk>', get_barangay, name='get-barangay'),



]
