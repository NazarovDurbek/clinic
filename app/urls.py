from django.urls import path
from .views import *




app_name='app'

urlpatterns = [
    path('hospitals/', hospitals, name='hospitals_list'),
    path('hospitals/<slug:hospital_slug>/', hospital_detail, name='hospital_detail'),
    path('doctors/<str:doctor_specialty>/', doctors_list, name='doctors_list'),
    path('doctor/<int:doctor_id>/', doctor_detail, name='doctor_detail'),
    path('doctor/<int:doc_id>/<str:type>/book_slot/', book_slot, name='book_slot'),
    path('doctor/confirm_record/', patient_details, name='patient_details'),
    path('goods/', goods, name='goods_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('basket/', basket, name='basket' ),
    path('basket/add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('convert-baskets-to-order/', convert_baskets_to_order, name='convert_baskets_to_order'),
    path('confirm_order/', confirm_order, name='confirm_order'),
    path('confirm_record/', confirm_record, name='confirm_record'),
    path('contact/', contact, name='contact' ),
    path('novosti/', novosti_catalog, name='novosti_catalog'),
    path('o_nas', o_nas, name='o_nas'),


]