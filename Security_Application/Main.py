from flask import Flask, render_template, request, redirect, url_for, session, current_app, flash
from Forms import LoginForm, CreateStaffForm, CreateOrderForm, CreateProductForm, CreatePaymentForm, CreateDeliveryForm
from Classes import User, Product, Order, Payment
import shelve
import os
from werkzeug.utils import secure_filename
import pathlib

dir = pathlib.Path().absolute()
dir = dir / 'static' / 'tmp'
UPLOAD_FOLDER = dir
ALLOWED_EXTENSIONS = {'png', 'jpg'}


app = Flask(__name__, static_url_path="/static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home page "Login"
@app.route('/login',methods=['GET', 'POST'])
def admin_home():
    create_user_form = LoginForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        user_dict = {}
        db = shelve.open('userMember.db', 'c')
        try:
            user_dict = db['user']
        except:
            print("Error in retrieving User from storage.db.")

        for key in user_dict:
            if user_dict[key].get_user_username() == create_user_form.username.data:
                if create_user_form.password.data == user_dict[key].get_user_password():
                    session['Username'] = request.form['username']
                    return redirect(url_for('home'))

        return render_template('login.html',form=create_user_form)

    return render_template('login.html',form=create_user_form)

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    create_user_form = CreateStaffForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        user_dict = {}
        db = shelve.open('userMember.db', 'c')
        counterID = 0
        try:
            user_dict = db['user']
            counterID = db["CounterID"]
        except:
            print("Error in retrieving User from storage.db.")

        user = User(counterID, create_user_form.username.data, create_user_form.password.data, create_user_form.email.data, create_user_form.phone.data)
        user_dict[user.get_id()] = user
        db['user'] = user_dict

        counterID += 1
        db["CounterID"] = counterID
        db.close()
        return redirect(url_for('admin_home'))

    return render_template('register.html', form=create_user_form)

# Home page
@app.route('/')
def home():
    products_dict = {}
    db = shelve.open('storage.db', 'c')
    try:
        products_dict = db['products']
    except:
         return render_template('home.html')
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)
    if not session:
        return render_template('home.html', products_list = products_list)
    return render_template('home.html', products_list = products_list)

# Create Product
@app.route('/createProduct', methods=['GET', 'POST'])
def create_product():
    create_user_form = CreateProductForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        products_dict = {}
        db = shelve.open('storage.db', 'c')
        counterID = 0

        try:
            products_dict = db['products']
            counterID = db["CounterID"]
        except:
            print("Error in retrieving products from storage.db.")

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        for x in os.listdir(dir):
            y = str(file.filename)
            if y.lower() == x.lower():
                return "This file name is clashing with one existing in the database, please rename the field!"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        combine_id = session['Username']

        product = Product(str(counterID), combine_id, create_user_form.name.data, create_user_form.price.data, create_user_form.quantity.data, create_user_form.remark.data, file.filename)
        counterID += 1
        db["CounterID"] = counterID

        products_dict[product.get_product_id()] = product
        db['products'] = products_dict
        db.close()
        return redirect(url_for('home'))
    return render_template('createproduct.html', form=create_user_form)

# create order
@app.route('/Order/<id>', methods=['GET', 'POST'])
def order(id):
    create_order_form = CreateOrderForm(request.form)
    products_dict = {}
    db2 = shelve.open('storage.db','w')
    try:
        products_dict = db2['products']
    except:
        pass

    product = products_dict.get(id)

    create_order_form.product_name.data = product.get_name()
    create_order_form.price.data = product.get_price()

    if request.method == 'POST' and create_order_form.validate():
        orders_dict = {}
        db = shelve.open('products.db', 'c')

        counter=0
        try:
            orders_dict = db['Orders']
            counter=db['counter']
        except:
            print("Error in retrieving Orders from storage.db.")

        counter+=1
        a= "y21-"+str(counter)

        if create_order_form.quantity.data <= product.get_quantity():

            newquantity = product.get_quantity() - create_order_form.quantity.data
            cost = product.get_price() * create_order_form.quantity.data
            print(cost)
            product.set_quantity(newquantity)

            db2['products'] = products_dict

            order = Order(a, create_order_form.product_name.data, create_order_form.quantity.data, cost ,create_order_form.remarks.data)
            orders_dict[order.get_order_id()] = order
            print(create_order_form.price.data)
            db['Orders'] = orders_dict

            db['counter']= counter

            db.close()
            db2.close()
            return redirect(url_for('create_payment',id = order.get_order_id()))

        db.close()
        db2.close()
    return render_template('cart.html', form=create_order_form)

# create payment
@app.route('/payment/<id>',methods=['GET','POST'])
def create_payment(id):
    create_payment_form = CreatePaymentForm(request.form)
    products_dict = {}
    db2 = shelve.open('products.db','w')
    try:
        products_dict = db2['Orders']
    except:
        pass

    product = products_dict.get(id)
    create_payment_form.price.data = product.get_price()
    if request.method == 'POST' and create_payment_form.validate():
        payment_dict = {}
        db = shelve.open('storage.db', 'c')
        counter = 0
        try:
            payment_dict = db['payment']
            order_dict = db['Orders']
            counter=db['counter']
        except:
            print("Error in retrieving Payment from storage.db.")

        payment = Payment(product.get_order_id(), create_payment_form.name.data,create_payment_form.address.data,create_payment_form.payment.data,create_payment_form.price.data,create_payment_form.credit.data,'Processing',product.get_remarks())
        print(product.get_remarks())
        payment_dict[payment.get_payment_id()] = payment

        db['payment'] = payment_dict

        db.close()

        return redirect(url_for('home'))
    return render_template('payment.html', form=create_payment_form)

# retrieve product
@app.route('/retrieveProducts')
def retrieve_products():
    products_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        products_dict = db['products']
    except:
        pass

    db.close()
    combine_id = session['Username']
    products_list = []
    for key in products_dict:
        if combine_id == products_dict[key].get_combine_id():
            product = products_dict.get(key)
            products_list.append(product)

    return render_template('productListing.html', count=len(products_list), products_list=products_list)

#Delete product
@app.route('/deleteProducts/<id>', methods=['POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('storage.db', 'w')
    products_dict = db['products']

    products_dict.pop(id)

    db['products'] = products_dict
    db.close()

    return redirect(url_for('retrieve_products'))

# Update Product
@app.route('/updateProducts/<id>/', methods=['GET', 'POST'])
def update_products(id):
    update_products_form = CreateProductForm(request.form)
    if request.method == 'POST' and update_products_form.validate():
        product_dict = {}
        db = shelve.open('storage.db', 'w')
        product_dict = db['products']

        product = product_dict.get(id)
        product.set_name(update_products_form.name.data)
        product.set_price(update_products_form.price.data)
        product.set_quantity(update_products_form.quantity.data)
        product.set_remark(update_products_form.remark.data)

        db['products'] = product_dict
        db.close()

        return redirect(url_for('retrieve_products'))
    else:
        product_dict = {}
        db = shelve.open('storage.db', 'r')
        product_dict = db['products']
        db.close()

        product = product_dict.get(id)
        update_products_form.name.data = product.get_name()
        update_products_form.price.data = product.get_price()
        update_products_form.quantity.data = product.get_quantity()
        update_products_form.remark.data = product.get_remark()

        return render_template('Updatepage.html', form=update_products_form)

# Retrieve Deliveries
@app.route('/retrieveDeliveries')
def retrieve_deliveries():
    deliveries_dict = {}
    try:
        db = shelve.open('storage.db', 'c')
        deliveries_dict = db['payment']

    except:
        return render_template('retrieveDeliveries.html')

    delivery_list = []
    for key in deliveries_dict:
        delivery = deliveries_dict[key]
        delivery_list.append(delivery)

    db.close()
    return render_template('retrieveDeliveries.html', count=len(delivery_list), delivery_list=delivery_list)

# Delete Deliveries
@app.route('/deleteDelivery/<id>', methods=['POST'])
def delete_delivery(id):
    deliveries_dict = {}
    db = shelve.open('storage.db', 'w')
    deliveries_dict = db['payment']
    deliveries_dict.pop(id)

    db['payment'] = deliveries_dict
    db.close()

    return redirect(url_for('retrieve_deliveries'))

# Update Status
@app.route('/updateDelivery/<id>/', methods=['GET', 'POST'])
def update_delivery(id):
    update_delivery_form = CreateDeliveryForm(request.form)
    if request.method == 'POST' and update_delivery_form.validate():
        deliveries_dict = {}
        db = shelve.open('storage.db', 'w')
        deliveries_dict = db['payment']

        delivery = deliveries_dict.get(id)
        delivery.set_delivery_status(update_delivery_form.delivery_status.data)
        db['payment'] = deliveries_dict

        db.close()

        return redirect(url_for('retrieve_deliveries'))
    else:
        deliveries_dict = {}
        db = shelve.open('storage.db', 'r')
        deliveries_dict = db['payment']
        db.close()
        id = str(id)

        delivery = deliveries_dict.get(id)
        update_delivery_form.order_id.data = delivery.get_payment_id()
        update_delivery_form.address.data = delivery.get_address()
        update_delivery_form.delivery_status.data = delivery.get_delivery_status()
        update_delivery_form.delivery_details.data = delivery.get_remark()

        return render_template('updateDelivery.html', form=update_delivery_form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(port=5003, debug=True)


