Grocery Store Application

Welcome to the Grocery Store Application! This application is designed to simulate a simple online grocery store where users can browse categories, view products, and place orders. It is built using Flask and SQLAlchemy.

Table of Contents:-
Features
Installation
Usage
API Endpoints

Features:-

User Registration and Authentication: Users can create accounts, log in, and log out.
Category Management: Admin users can add, update, and delete product categories.
Product Management: Admin users can add, update, and delete products with details like name, price, and stock.
Order Placement: Users can place orders for products, specifying the quantity.
API Endpoints: Provides a RESTful API for managing categories and products .
Basic Frontend: Includes basic frontend pages for users to view categories, products, and place orders.

Installation

1] Creating a virtual environment : py -m venv env 
2] Activating a virtual environment : .\env\Scripts\activate 

3] Install all necessary modules : py -m pip install -r requirements.txt

 (Instead of installing packages individually, pip allows you to declare all dependencies in a Requirements File.)


Configure the database:
(Inside python terminal)
1] from app import *
2] db.create_all()

Run the application:

*] python app.py

Open your web browser and visit http://127.0.0.1:5000/ to access the application.

Usage:- 

Register as a user or log in with existing credentials.
Browse categories and view products.
Place orders by selecting products and specifying quantities.
Admin users can access the admin panel (/admin) to manage categories and products.

API Endpoints:-

The application provides the following API endpoints:

/cate: Category management (GET)
/cate/<int:c_id>: Single category management (GET, POST,PUT, DELETE)
/proc: Product management (GET)
/proc/<int:p_id>: Single product management (GET, POST, PUT, DELETE)
Refer to the API Documentation for more details on these endpoints.


