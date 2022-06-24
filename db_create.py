import sqlite3 as sql
import csv
import hashlib

# Global array for all the names of each dataset
datasets = ['Users', 'Address', 'Buyers', 'Categories', 'Credit_cards', 'Local_Vendors', 'Orders',
            'Product_Listing',  'Sellers', 'Zipcode_info']

# Will not be doing rating/reviews
# 'Ratings', 'Reviews',

# First function that will be called
def main():
    create_tables()

    for table in datasets:
        print(table)
        populate(table)


# Creates the data tables for each csv file given
# No foreign keys used yet, just declaring data types and primary keys for each attribute
def create_tables():
    connection = sql.connect('database.db')

    # Users(email, password)
    connection.execute('CREATE TABLE IF NOT EXISTS users('
                       'email TEXT, '
                       'password TEXT, '
                       'PRIMARY KEY (email));')

    # Address(address_id,zipcode,street_num,street_name)
    connection.execute("CREATE TABLE IF NOT EXISTS address("
                       "address_id TEXT, "
                       "zipcode INTEGER, "
                       "street_num INTEGER, "
                       "street_name TEXT, "
                       "PRIMARY KEY (address_id), "
                       "FOREIGN KEY (zipcode) REFERENCES zipcode_info (zipcode))")

    # Buyers: Buyers is a subset of the Users.
    connection.execute("CREATE TABLE IF NOT EXISTS buyers("
                       "email TEXT, "
                       "first_name TEXT, "
                       "last_name TEXT, "
                       "gender TEXT, "
                       "age INTEGER, "
                       "home_address_id TEXT, "
                       "billing_address_id TEXT, "
                       "PRIMARY KEY (email), "
                       "FOREIGN KEY (email) REFERENCES users (email) ON DELETE CASCADE,"
                       "FOREIGN KEY (home_address_id) REFERENCES address (address_id), "
                       "FOREIGN KEY (billing_address_id) REFERENCES address (address_id))")

    # Categories(parent_category, category_name)
    connection.execute("CREATE TABLE IF NOT EXISTS categories("
                       "parent_category TEXT, "
                       "category_name TEXT, "
                       "PRIMARY KEY(category_name))")

    # Credit cards stored in the system.
    connection.execute("CREATE TABLE IF NOT EXISTS credit_cards("
                       "credit_card_num TEXT, "
                       "card_code INTEGER, "
                       "expire_month INTEGER, "
                       "expire_year INTEGER, "
                       "card_type TEXT, "
                       "Owner_email TEXT,"
                       "PRIMARY KEY (credit_card_num), "
                       "FOREIGN KEY (Owner_email) REFERENCES users (email) ON DELETE CASCADE)")

    # Local_Vendors(Email, Business_Name, Business_Address_ID, Customer_Service_Number)
    connection.execute("CREATE TABLE IF NOT EXISTS local_vendors("
                       "email TEXT, "
                       "business_name TEXT, "
                       "business_address_ID TEXT , "
                       "customer_Service_Number TEXT,"
                       "PRIMARY KEY (email))")

    # Orders(Transaction_ID, Seller_Email, Listing_ID, Buyer_Email, Date, Quantity, Payment)
    connection.execute("CREATE TABLE IF NOT EXISTS orders("
                       "transaction_id INTEGER, "
                       "seller_email TEXT, "
                       "listing_id INTEGER, "
                       "buyer_email TEXT, "
                       "date TEXT, "
                       "quantity INTEGER, "
                       "payment REAL,"
                       "PRIMARY KEY (transaction_id)"
                       "FOREIGN KEY (seller_email, transaction_id) REFERENCES product_listing (seller_email, listing_id), "
                       "FOREIGN KEY (buyer_email) REFERENCES buyers (email) ON DELETE NO ACTION)")


    # ADDED NEW ACTIVE BOOLEAN AND ACTIVE PERIOD DATE
    # Product_Listings(Seller_Email, Listing_ID, Category, Title, Product_Name, Product_Description, Price, Quantity)
    connection.execute("CREATE TABLE IF NOT EXISTS product_listing("
                       "seller_email TEXT, "
                       "listing_id INTEGER, "
                       "category TEXT, "
                       "title TEXT, "
                       "product_name TEXT, "
                       "product_description TEXT, "
                       "price REAL, "
                       "quantity INTEGER, "
                       "archived INTEGER, "
                       "active_period TEXT, "
                       "PRIMARY KEY (seller_email, listing_id), "
                       "FOREIGN KEY (seller_email) REFERENCES sellers (email) ON DELETE NO ACTION, "
                       "FOREIGN KEY (category) REFERENCES categories (category_name))")

    # Will not be doing ratings/reviews
    """
    # Ratings(Buyer_Email,  Seller_Email, Date, Rating, Rating_Desc)
    connection.execute("CREATE TABLE IF NOT EXISTS ratings("
                       "buyer_email TEXT, "
                       "seller_email TEXT, "
                       "date TEXT, "
                       "rating INTEGER, "
                       "rating_desc TEXT,"
                       "PRIMARY KEY( buyer_email, seller_email, date))")

    # Reviews(Buyer_Email, Seller_Email, Listing_ID, Review_Desc)
    connection.execute("CREATE TABLE IF NOT EXISTS reviews ("
                       "buyer_email TEXT, "
                       "seller_email TEXT, "
                       "listing_id INTEGER, "
                       "review_desc TEXT, "
                       "PRIMARY KEY (buyer_email, seller_email, listing_id))")
    """

    # Sellers (email, routing_number, account_number, balance)
    connection.execute("CREATE TABLE IF NOT EXISTS sellers("
                       "email TEXT, "
                       "routing_number INTEGER, "
                       "account_number INTEGER, "
                       "balance REAL, "
                       "PRIMARY KEY (email), "
                       "FOREIGN KEY (email) REFERENCES users (email) ON DELETE CASCADE)")

    # Zipcode_Info(zipcode, city, state_id, population, density, county_name, timezone)
    connection.execute("CREATE TABLE IF NOT EXISTS zipcode_info("
                       "zipcode INTEGER, "
                       "city TEXT, "
                       "state_id TEXT, "
                       "population INTEGER, "
                       "density REAL, "
                       "county_name TEXT, "
                       "timezone TEXT, "
                       "PRIMARY KEY (zipcode))")
    connection.commit()


# Responsible for populating the table given, if it is a user table then the passwords are hashed first
def populate(table):
    connection = sql.connect('database.db')

    # Clear out table beforehand to prevent reentry of same rows
    connection.execute('DELETE FROM ' + table)

    # pathway to .csv file
    path = "NittanyMarketDataset-Final/" + table + ".csv"

    # encoding as utf-8-sig to prevent the characters ï»¿ from appearing
    # https://stackoverflow.com/questions/34399172/why-does-my-python-code-print-the-extra-characters-%C3%AF-when-reading-from-a-tex
    with open(path, 'r', encoding="utf-8-sig") as data:
        # using DictReader from .csv library to convert csv file into a python dictionary
        for line in csv.DictReader(data):

            # Used method from below to convert python dictionary into sql insert statements
            # https://stackoverflow.com/questions/9336270/using-a-python-dict-for-a-sql-insert-statement
            temp = ', '.join(['?'] * len(line))
            columns = ', '.join(line.keys())

            statement = f"INSERT INTO {table} ({columns}) VALUES ( {temp} )"

            # Checks if table is specifically a users table in order to hash passwords
            if table == 'Users':
                h = hashlib.md5(line['password'].encode())
                hashed = h.hexdigest()
                connection.execute(statement, (line['email'], hashed))
            elif table == 'Product_Listing':
                # Add new column values for Product Listing
                columns = columns + ", archived, active_period"
                temp = temp + ",?,?"

                line['archived'] = 0
                line['active_period'] = ''
                statement = f"INSERT INTO {table} ({columns}) VALUES ( {temp} )"
                connection.execute(statement, list(line.values()))
            else:
                connection.execute(statement, list(line.values()))

    connection.commit()


# Prints a given table
def print_table(table):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM ' + table + ';')
    print(cursor.fetchall())


if __name__ == "__main__":
    main()