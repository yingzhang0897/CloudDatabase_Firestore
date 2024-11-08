import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK with my Service Account File
cred = credentials.Certificate("/Users/zhangying-macbookpro/Documents/BYU-Pathway/BYU_Idaho/fall 2024/cse310/jianjun-furniture-store-firebase-adminsdk-dja2z-de227bea56.json")

firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

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
    print(f'Product {name} added under {category_name} successfully!')

def add_user(user_id, name, email):
    db.collection('users').document(user_id).set({
        'name': name,
        'email': email
    })
    print(f'User {name} added successfully!')

# merge new fields into existing document
def merge_field_user(user_id):
    db.collection('users').document(user_id).set({
        'new_user': True}, merge=True)
    print(f'{user_id} is added as new_user successfully!')

def list_top_level_collections():
    try:
        collections = db.collections()
        print("Top-level collections:")
        for collection in collections:
            print(collection.id)
    except Exception as e:
        print(f"Error fetching top-level collections: {e}")
def list_documents_in_products():
    try:
        categories = db.collection('products').get()
        if not categories:
            print("No documents found in 'products' collection.")
        else:
            print("Documents in 'products' collection:")
            for category in categories:
                print(f" - {category.id}")
    except Exception as e:
        print(f"Error listing documents in 'products' collection: {e}")
def check_items_subcollections():
    try:
        categories = db.collection('products').get()
        for category in categories:
            category_name = category.id
            print(f"Checking 'items' sub-collection in category '{category_name}'...")
            
            # Try fetching items in this category's 'items' sub-collection
            items = db.collection('products').document(category_name).collection('items').get()
            if not items:
                print(f"No items found in 'items' sub-collection of '{category_name}'")
            else:
                print(f"Items in '{category_name}':")
                for item in items:
                    print(f" - {item.id}: {item.to_dict()}")
    except Exception as e:
        print(f"An error occurred: {e}")








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
                product_data["category"] = category_name  # Add category name to product data
                product_data["id"] = item.id              # Add item ID to product data
                all_products.append(product_data)
                print(f" - Product ID: {item.id}, Data: {product_data}")
        
        print("All products retrieved successfully.")
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
        else:
            print(f"Product {item_id} does not exist!")
    except Exception as e:
        print(f"An error occured: {e}")


# Function to retrieve all users from a collection
def get_users():
    users = db.collection('users').stream()
    for user in users:
        print(f'{user.id} => {user.to_dict()}')

#Funciton to filter a collection
def filter_products():
    expensive_products = (
        db.collection("products")
        .where("price", ">=", 1000)  # Using the 'filter' keyword explicitly
        .stream()
    )
    for ex in expensive_products:
        print(f"{ex.id} => {ex.to_dict()}")
#Function to order documents in a collection
def order_products():
    ordered_products = db.collection("products").order_by('price', direction = firestore.Query.DESCENDING).order_by('stock', direction = firestore.Query.DESCENDING).stream()
    for product in ordered_products:
        print(f'{product.id} => {product.to_dict()}')

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
    else:
        print("No updates provided.")

#update user data
def update_user(user_id, updated_data):
    db.collection('users').document(user_id).update(updated_data)
    print(f'User {user_id} updated successfully!')

#delete user data 
def delete_user(user_id):
    db.collection('users').document(user_id).delete()
    print(f'User {user_id} is deleted successfully!')

#delete products data
def delete_product_from_category(category_name, product_id):
    # Reference to the 'items' subcollection within the specified category
    product_ref = db.collection('products').document(category_name).collection('items').document(product_id)
    product_ref.delete()
    print(f'Product {product_id} from {category_name} category deleted successfully!')

#test
# Test fetching a single known document
def test_retrieve_known_category():
    try:
        # Replace 'living_room' with an actual category document ID
        category_id = "living_room"
        doc = db.collection('products').document(category_id).get()
        if doc.exists:
            print(f"Document '{category_id}' found:", doc.to_dict())
        else:
            print(f"Document '{category_id}' not found.")
    except Exception as e:
        print(f"Error retrieving document '{category_id}': {e}")

# Test listing all documents again after fetching one directly
def list_documents_in_products():
    try:
        categories = db.collection('products').get()
        if not categories:
            print("No documents found in 'products' collection.")
        else:
            print("Documents in 'products' collection:")
            for category in categories:
                print(f" - {category.id}")
    except Exception as e:
        print(f"Error listing documents in 'products' collection: {e}")


# Example usage
if __name__ == '__main__':
# Adding products to Firestore with their respective categories
# Living Room Products
    # add_product_to_category("living_room", "lr1", "Sofa", 800, 15)
    # add_product_to_category("living_room", "lr2", "Coffee Table", 150, 25)
    # add_product_to_category("living_room", "lr3", "TV Stand", 200, 10)
    # add_product_to_category("living_room", "lr4", "Bookshelf", 120, 8)
    # add_product_to_category("living_room", "lr5", "Armchair", 250, 12)
    # print('-' * 50)  # Horizontal line

    # # Bedroom Products
    # add_product_to_category("bedroom", "br1", "Bed Frame", 700, 20)
    # add_product_to_category("bedroom", "br2", "Nightstand", 90, 30)
    # add_product_to_category("bedroom", "br3", "Wardrobe", 500, 5)
    # add_product_to_category("bedroom", "br4", "Dresser", 300, 10)
    # add_product_to_category("bedroom", "br5", "Bedside Lamp", 40, 50)
    # print('-' * 50)  # Horizontal line

    # # Kitchen Products
    # add_product_to_category("kitchen", "kt1", "Dining Set", 900, 7)
    # add_product_to_category("kitchen", "kt2", "Refrigerator", 1200, 3)
    # add_product_to_category("kitchen", "kt3", "Microwave Oven", 200, 20)
    # add_product_to_category("kitchen", "kt4", "Kitchen Island", 600, 4)
    # add_product_to_category("kitchen", "kt5", "Bar Stool", 75, 18)
    # print('-' * 50)  # Horizontal line

    # # Dining Room Products
    # add_product_to_category("dining_room", "dr1", "Dining Table", 700, 5)
    # add_product_to_category("dining_room", "dr2", "Dining Chair", 120, 30)
    # add_product_to_category("dining_room", "dr3", "Buffet Table", 500, 4)
    # add_product_to_category("dining_room", "dr4", "China Cabinet", 850, 3)
    # add_product_to_category("dining_room", "dr5", "Table Runner", 25, 40)
    # print('-' * 50)  # Horizontal line

    # # Bathroom Products
    # add_product_to_category("bathroom", "bt1", "Bathroom Vanity", 400, 8)
    # add_product_to_category("bathroom", "bt2", "Shower Curtain", 20, 60)
    # add_product_to_category("bathroom", "bt3", "Bathroom Mirror", 100, 15)
    # add_product_to_category("bathroom", "bt4", "Storage Cabinet", 150, 6)
    # add_product_to_category("bathroom", "bt5", "Towel Set", 35, 50)  
    # print('-' * 50)  # Horizontal line

    # add_user('U001', 'Alice', 'alice@example.com')
    # add_user('U002', 'Sam', 'sam@gmail.com')
    # add_user('U003', 'Alex', 'alex@hotmail.com')
    # add a field to document "user "
    # merge_field_user('U003')
    # filter products data by >= 1000
    # filter_products()
    # order products data by price and stock descending
    # order_products()
    # print("\nProducts:")
    # get_product("living_room", "lr1")
    # get_products_in_category("living_room")
    # list_top_level_collections()
    # list_documents_in_products()
    # check_items_subcollections()
    # Run both functions
    test_retrieve_known_category()
    list_documents_in_products()

    # get_all_products()
    # print("\nUsers:")
    # get_users()   

    # Update data
    # Update only the price of the product
    # update_product_in_category("bathroom", "bt1", price=450)
    # Update all fields
    # update_product_in_category("bathroom", "bt1", name=" Luxury Bathroom Vanity", price=500, stock=5)

    # update_user('U001', {'name': 'Alice Smith'})

    # Delete data
    # delete_product_from_category("bathroom", "bt1")
    # delete_user('U003')