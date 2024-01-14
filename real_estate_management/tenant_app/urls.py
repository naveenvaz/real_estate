from django.urls import path
from .views import *


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('propery_list/', property_list, name='property_list'),
    path('property_create/', property_create, name='property_create'),
    path('property_update/<int:id>', property_update, name='property_update'),
    path('property_delete/<int:id>', property_delete, name='property_delete'),
    path('property_units/<int:property_id>', property_units, name='property_units'),
    path('units/', unit_list, name='unit_list'),
    path('create_unit/', create_unit, name='create_unit'),
    path('update_unit/<int:id>/', update_unit, name='update_unit'),
    path('delete_unit/<int:id>/', delete_unit, name='delete_unit'),
    path('agreements/', agreement_list, name='agreement_list'),
    path('create_agreement/', create_agreement, name='create_agreement'),
    path('update_agreement/<int:id>/', update_agreement, name='update_agreement'),
    path('delete_agreement/<int:id>/', delete_agreement, name='delete_agreement'),
    path('tenants/', tenant_list, name='tenant_list'),
    path('create_tenant/', create_tenant, name='create_tenant'),
    path('update_tenant/<int:pk>/', update_tenant, name='update_tenant'),
    path('delete_tenant/<int:pk>/', delete_tenant, name='delete_tenant'),
    path('tenant/<int:tenant_id>/', tenant_profile, name='tenant_profile'),
    path('tenant/<int:tenant_id>/agreements/', agreements_for_tenant, name='agreements_for_tenant'),
    path('view_documents/<int:tenant_id>/', view_documents, name='view_documents'),
    path('get_units_for_property/', get_units_for_property, name='get_units_for_property'),
    path('get_tenants_for_unit/', get_tenants_for_unit, name='get_tenants_for_unit'),
    path('accounts/profile/', home, name='home'),
    path('search/', search_results, name='search_results'),
    path('add_document/', add_document, name='add_document'),
    path('features/', feature_list, name='feature_list'),
    path('features/create/', create_feature, name='create_feature'),
    path('features/<int:pk>/update/', update_feature, name='update_feature'),
    path('features/<int:pk>/delete/', delete_feature, name='delete_feature'),
]



