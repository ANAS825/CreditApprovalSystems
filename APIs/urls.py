# Here all the API URLS are defined for the CAS

from django.urls import path
from.views import get_customer_data, get_allcustomers, get_loan_data, register_customer, check_eligibility, add_loan, get_loan_by_id

urlpatterns = [
    path('customers/', get_allcustomers, name = 'get_allcustomers'), # List all customers
    path('customer/<int:id>/', get_customer_data, name='get_customer_data'), # Get customers by ID
    path('customer/view-loan/<int:id>/', get_loan_data, name = 'Get_customer_loan_data'), # Get loans associated By customer Id
    path('register/', register_customer, name = 'register_new_customer'), # Register a new customer
    path('check-eligibility/',check_eligibility, name='check_eligibility'), # Check loan eligibility
    path('create-loan/', add_loan, name='new_loan'), # Create a new loan
    path('view-loan/<int:loan_id>/', get_loan_by_id, name = 'get_loan_by_id'), # Get loan by ID
]

