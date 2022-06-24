from flask import Flask, render_template, request, flash
import db_methods

app = Flask(__name__)
# Secret key needed for Flask flash, used from given link below
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

host = 'http://127.0.0.1:5000/'

email = ''


# renders the index.html template
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


# If login button was pressed, would check values given from email and password and see if it matches in database
@app.route('/login', methods=['POST', 'GET'])
def login():
    e = False
    if request.method == 'POST':
        e = db_methods.verify(request.form['useremail'], request.form['userpassword'])

        # Flask flashing https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/
        # Makes alert message to be displayed
        if e:
            global email
            email = request.form['useremail']
            return render_template('store.html', products=None, categories=db_methods.get_categories())
        else:
            flash(u'Invalid password provided', 'danger')

    return render_template('index.html')


@app.route('/category', methods=['POST', 'GET'])
def store():
    if request.method == 'POST':
        p = db_methods.get_products(request.form['category'])
        return render_template('store.html', products=p, categories=db_methods.get_categories())

    return render_template('store.html', products=None, categories=db_methods.get_categories())


# If change password button was pressed, checks if the old password is the correct password by matching it with database
# Would then change it if it is true, otherwise, would display an error message
@app.route('/password', methods= ['POST', 'GET'])
def change_password():
    e = False
    if request.method == 'POST':
        e = db_methods.change_pass(email, request.form['oldpassword'], request.form['newpassword'])

        # Makes alert message to be displayed
        if e:
            flash(u'Successfully changed password', 'success')
        else:
            flash(u'Invalid password provided', 'danger')

    return render_template('settings.html', userinfo=db_methods.display_user_info(email))


# Loads user information into settings page
@app.route('/settings', methods=['POST', 'GET'])
def settings():
    return render_template('settings.html', userinfo=db_methods.display_user_info(email))


# Returns information about specific product and category hierarchy of product
@app.route('/product', methods=['POST', 'GET'])
def product():
    p = None
    cat = None
    if request.method == 'POST':
        p = db_methods.get_specific_product(request.form['seller'], request.form['lid'])
        cat = db_methods.get_parent_categories(request.form['category'])
        print(cat)

    return render_template('product.html', product=p, categories=cat)


# Publishes product if user is a seller
@app.route('/publish', methods=['POST', 'GET'])
def publish():
    e = False
    if request.method == 'POST':
        # Get all form information
        cat = request.form['category']
        price = request.form['price']
        quantity = request.form['quantity']
        title = request.form['title']
        name = request.form['name']
        desc = request.form['desc']

        # Calls publish_product function with all information
        e = db_methods.publish_product(email,cat,title,name,desc,price,quantity)

        # Makes alert message to be displayed
        if e:
            flash(f'{e}', 'danger')
        else:
            flash(u'Successfully published product', 'success')

    # userinfo is information about the user in the publish page
    # is_seller checks if the user is a seller
    return render_template('publish.html', userinfo=db_methods.display_user_info(email), is_seller=db_methods.check_seller(email))


@app.route('/userinfo', methods=['POST', 'GET'])
def change_user_info():
    e = False

    f = request.form['first']
    l = request.form['last']
    g = request.form['gender']
    a = request.form['age']

    if request.method == 'POST':
        e = db_methods.change_user_info(email, f,l,g,a)

        # Makes alert message to be displayed
        if e == True:
            flash(u'Successfully changed user information', 'success')
        else:
            flash(f'{e}', 'danger')

    return render_template('settings.html', userinfo=db_methods.display_user_info(email))


@app.route('/address', methods=['POST', 'GET'])
def change_address():
    e = False
    if request.method == 'POST':
        # Request form information to change address
        a = request.form['address_id']
        z = request.form['zip']
        snum = request.form['streetnum']
        sname = request.form['street']

        e = db_methods.change_address(a, z, snum, sname)

        # Makes alert message to be displayed
        if e == True:
            flash(u'Successfully changed address', 'success')
        else:
            flash(f'{e}', 'danger')

    return render_template('settings.html', userinfo=db_methods.display_user_info(email))


# Deletes a product listing
@app.route('/listing', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        # Takes only the LID from the seller
        lid = request.form["lid"]

        # Removes the product
        e = db_methods.remove_product(email,lid)

        # Makes alert message to be displayed
        if e:
            flash(f'{e}', 'danger')
        else:
            flash(u'Successfully removed product', 'success')

    # if user is not a seller, display their past orders instead
    if db_methods.check_seller(email):
        return render_template('listing.html', products=db_methods.get_seller_products(email), is_seller=True)
    else:
        return render_template('listing.html', orders=db_methods.get_buyer_orders(email), is_seller=False)

if __name__ == "__main__":
    app.run()


