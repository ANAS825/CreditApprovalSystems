from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CustomerSerializer, LoanSerializer, RegisterSerializer, NewLoanEligibilitySerializer, NewLoanSerializer
from rest_framework import status
from .models import newcustomerdatamodel, loandata
import datetime
from datetime import date, timedelta
from rest_framework.request import Request
from rest_framework.test import APIClient
import random

# Get all customers
@api_view(['GET'])
def get_allcustomers(request):
    customers = newcustomerdatamodel.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

# Get customer data by ID
@api_view(['GET'])
def get_customer_data(request, id):
    customers = newcustomerdatamodel.objects.filter(customer_id = id).first()
    if customers:
        serializer = CustomerSerializer(customers)
        return Response(serializer.data)
    else:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

# Get loans associated with a customer by ID
@api_view(['GET'])
def get_loan_data(request, id):
    loan_data = loandata.objects.filter(Customer_id=id).all()  # or Customer__customer_id=id if FK used properly

    if loan_data.exists():
        serializer = LoanSerializer(loan_data, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'Loan data not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    
# Get loan data by Loan ID
@api_view(['GET'])
def get_loan_by_id(request, loan_id):
    loan_data = loandata.objects.filter(Loan_ID=loan_id).first()
    if loan_data:
        serializer = LoanSerializer(loan_data)
        return Response(serializer.data)
    else:
        return Response({'error': 'Loan data not found'}, status=status.HTTP_404_NOT_FOUND)


# Register a new customer
@api_view(['POST'])
def register_customer(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        return Response(RegisterSerializer(instance).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Check loan eligibility
@api_view(['POST'])
def check_eligibility(request):
    serializer = NewLoanEligibilitySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data
    customer_id = validated_data['customer_id']
    loan_amount = validated_data['loan_amount']
    interest_rate = validated_data['interest_rate']
    tenure = validated_data['tenure']


    customer_data = newcustomerdatamodel.objects.filter(customer_id = customer_id).first()
    if not customer_data:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    # Credit score logic
    credit_score = 10
    loans = loandata.objects.filter(Customer_id=customer_id)
    total_loan_amount = sum(loan.Loan_amount for loan in loans)

    if loans.exists():
        if all(loan.EMI < 0.4 * customer_data.monthly_income for loan in loans):
            credit_score += 10
        else:
            credit_score -= 10
        if len(loans) > 1:
            credit_score += 10

        today = datetime.date.today()
        if any(loan.end_date < today for loan in loans):
            credit_score -= 10
        else:
            credit_score += 10
    else:
        credit_score += 20

    if total_loan_amount >= customer_data.approved_limit:
        credit_score = 0  # Reset credit score if total loan amount exceeds approved limit
        return Response({'message': 'Customer is not eligible for a new loan'}, status=status.HTTP_400_BAD_REQUEST)
    
    credit_score += 10  # for below approved limit

    # Loan approval decision
    approval = False
    if credit_score >= 50:
        approval = True
        final_interest_rate = 10
    elif 30 < credit_score < 50:
        approval = True
        final_interest_rate = 12
    elif 20 < credit_score <= 30:
        approval = True
        final_interest_rate = 16
    else:
        approval = False
        return Response({'message': 'Customer is not eligible for a new loan'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'customer_id': customer_id,
        'loan_amount': loan_amount,
        'tenure': tenure,
        'interest_rate': interest_rate,
        'corrected_interest_rate': final_interest_rate,
        'approval': approval
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def add_loan(request):
    try:
        data = request.data.copy()

        # Validate required input fields
        required_fields = ['customer_id', 'Loan_amount', 'Tenure', 'Interest_rate']
        for field in required_fields:
            if field not in data:
                return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract and convert input
        customer_id = int(data['customer_id'])
        loan_amount = int(data['Loan_amount'])
        tenure = int(data['Tenure'])  # in months
        interest_rate = float(data['Interest_rate'])

        # Fetch customer
        customer = newcustomerdatamodel.objects.get(customer_id=customer_id)

        # Example eligibility logic:
        if loan_amount > customer.approved_limit:
            return Response({
                "loan_id": None,
                "customer_id": customer_id,
                "loan_approved": False,
                "message": "Loan amount exceeds customer approved limit",
                "monthly_installment": 0.0
            }, status=status.HTTP_200_OK)

        # Generate Loan ID
        loan_id = random.randint(1000, 9999)

        # Calculate EMI
        monthly_interest = interest_rate / 12 / 100
        emi = (loan_amount * monthly_interest * (1 + monthly_interest)**tenure) / ((1 + monthly_interest)**tenure - 1)
        emi = round(emi, 2)


        # Set dates
        start_date = date.today()
        end_date = start_date + timedelta(days=30 * tenure)

        # Create loan entry
        loan = loandata.objects.create(
            Customer_id=customer,
            Loan_ID=loan_id,
            Loan_amount=loan_amount,
            Tenure=tenure,
            Interest_rate=interest_rate,
            EMI=int(emi),
            EMIPOT=0,
            start_date=start_date,
            end_date=end_date
        )

        return Response({
            "loan_id": loan.Loan_ID,
            "customer_id": customer_id,
            "loan_approved": True,
            "message": "Loan successfully approved.",
            "monthly_installment": emi
        }, status=status.HTTP_201_CREATED)

    except newcustomerdatamodel.DoesNotExist:
        return Response({
            "loan_id": None,
            "customer_id": data.get('customer_id'),
            "loan_approved": False,
            "message": "Customer not found",
            "monthly_installment": 0.0
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "loan_id": None,
            "customer_id": data.get('customer_id'),
            "loan_approved": False,
            "message": str(e),
            "monthly_installment": 0.0
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)