import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK with my Service Account File
cred = credentials.Certificate("/customers/zhangying-macbookpro/Documents/BYU-Pathway/BYU_Idaho/fall 2024/cse310/jianjun-furniture-store-firebase-adminsdk-dja2z-de227bea56.json")

firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

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
def add_product_to_category(category_name, product_id, name, price, stock):
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
def add_customer(customer_id, name, email):
    db.collection('customers').document(customer_id).set({
        'name': name,
        'email': email
    })
    print(f'customer {name} added successfully!')
    print("-" * 30)

# merge new fields into existing document
def merge_field_customer(customer_id):
    db.collection('customers').document(customer_id).set({
        'new_customer': True}, merge=True)
    print(f'{customer_id} is added as new_customer successfully!')
    print("-" * 30)


# Function to retrieve all products in all categories with additional checks
def get_all_products():
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
def get_products_in_category(category_name):
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
def get_product(category_name, item_id):
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
def get_customers():
    customers = db.collection('customers').get()
    for customer in customers:
        print(f'{customer.id} => {customer.to_dict()}')
        print("-" * 30)

#Funciton to sorting products and limiting 10 in a Sub-Collection (items)
def get_top_10_expensive_items():
    try:
        # Query the 'items' collection group directly
        query = db.collection_group('items').order_by('price', direction=firestore.Query.DESCENDING).limit(10)
        items = query.get()

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
def update_product_in_category(category_name, product_id, name=None, price=None, stock=None):
    # Reference to the 'items' subcollection within the specified category
    product_ref = db.collection('products').document(category_name).collection('items').document(product_id)
    
    # Prepare a dictionary with only the fields that need to be updated
    updates = {}
    if name is not None:
        updates['name'] = name
    if price is not None:
        updates['price'] = price
    if stock is not None:
        updates['stock'] = stock
    
    # Perform the update if there are fields to update
    if updates:
        product_ref.update(updates)
        print(f'Product {product_id} in {category_name} category updated successfully!')
        print("-" * 30)
    else:
        print("No updates provided.")

#update customer data
def update_customer(customer_id, name=None, email=None):
    # Prepare a dictionary with only the fields that need to be updated
    updates = {}
    if name is not None:
        updates['name'] = name
    if email is not None:
        updates ['email'] = email

    # Perform the update if there are fields to update
    if updates:
        db.collection('customers').document(customer_id).update(updates)
        print(f"Customer {customer_id} updated successfully!")
        print("-" * 30)
    else:
        print("No updates provided.")

#delete customer data 
def delete_customer(customer_id):
    db.collection('customers').document(customer_id).delete()
    print(f'customer {customer_id} is deleted successfully!')
    print("-" * 30)

#delete products data
def delete_product_from_category(category_name, product_id):
    # Reference to the 'items' subcollection within the specified category
    product_ref = db.collection('products').document(category_name).collection('items').document(product_id)
    product_ref.delete()
    print(f'Product {product_id} from {category_name} category deleted successfully!')
    print("-" * 30)

    
def register_out_of_stock():

def main():
    categories = ["living_room", "bedroom", "bathroom", "kitchen", "dining_room"]
    register_out_of_stock(db)
    choice = None
    while choice != "0":
        print()
        print("0> Exit")
        print("1> Add New Data")
        print("2> Retrieve Data")
        print("3> Remove Data")
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
                category_name = choose_category(categories)
                product_id = input(f"Enter producr ID: ")
                name = input(f"Enter product name: ")
                try:
                    price = float(input("Enter product price: "))
                    stock = int(input("Enter product stock: "))
                    add_product_to_category(category_name, product_id, name, price, stock)
                except ValueError:
                    print("Invalid input! Make sure price is a number and stock is an integer.")
            elif sub_choice =="2":
                customer_id = input(f"Enter customer ID: ")
                name = input(f"Enter customer name: ")
                email = input(f"Enter customer email: ")
                add_customer(customer_id, name, email)
            else:
                print("Please choose again.")
        elif choice == "2":
            print("1. Retrieve data of a specific product")
            print("2. Retrieve data of products from a specific category")
            print("3. Retrieve data of products from all categories")
            print("4. Retrieve all customers data")
            sub_choice = input(f"Choose a function: ")
            print()
            if sub_choice == "1":
                get_product(category_name, product_id)
            elif sub_choice == "2":
                get_products_in_category(category_name)
            elif sub_choice == "3":
                get_all_products()
            elif sub_choice == "4":
                get_customers()



        elif choice == "3":

        elif choice == "4":


# Example usage
if __name__ == '__main__':
    main()

    # add a field to document "customer "
    # merge_field_customer('U003')
    # filter products data by >= 1000
    # filter_products()
    # order products data by price and stock descending
    # order_products()
    # print("\nProducts:")
    # get_product("living_room", "lr1")
    # get_products_in_category("living_room")
    # get_all_products()
    # print("\ncustomers:")
    # get_customers()   

    # Update data
    # Update only the price of the product
    # update_product_in_category("bathroom", "bt1", price=450)
    # Update all fields
    # update_product_in_category("bathroom", "bt1", name=" Luxury Bathroom Vanity", price=500, stock=5)

    # update_customer('U001', {'name': 'Alice Smith'})

    # Delete data
    # delete_product_from_category("bathroom", "bt1")
    # delete_customer('U003')


                        # Living Room Products
                    # add_product_to_category("living_room", "lr1", "Sofa", 800, 15)
                    # add_product_to_category("living_room", "lr2", "Coffee Table", 150, 25)
                    # add_product_to_category("living_room", "lr3", "TV Stand", 200, 10)
                    # add_product_to_category("living_room", "lr4", "Bookshelf", 120, 8)
                    # add_product_to_category("living_room", "lr5", "Armchair", 250, 12)
                    # Bedroom Products
                    # add_product_to_category("bedroom", "br1", "Bed Frame", 700, 20)
                    # add_product_to_category("bedroom", "br2", "Nightstand", 90, 30)
                    # add_product_to_category("bedroom", "br3", "Wardrobe", 500, 5)
                    # add_product_to_category("bedroom", "br4", "Dresser", 300, 10)
                    # add_product_to_category("bedroom", "br5", "Bedside Lamp", 40, 50)
                    # Kitchen Products
                    # add_product_to_category("kitchen", "kt1", "Dining Set", 900, 7)
                    # add_product_to_category("kitchen", "kt2", "Refrigerator", 1200, 3)
                    # add_product_to_category("kitchen", "kt3", "Microwave Oven", 200, 20)
                    # add_product_to_category("kitchen", "kt4", "Kitchen Island", 600, 4)
                    # add_product_to_category("kitchen", "kt5", "Bar Stool", 75, 18)
                    #  Dining Room Products
                    # add_product_to_category("dining_room", "dr1", "Dining Table", 700, 5)
                    # add_product_to_category("dining_room", "dr2", "Dining Chair", 120, 30)
                    # add_product_to_category("dining_room", "dr3", "Buffet Table", 500, 4)
                    # add_product_to_category("dining_room", "dr4", "China Cabinet", 850, 3)
                    # add_product_to_category("dining_room", "dr5", "Table Runner", 25, 40)
                    # Bathroom Products
                    # add_product_to_category("bathroom", "bt1", "Bathroom Vanity", 400, 8)
                    # add_product_to_category("bathroom", "bt2", "Shower Curtain", 20, 60)
                    # add_product_to_category("bathroom", "bt3", "Bathroom Mirror", 100, 15)
                    # add_product_to_category("bathroom", "bt4", "Storage Cabinet", 150, 6)
                    # add_product_to_category("bathroom", "bt5", "Towel Set", 35, 50)  
