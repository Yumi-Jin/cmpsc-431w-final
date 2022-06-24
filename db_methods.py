import sqlite3 as sql
import hashlib
from datetime import *


# First function that will be called
def main():
    #for p in get_products('Makeup'):
    #    print(p[0])

    """ Testing Category Print
    for root, subcategory in get_categories().items():
        print(root)
        for subcat, sscat in subcategory.items():
            print("SUB CAT ---------" + subcat)
            if sscat:
                for subsubcat in sscat:
                    print("SUBSUBCAT --------------- " + subsubcat)
    """


# Checks the database for the specific user and password
def verify(email, password):
    connection = sql.connect('database.db')

    # Hashes the given password to see if it matches up with stored hashed password
    p = hashlib.md5(password.encode()).hexdigest()
    statement = f"SELECT email from users WHERE email = '{email}' AND password = '{p}';"
    cursor = connection.execute(statement)

    # If there is no rows selected, return False, otherwise return True
    if cursor.fetchone() != None:
        return True
    return False


def check_seller(email):
    connection = sql.connect('database.db')
    statement = f"SELECT email from Sellers where email = '{email}'"
    cursor = connection.execute(statement)
    if cursor.fetchone():
        return True
    else:
        return False


# Changes the password of specific user
def change_pass(email, old_password, new_password):
    correct_pass = verify(email, old_password)
    # FIrst checks if the password is correct
    if correct_pass:
        # hashes password, updates old password
        password = hashlib.md5(new_password.encode()).hexdigest()
        connection = sql.connect('database.db')
        statement = f"UPDATE Users SET password = '{password}' WHERE email = '{email}'"
        connection.execute(statement)

        connection.commit()
        return True
    return False


# Displays user information from tables Users, Buyers, and Addresses
# Puts all the information into a dictionary for easy retrieval
def display_user_info(email):
    connection = sql.connect('database.db')
    statement = f"SELECT * from Buyers WHERE email = '{email}'"
    cursor = connection.execute(statement)
    # email,first_name,last_name,gender,age,home_address_id,billing_address_id
    buyerinfo = cursor.fetchone()

    home_address = address_info(buyerinfo[5])
    billing_address = address_info(buyerinfo[6])

    statement = f"SELECT credit_card_num from Credit_Cards WHERE Owner_email = '{email}'"
    cursor = connection.execute(statement)
    creditcard = cursor.fetchone()
    last4digits = creditcard[0][-4:]

    # name, email ID, age, gender, email address, home and billing address, which
    # includes street, city, state and zipcode, last four digits of credit card number.
    userinfo = {
        "first_name": buyerinfo[1],
        "last_name": buyerinfo[2],
        "age": buyerinfo[4],
        "gender": buyerinfo[3],
        "email": email,
        "home_addr": home_address,
        "billing_addr": billing_address,
        "credit_card": last4digits
    }
    return userinfo


# Updates the values of first_name,last_name,gender,age from Buyers
def change_user_info(email, first_name, last_name, gender, age):
    connection = sql.connect('database.db')
    # Changes user information. checks if each field exists and then changes that specific field
    checkNone = 0
    if first_name:
        statement = f"UPDATE Buyers SET first_name = '{first_name}' WHERE email = '{email}'"
        connection.execute(statement)
        checkNone +=1
    if last_name:
        statement = f"UPDATE Buyers SET last_name = '{last_name}' WHERE email = '{email}'"
        connection.execute(statement)
        checkNone +=1
    if gender:
        statement = f"UPDATE Buyers SET gender = '{gender}' WHERE email = '{email}'"
        connection.execute(statement)
        checkNone +=1
    if age:
        statement = f"UPDATE Buyers SET age = '{age}' WHERE email = '{email}'"
        connection.execute(statement)
        checkNone +=1

    # If none of them were changed, then return error
    if checkNone == 0:
        return 'All entries are empty, please enter a value if you would like to change User Information'
    connection.commit()
    return True


# Puts all information from Address table into a dictionary based on address_id
def address_info(address_id):
    connection = sql.connect('database.db')

    # Gets all address attributes from address_id
    statement = f"SELECT * from Address WHERE address_id = '{address_id}'"
    cursor = connection.execute(statement)
    address = cursor.fetchone()

    # Get city and state from zip code
    statement = f"SELECT city, state_id from Zipcode_Info WHERE zipcode = '{address[1]}'"
    zip = connection.execute(statement).fetchone()

    # Puts all address information together as a nested hash table
    addressinfo = {
        'address_id': address_id,
        'street_name': address[3],
        'street_num': address[2],
        'city': zip[0],
        'state_id': zip[1],
        'zipcode': address[1]
    }

    return addressinfo


# Updates the values of zipcode,street_num,street_name from Address
def change_address(address_id, zipcode, street_num, street_name):
    connection = sql.connect('database.db')
    checkNone = 0

    # Check if zipcode exists
    if zipcode:
        # Edits zipcode, makes sure zipcode exists
        statement = f"SELECT zipcode from Zipcode_info WHERE zipcode = '{zipcode}'"
        cursor = connection.execute(statement).fetchone()
        if cursor:
            statement = f"UPDATE Address SET zipcode = '{zipcode}' WHERE address_id = '{address_id}'"
            connection.execute(statement)
            checkNone += 1
        else:
            return f"Zipcode '{zipcode}' does not exist, please enter a proper value"
    # Checks of streetnum exists
    if street_num:
        # Edits street number
        statement = f"UPDATE Address SET street_num = '{street_num}' WHERE address_id = '{address_id}'"
        connection.execute(statement)
        checkNone += 1
    # CHecks if street_name exists
    if street_name:
        # Edits street name
        statement = f"UPDATE Address SET street_name = '{street_name}' WHERE address_id = '{address_id}'"
        connection.execute(statement)
        checkNone += 1

    # if none of the entries were filled out, return an error
    if checkNone == 0:
        return 'All entries are empty, please enter a value if you would like to change Address Information'
    connection.commit()
    return True


# Gets all unique categories, used for testing
def get_all_categories():
    connection = sql.connect('database.db')
    statement = f"SELECT DISTINCT category_name from Categories"
    all_categories = connection.execute(statement).fetchall()
    return single_tuple_to_list(all_categories)


# Get all products from a specific category
def get_products(category):
    connection = sql.connect('database.db')
    statement = f"SELECT * from Product_Listing WHERE Category = '{category}'"
    products = connection.execute(statement).fetchall()
    return products


# Returns product information from specific product
def get_specific_product(email,lid):
    connection = sql.connect('database.db')
    statement = f"SELECT * from Product_Listing WHERE Seller_Email = '{email}' AND Listing_ID = '{lid}'"
    products = connection.execute(statement).fetchone()
    return products


# Converts categories from tuple into a hashtable for easy access
def get_categories():
    connection = sql.connect('database.db')
    statement = f"SELECT category_name from Categories WHERE parent_category = 'Root'"
    root_categories = connection.execute(statement).fetchall()

    categories = {}
    # Loops through all root categories
    for category in single_tuple_to_list(root_categories):
        categories[category] = {}

        # Loops through all subcategories of Root Categories
        subcategories = subcategory(category)
        for sc in subcategories:
            # If it is a leaf node, set the value of dictionary into None
            categories[category][sc] = {}

            # Checks for sub sub categories
            ssc = subcategory(sc)
            if ssc:
                for ssc in subcategory(sc):
                    categories[category][sc][ssc] = None
            else:
                categories[category][sc] = None

    # Returns a dictionary of all the categories and its children as a nested dictionary
    return categories


# Converts tuple into a list for easy access
def single_tuple_to_list(tup):
    l = []
    for t in tup:
        l.append(t[0])
    return l


# Gets the subcategory of specific parent category
def subcategory(category):
    connection = sql.connect('database.db')
    statement = f"SELECT category_name from Categories WHERE parent_category = '{category}'"
    subcategories = connection.execute(statement).fetchall()

    return single_tuple_to_list(subcategories)


# Gets the parent category until Root node is reached of specific category
def get_parent_categories(category):
    connection = sql.connect('database.db')
    # Stores all the categories
    categories = []
    categories.append(category)

    # Keeps searching for parent category until category == "Root"
    statement = f"SELECT parent_category from Categories WHERE category_name = '{category}'"
    category = connection.execute(statement).fetchone()[0]
    while (category != "Root"):
        categories.append(category)
        statement = f"SELECT parent_category from Categories WHERE category_name = '{category}'"
        category = connection.execute(statement).fetchone()[0]

    # Reverse category to show top-down order
    categories.reverse()
    return categories


# Returns all the leaf nodes of category hierarchy
# Used for testing
def get_leaf_categories():
    connection = sql.connect('database.db')
    # Get unique category_name (child categories) that did not occur at all in parent_category
    statement = f"SELECT DISTINCT C1.category_name from Categories C1 WHERE " \
                f"C1.category_name NOT IN (SELECT parent_category from Categories C2)"
    categories = connection.execute(statement).fetchall()

    return single_tuple_to_list(categories)


# Used to create new Listing_ID by adding +1 to maximum LID
def max_LID():
    connection = sql.connect('database.db')
    statement = f"SELECT MAX(Listing_ID) from Product_listing"
    cursor = connection.execute(statement)
    return cursor.fetchone()[0]


# Publish product lising
def publish_product(email, category, title, name, desc, price, quantity):
    # Checks if category exists and price and quantity are digits
    if category not in get_all_categories():
        return "Category does not exist, please enter an existing category"
    if not price.isdigit():
        return "Error, Price has to be an integer"
    if not quantity.isdigit():
        return "Error, Quantity has to be an integer"

    # Inserts into product_listing new product
    connection = sql.connect('database.db')
    statement = f"INSERT INTO Product_Listing (Seller_Email,Listing_ID,Category,Title,Product_Name,Product_Description," \
                f"Price, Quantity, archived, active_period) VALUES (?,?,?,?,?,?,?,?,?,?)"
    # New LID and adds $ to price digit
    lid = max_LID() + 1
    price = '$' + str(price)
    # Set archived to False and active_period to None
    values = [email, lid, category, title, name, desc, price, quantity, 0, None]
    connection.execute(statement, values)
    connection.commit()
    return None


# Removes a specific product from the listing
def remove_product(email, lid):
    connection = sql.connect('database.db')

    # Checks if the product is listed and if archived already
    statement = f"SELECT * from Product_Listing WHERE Seller_Email = '{email}' AND Listing_ID = '{lid}'"
    cursor = connection.execute(statement)
    product = cursor.fetchone()
    if product is None:
        return "Product Listing does not exist"
    if product[8] == 1:
        return "Product is already Archived"

    # For now, just removing all the products to show it works
    d = datetime.now()
    statement = f"UPDATE Product_Listing SET " \
                f"archived = 1, " \
                f"active_period = '{d}' " \
                f"WHERE Seller_Email = '{email}' AND Listing_ID = '{lid}';"
    connection.execute(statement)
    connection.commit()

    return None


# Get all the products that were listed by the seller
def get_seller_products(email):
    connection = sql.connect('database.db')
    statement = f"SELECT * from Product_Listing WHERE Seller_Email = '{email}'"
    cursor = connection.execute(statement)

    return cursor.fetchall()


# Get all the orders that were purchased by the buyer
def get_buyer_orders(email):
    connection = sql.connect('database.db')
    statement = f"SELECT * from Orders WHERE Buyer_Email = '{email}'"
    cursor = connection.execute(statement)

    return cursor.fetchall()


if __name__ == "__main__":
    main()