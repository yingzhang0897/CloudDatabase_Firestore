import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK with your Service Account File
cred = credentials.Certificate("/Users/zhangying-macbookpro/Documents/BYU-Pathway /BYU_Idaho/fall 2024/cse310/jianjun-furniture-store-firebase-adminsdk-dja2z-033eeb3f54.json")

firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Function to insert data into Firestore
def add_product(product_id, name, price, stock):
    db.collection('products').document(product_id).set({
        'name': name,
        'price': price,
        'stock': stock
    })
    print(f'Product {name} added successfully!')

def add_user(user_id, name, email):
    db.collection('users').document(user_id).set({
        'name': name,
        'email': email
    })
    print(f'User {name} added successfully!')

# Function to retrieve data from Firestore
def get_products():
    products = db.collection('products').get()
    for product in products:
        print(f'{product.id} => {product.to_dict()}')

def get_users():
    users = db.collection('users').get()
    for user in users:
        print(f'{user.id} => {user.to_dict()}')

# Function to update data in Firestore
def update_product(product_id, updated_data):
    db.collection('products').document(product_id).update(updated_data)
    print(f'Product {product_id} updated successfully!')

def update_user(user_id, updated_data):
    db.collection('users').document(user_id).update(updated_data)
    print(f'User {user_id} updated successfully!')

# Function to delete data from Firestore
def delete_product(product_id):
    db.collection('products').document(product_id).delete()
    print(f'Product {product_id} deleted successfully!')

def delete_user(user_id):
    db.collection('users').document(user_id).delete()
    print(f'User {user_id} deleted successfully!')

# Example usage
if __name__ == '__main__':
    # Insert sample data
    add_product('P001', 'Laptop', 1200.00, 10)
    add_user('U001', 'Alice', 'alice@example.com')

    # Retrieve and display data
    print("\nProducts:")
    get_products()
    print("\nUsers:")
    get_users()

    # Update data
    update_product('P001', {'price': 1100.00})
    update_user('U001', {'name': 'Alice Smith'})

    # Delete data
    # delete_product('P001')
    # delete_user('U001')
