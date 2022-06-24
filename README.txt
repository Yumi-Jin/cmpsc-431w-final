NittanyMarket Project
Used PyCharm for entire project, using Flask and python for backend, sqlite3 for storage, and html for frontend.

main.py
Deals with retrieving information from the user/html files and sends information back using Flask and python
Would call functions from db_methods to process information, would then load the html template with new information
    index(): used to load the html for login page
    login(): took information from input box and called login function, loads html for login page or store page
    store(): loads all products and category
    settings(): loads the user settings page
    change_password(): changes the password from user setting page
    product(): loads specific information about product
    publish(): publishes product
    change_user_info(): updates user information
    change_address(): updates address for home or billing
    delete(): deletes product listing

db_methods.py
Processes given information and connects it to the database with sqlite3 and python
    verify(email, password): checks if user and password is correct
    check_seller(email): checks if user is a seller
    change_pass(email, old_password, new_password): changes password
    display_user_info(email): displays user information from Buyers, Address, and Credit_cards
    change_user_info(email, first_name, last_name, gender, age): changes some or all user information
    address_info(address_id): gets address information for display_user_info(email)
    change_address(address_id, zipcode, street_num, street_name): changes some or all address information
    get_all_categories(): grabs all unique categories from Categories
    get_products(category): grabs all products with category = category
    get_specific_product(email,lid): grabs all information of specific product
    get_categories(): converts all categories into hashtable for easy access
    single_tuple_to_list(tup): convenient function to turn tuple into a list
    subcategory(category): grabs subcategory of specific category, used for get_categories()
    get_parent_categories(category): get all parent categories of specific category in order to display
    get_leaf_categories(): for testing, returns all leaf categories
    max_LID(): returns maximum listing_id to create new LID
    publish_product(email, category, title, name, desc, price, quantity): publish new product listing
    remove_product(email, lid): archives specific product
    get_seller_products(email): get all products listed from seller
    get_buyer_orders(email): get all buyer orders

db_create.py
    main(): calls db creation functions
    create_tables(): creates the tables and initializes attributes
    populate(table): populates each table, unique for product listing and users
    print_table(table): for testing, prints out specific table

index.html: login page
store.html: store page to display products
listing.html: displays product listing or orders
product.html: displays specific product
settings.html: displays user information and addresses, change password
publish.html: publishes product if user is a seller

Resources-------------------------------------------------------------------------
Main bootstrap stylesheet by https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css
CSS stylesheet by https://bbbootstrap.com/snippets/bootstrap-login-form-social-buttons-43836301
Store template by https://bbbootstrap.com/snippets/bootstrap-ecommerce-category-product-list-page-93685579
Login page template by https://bbbootstrap.com/snippets/bootstrap-login-form-social-buttons-43836301
Settings page template by https://www.bootdey.com/snippets/view/dark-profile-settings

Boot strap references
https://bootstrapious.com/p/bootstrap-sidebar
https://mdbootstrap.com/docs/standard/navigation/headers/#section-introduction

Flask Flash reference
https://www.codegrepper.com/code-examples/python/flask+alert+popup