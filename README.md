# Overview

This software is an e-commerce platform that integrates with a cloud database (Firestore) to manage product listings and user accounts. The platform enables CRUD operations, demonstrating cloud database capabilities in a real-world application.

The purpose of this software is to gain hands-on experience with cloud databases, particularly Firestore, and to implement basic functionalities like data insertion, retrieval, modification, and deletion.

[Software Demo Video](not done yet...)

# Cloud Database

The cloud database used is Google Firestore. 
It stores two collections: 'products' and 'users'. The 'products' collection stores product details such as ID, name, price, and stock, while the 'users' collection stores user information like ID, name, and email.

# Development Environment

The software was developed using:
- Python
- Firebase Admin SDK for Python

# Useful Websites

- [Firestore Documentation](https://firebase.google.com/docs/firestore)
- [Firebase Python Admin SDK](https://firebase.google.com/docs/admin/setup)

# Future Work

- Implement user authentication for secure login and registration.
- Add real-time notifications for data changes using Firestore triggers.
- Create a frontend interface using a framework like Flask or Django.
