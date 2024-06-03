
Project Overview

Project Name: Django Vendor Management System with Performance Metrics

Objective:
The objective of the project is to develop a Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

Key Features:

User Authentication: Users can register as either a consumer or a vendor and log in securely to access the system.
Vendor Management: Vendors can create and manage their profiles, including contact details and address information.
Purchase Order Tracking: The system allows buyers to create purchase orders, which vendors can then acknowledge, issue, and complete.
Performance Metrics Calculation: The system calculates various performance metrics for vendors, including on-time delivery rate, quality rating average, average response time, and fulfillment rate.
Historical Performance Tracking: Historical performance metrics are recorded over time to track vendor performance trends.

Technology Stack:
Django: Backend framework for building web applications using Python.
Django REST Framework: Powerful and flexible toolkit for building Web APIs in Django.
Swagger: API documentation tool for describing, producing, consuming, and visualizing RESTful web services.
Implementation Highlights:

User Model: Custom user model implemented to support  consumer, products,orderr purchase and vendors with different user types.
API Endpoints: Various endpoints implemented to handle user authentication, vendor management, purchase order tracking, and performance metrics calculation.
Swagger Documentation: Swagger used to generate interactive API documentation, making it easy for developers to understand and test the endpoints.

This project aims to streamline vendor management processes, improve transparency and accountability, and facilitate data-driven decision-making by providing valuable insights into vendor performance.



Setting Up the Project:

1. Clone the Repository:
git clone <repository-url>

2. Navigate to Project Directory:
cd Vendor_management_system
run ls to check if there is any file named manage.py , if it is there then you are in right directory.

3.Create and Activate Virtual Environment:
For MAC/Linux:
python3 -m venv env
source venv/bin/activate
For Windows:
python -m venv env
venv\Scripts\activate

4.Install Dependencies:
pip install -r requirements.txt

5. Run Migrations:(Optional)- Only if it is asking for migrations:
python manage.py migrate

6. Run the Development Server:
python manage.py runserver
Clone the repository:
  git clone <repository_url>
  
Install dependencies:
  pip install -r requirements.txt
  
Authentication:
  Login: POST  api/login/
  Vendor Signup: POST /api/vendors/signup/
  Consumer Signup: POST /api/consumer/signup/

Products:
  Create Product: POST /api/product/
  List Products: GET /api/product/list/
  Update Product: PUT /api/product/update/
  Delete Product: DELETE /api/product/delete/<int:product_id>/

Vendor Performance:
  Vendor Performance Metrics: GET /api/vendors/performance/
  Vendor Historical Performance: GET /api/vendors/historical-performance/

Vendor Profile:
  Vendor Signup: POST /api/vendors/signup/
  List Vendors: GET /api/vendors/list/
  Retrieve Vendor Detail: GET /api/vendors/<int:vendor_id>/
  Update Vendor Detail: PUT /api/vendors/<int:vendor_id>/
  Delete Vendor: DELETE /api/vendors/<int:vendor_id>/
  Consumer Profile
  Consumer Signup: POST /api/consumer/signup/
  Retrieve Consumer Detail: GET /api/consumer/details/





Project Structure
  vendor_models: Contains all the models related to Projects.
  apis: Contains all the APIs along with Swagger documentation and Simple JWT authentication.

Authentication
JWT Token: Authentication for accessing API endpoints is handled using JSON Web Tokens (JWT). Users are required to authenticate by including a valid JWT token in the Authorization header of the request. Without authentication, access to most endpoints is restricted.
Note on Filters and Pagination

Filters: Some list endpoints support filtering by specific parameters, such as vendor name or item name. Users can include filter parameters in the query string of the URL to narrow down the results.
Pagination: List endpoints are paginated to improve performance and manage large datasets. Users can specify the page number and page size in the query string to navigate through the paginated results.

Swagger:Swagger  UI allows you to test your API endpoints directly from the documentation page. This can be very handy during development and debugging, as you can quickly verify that your endpoints are behaving as expected.


 
