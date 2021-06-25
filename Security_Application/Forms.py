from wtforms import Form, StringField, PasswordField, validators, ValidationError,IntegerField, TextAreaField,SelectField,RadioField,FloatField
from flask_wtf.file import FileField
from wtforms.fields.html5 import EmailField
import shelve

def validate_username(form,field):
    db=shelve.open("retailer.db","c")
    retailerDict={}
    try:
        retailerDict=db['Retailer']
    except:
        pass

    if len(retailerDict)>0:
        for key in retailerDict:
            if field.data == retailerDict[key].get_retail_username():
                raise ValidationError("Username exists")

def validate_staff(form,field):
    db=shelve.open("staffMember.db","c")
    staffDict={}
    try:
        staffDict=db['Staff']
    except:
        pass

    if len(staffDict)>0:
        for key in staffDict:
            if field.data == staffDict[key].get_staff_username():
                raise ValidationError("Username exists")

class CreateUserForm(Form):
    username = StringField('Username',[validators.Length(min=1, max=150),validators.DataRequired(),validate_username])
    email = EmailField('email',[validators.Email(message=None, granular_message=False, check_deliverability=True, allow_smtputf8=True, allow_empty_local=False),validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Re-Password')
    phone = IntegerField('phone', [validators.DataRequired()])
    company = StringField('Company',[validators.Length(min=1, max=150),validators.DataRequired(),validate_username])
    category = SelectField('Category',[validators.DataRequired()],choices=[('','Select'),('Home','Home'),('Computer & Accessories','Computer & Accessories'),('Grocery','Grocery'),('Baby','Baby'),('Toy & Games','Toy & Games'),('other','other')],default='',validate_choice=True)

class UpdateUserForm(Form):
    username = StringField('Username',[validators.Length(min=1, max=150),validators.DataRequired()])
    email = EmailField('email',[validators.Email(message=None, granular_message=False, check_deliverability=True, allow_smtputf8=True, allow_empty_local=False),validators.DataRequired()])
    phone = IntegerField('phone', [validators.DataRequired()])

class UpdateRetailerForm(Form):
    username = StringField('Username',[validators.Length(min=1, max=150),validators.DataRequired()])
    email = EmailField('email',[validators.Email(message=None, granular_message=False, check_deliverability=True, allow_smtputf8=True, allow_empty_local=False),validators.DataRequired()])
    phone = IntegerField('phone', [validators.DataRequired()])
    company = StringField('Company',[validators.Length(min=1, max=150),validators.DataRequired(),validate_username])
    category = SelectField('Category',[validators.DataRequired()],choices=[('','Select'),('Home','Home'),('Computer & Accessories','Computer & Accessories'),('Grocery','Grocery'),('Baby','Baby'),('Toy & Games','Toy & Games'),('other','other')],default='',validate_choice=True)
    pending = SelectField('Pending', [validators.DataRequired()], choices=[('pending','pending'),('accept','accept'),('reject','reject')],validate_choice=True)

class CreateStaffForm(Form):
    username = StringField('Username',[validators.Length(min=1, max=150),validators.DataRequired(),validate_staff])
    email = EmailField('email',[validators.Email(message=None, granular_message=False, check_deliverability=False, allow_smtputf8=True, allow_empty_local=False),validators.DataRequired()])
    phone = IntegerField('phone', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Re-Password')

class LoginForm(Form):
    username = StringField('username',[validators.Length(min=1, max=150),validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class CreateProductForm(Form):
    name = StringField('Product Name', [validators.Length(min=1, max=50), validators.DataRequired()])
    price = FloatField('Product Price', [validators.NumberRange(min=0, max=9999999999)])
    quantity = IntegerField('Product Quantity', [validators.NumberRange(min=0, max=9999)])
    remark = TextAreaField('Remarks', [validators.Optional()])
    file = FileField('Image', [validators.Optional()])

class CreateOrderForm(Form):
    product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    quantity = IntegerField('Quantity', [validators.DataRequired()], default=1)
    price = FloatField('Price', [validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])

class CreatePaymentForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=1, max=100), validators.DataRequired()])
    payment = RadioField('Payment Choice',choices=[('V', 'Visa'), ('M', 'MasterCard'), ('A', 'American Express'), ('J', 'JCB')],default='V')
    price = FloatField('Price', [validators.DataRequired()])
    credit = IntegerField('Credit Card Number', [validators.DataRequired()])
    cvc = IntegerField('CVC',[validators.DataRequired()])

class passwordResetRequestForm(Form):
    email = EmailField('email',[validators.Email(message=None, granular_message=False, check_deliverability=False, allow_smtputf8=True, allow_empty_local=False),validators.DataRequired()])

class passwordResetForm(Form):
    password = PasswordField('Password', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Re-Password')

class CreateDeliveryForm(Form):
    order_id = StringField('Order Id', [validators.Length(min=1, max=150), validators.DataRequired()])
    address = StringField('Address',[validators.Length(min=1, max=150), validators.DataRequired()])
    delivery_details = StringField('Delivery Details')
    delivery_status = RadioField('Delivery Status', choices=[('Delivered'),('On the way'),('Not Delivered')])


