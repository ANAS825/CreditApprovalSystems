# CreditApprovalSystems
Repository for the Credit Approval System
This project is a Credit Approval System built using Django 4+ and Django Rest Framework. It processes customer data and historical loan information to assess loan eligibility based on credit scores. The application includes multiple API endpoints for customer registration, loan eligibility checks, and loan creation, all while handling error management effectively. The system is fully dockerized with a PostgreSQL database and background workers for data ingestion. This project showcases backend development with a focus on financial data processing and credit scoring logic.



**ENDPOINTS**
api/ customers/ ---> List All Customers
api/ customer/<int:id>/ --> Get Customer Details By Id
api/ customer/view-loan/<int:id>/ ---> View Customer's Loans
api/ register/ ---> Register New Customer
api/ check-eligibility/ ---> Check Customer's Eligiblity For Loan (using Credit score)
api/ create-loan/ ---> Create New Loan WIth with Customer Based on Eligbility
api/ view-loan/<int:loan_id>/ ---> Get Loans By Loan_Id



**Go to MASTER branch For Files**
