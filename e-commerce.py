import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firestore():
# Initialize Firebase Admin SDK with my Service Account File
    cred = credentials.Certificate("/Users/zhangying-macbookpro/Documents/BYU-Pathway/BYU_Idaho/fall 2024/cse310/jianjun-furniture-store-firebase-adminsdk-dja2z-de227bea56.json")

    firebase_admin.initialize_app(cred)

    # Initialize Firestore client
    db = firestore.client()
    return db

#This list is needed in product-related functions
categories = ["living_room", "bedroom", "bathroom", "kitchen", "dining_room"]

# let customer choose a category to add product
def choose_category(categories):
    print("Select a category:")
    for i, category in enumerate(categories, 1):
        print(f"{i}> {category}")
    
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

# Function to add a product under a specific category's subcollection
def add_product_to_category(db):
    print("It is ready for you to add some products data...")

    #prompt user to type in parameters in order to add product data
    category_name = choose_category(categories)
    product_id = input(f"Enter producr ID: ")
    name = input(f"Enter product name: ")
    try:
        price = float(input("Enter product price: "))
        stock = int(input("Enter product stock: "))
    except ValueError:
        print("Invalid input! Make sure price is a number and stock is an integer.")

    # Reference to the 'items' subcollection within the specific category document in the 'products' collection
    product_ref = db.collection('products').document(category_name).collection('items').document(product_id)
    #Set product details under the 'items' subcollection
    product_ref.set({
        'name': name,
        'price': price,
        'stock': stock
    })
    print(f'Product: {name} - ID: {product_id} - Price: {price} - Stock: {stock} added to {category_name}  successfully!')
    print("-" * 30)

# Function to add a customer
def add_customer(db):
    print("It is ready for you to add some customers data...")
    #prompt user to type in parameters in order to add customer data
    customer_id = input(f"Enter customer ID: ")
    name = input(f"Enter customer name: ")
    email = input(f"Enter customer email: ")

    db.collection('customers').document(customer_id).set({
        'name': name,
        'email': email
    })
    print(f'customer {name} added successfully!')
    print("-" * 30)

# merge new fields into existing document
def merge_new_customer(db):
    print("This customer data is going to be merged...")
    #prompt user to type in parameters in order to modify customer data
    customer_id = input(f"Please verify customer ID: ")
    db.collection('customers').document(customer_id).set({
        'new_customer': True}, merge=True)
    print(f'{customer_id} is added as new_customer successfully!')
    print("-" * 30)


# Function to retrieve all products in all categories with additional checks
def get_all_products(db):
    try:
        print("Fetching categories from 'products' collection...")
        
        # Retrieve all category documents in the 'products' collection
        categories = db.collection('products').get()
        
        # Check if categories were fetched
        if not categories:
            print("No categories found.")
            return []

        all_products = []  # List to store all products across all categories

        # Loop through each category document
        for category in categories:
            category_name = category.id
            print(f"Retrieving products for category '{category_name}'...")

            # Check if the category has an 'items' sub-collection
            items_ref = db.collection('products').document(category_name).collection('items')
            items = items_ref.get()

            # If no items are found, skip this category
            if not items:
                print(f"No items found for category '{category_name}' or 'items' sub-collection missing.")
                continue
            
            # Collect all items under this category
            for item in items:
                product_data = item.to_dict()
                all_products.append(product_data)
                print(f" -  {item.id}: {product_data}")
        
        print("All products retrieved successfully.")
        print("-" * 30)
        return all_products  # Return a list of all products across all categories
    
    except Exception as e:
        print(f"An error occurred while retrieving all products: {e}")
        return []

# Function to retrieve all products within a specific category
def get_products_in_category(db):
    print("It is ready for you to get some products data from a category...")
    category_name = choose_category(categories)
    try:
        # Access the 'items' sub-collection within the specified category
        items = db.collection('products').document(category_name).collection('items').get()
        
        # Check if any items are found
        if not items:
            print(f"No items found for category '{category_name}'")
            return []

        # Print and collect all items in this category
        print(f"Products in category '{category_name}':")
        product_list = []
        for item in items:
            product_data = item.to_dict()
            product_list.append({"id": item.id, **product_data})
            print(f" - {item.id}: {product_data}")
            print("-" * 30)

        return product_list  # Return the list of products in the category
    
    except Exception as e:
        print(f"An error occurred while retrieving products in category '{category_name}': {e}")
        return []

# Function to retrieve single document data from Firestore
def get_product(db):
    print("It is ready for you to get a product data...")
    #prompt user to type in category_name and item_id to get a specific product data
    category_name = choose_category(categories)
    item_id = input(f"Enter producr ID: ")
    try:
        doc = db.collection('products').document(category_name).collection('items').document(item_id).get()
        if doc.exists:
            print(f"{category_name} - {item_id}: {doc.to_dict()}")
            print("-" * 30)
        else:
            print(f"Product {item_id} does not exist!")
    except Exception as e:
        print(f"An error occured: {e}")


# Function to retrieve all customers from a collection
def get_customers(db):
    print("It is ready for you to get some customers data...")
    customers = db.collection('customers').get()
    for customer in customers:
        print(f'{customer.id} => {customer.to_dict()}')
        print("-" * 30)

#Funciton to sorting products and limiting 10 in a Sub-Collection (items)
def get_top_10_expensive_items(db):
    print("It is ready for you to get top-10 expensive product items data in all categories...")
    try:
        # Query the 'items' collection group directly
        items = db.collection_group('items').order_by('price', direction=firestore.Query.DESCENDING).limit(10).get()

        print("Top 10 Most Expensive Items:")
        for i, item in enumerate(items, start=1):
            item_data = item.to_dict()
            print(f"#{i}")
            print(f"Item ID: {item.id}")
            print(f"Name: {item_data.get('name')}")
            print(f"Price: {item_data.get('price')}")
            print(f"Stock: {item_data.get('stock')}")
            print("-" * 30)
    except Exception as e:
        print(f"An error occurred: {e}")

#update products data
def update_product_in_category(db):
    print("It is ready for you to update some products data...")
    #prompt user to type in parameters in order to update product data
    category_name = choose_category(categories)
    product_id = input(f"Enter producr ID: ")
    # Prepare a dictionary with fields that need to be updated
    updates = {}
    #update name
    update_name = input("Do you want to update the product name? (yes/no): ").strip().lower()
    if update_name == "yes":
        name = input("Enter new product name: ").strip()

    #update price
    update_price = input("Do you want to update the product price? (yes/no): ").strip().lower()
    if update_price == "yes":
        try:
            price = float(input("Enter new product price: "))
            updates['price'] = price
        except ValueError:
            print("Invalid input! Make sure price is a number.")
    #update stock
    update_stock = input("Do you want to update the product stock (yes/no): ").strip().lower()
    if update_stock == "yes":
        try:
            stock = int(input("Enter new product stock: "))
            updates['stock'] = stock
        except ValueError:
            print("Invalid input! Make sure stock is an integer.")

    # Reference to the 'items' subcollection within the specified category
    product_ref = db.collection('products').document(category_name).collection('items').document(product_id)
        
    # Perform the update if there are fields to update
    if updates:
        try:
            product_ref.update(updates)
            print(f'Product {product_id} in {category_name} category updated successfully!')
            print("-" * 30)
        except Exception as e:
            print(f"Error updating product: {e}")
    else:
        print("No updates provided.")

#update customer data
def update_customer(db):
    print("It is ready for you to update some customers data...")
    customer_id = input("Enter customer ID: ").strip()
    # Prepare a dictionary with fields that need to be updated
    updates = {}

    #prompt user to type in parameters in order to update customer data
    update_name = input("Do you want to update the customer name? (yes/no): ").strip().lower()
    if update_name == "yes":
        name = input("Enter new customer name: ").strip()
        updates['name'] = name

    update_email = input("Do you want to update the customer email? (yes/no): ").strip().lower()
    if update_email == "yes":
        email = input("Enter new customer email: ").strip()
        updates ['email'] = email

    # Perform the update if there are fields to update
    if updates:
        try:
            db.collection('customers').document(customer_id).update(updates)
            print(f"Customer {customer_id} updated successfully!")
            print("-" * 30)
        except Exception as e:
            print(f"Error updating product: {e}")
    else:
        print("No updates provided.")

#delete customer data 
def delete_customer(db):
    print("It is ready for you to delete some customers data...")
    customer_id = input("Enter customer_id: ")
    db.collection('customers').document(customer_id).delete()
    print(f'customer {customer_id} is deleted successfully!')
    print("-" * 30)

#delete products data
def delete_product_from_category(db):
    print("It is ready for you to delete some products data...")
    category_name = choose_category(categories)
    product_id = input("Enter product ID: ")
    # Reference to the 'items' subcollection within the specified category
    product_ref = db.collection('products').document(category_name).collection('items').document(product_id)
    product_ref.delete()
    print(f'Product {product_id} from {category_name} category deleted successfully!')
    print("-" * 30)


# Notify stock alert for items in sub-collections
def notify_stock_alert(results, changes, real_time):
    for change in changes:
        document_id = change.document.id
        data = change.document.to_dict()
        print(f"Change detected: {change.type.name} - {document_id}")
        
        if change.type.name == "ADDED":
            print(f"\nItem {document_id} is out of stock!!!\n")
        elif change.type.name == "REMOVED":
            print(f"\nItem {document_id} has been restocked!\n")
        elif change.type.name == "MODIFIED":
            stock = data.get("stock", None)
            if stock == 0:
                print(f"\nItem {document_id} is now out of stock!!!\n")
            elif stock is not None:
                print(f"\nItem {document_id} stock updated to {stock}\n")
    
# Register real-time listener for out-of-stock products in "items" sub-collections
def register_out_of_stock(db):
    print("Registering listener for out-of-stock items...")
    
    # Iterate over all categories in 'products' collection
    categories = db.collection("products").get()
    for category in categories:
        category_name = category.id        
        # Query the 'items' sub-collection for stock == 0
        query = db.collection("products").document(category_name).collection("items").where("stock", "==", 0)
        query.on_snapshot(notify_stock_alert)
    

def main():
    db = initialize_firestore()
    register_out_of_stock(db)
    choice = None
    while choice != "0":
        print()
        print("0> Exit")
        print("1> Add New Data")
        print("2> Retrieve Data")
        print("3> Delete Data")
        print("4> Update Data")
        choice = input(f"--- ")
        print()
        if choice == "0":
            print("See you soon.")
            break
        elif choice == "1":
            print("1. Add Product Data")
            print("2. Add customer Data")
            sub_choice = input(f"Choose a function: ")
            print()
            if sub_choice == "1":
                add_product_to_category(db)
            elif sub_choice =="2":
                add_customer(db)
            else:
                print("Please choose again.")

        elif choice == "2":
            print("1. Retrieve data of a specific product")
            print("2. Retrieve data of products from a specific category")
            print("3. Retrieve data of products from all categories")
            print("4. Retrieve all customers data")
            print("5. Get top-10 expensive product items")
            sub_choice = input(f"Choose a function: ")
            print()
            if sub_choice == "1":
                get_product(db)
            elif sub_choice == "2":
                get_products_in_category(db)
            elif sub_choice == "3":
                get_all_products(db)
            elif sub_choice == "4":
                get_customers(db)
            elif sub_choice =="5":
                get_top_10_expensive_items(db)

        elif choice == "3":
            print("1. Delete a customer")
            print("2. Delete a product from a category")
            sub_choice = input(f"Choose a function: ")
            print()
            if sub_choice == "1":
                delete_customer(db)
            elif sub_choice == "2":
                delete_product_from_category(db)

        elif choice == "4":
            print("1. Update a customer info")
            print("2. Update a product info")
            sub_choice = input(f"Choose a function: ")
            print()
            if sub_choice == "1":
                update_customer(db)
                merge = input("Do you want to mark this customer as a new customer? (yes/no): ")
                if merge == "yes":
                    merge_new_customer(db)
            elif sub_choice == "2":
                update_product_in_category(db)

# Example usage
if __name__ == '__main__':
    main()

