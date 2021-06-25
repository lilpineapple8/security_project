class User():
    def __init__(self, counterId,user_username,user_password, user_email,user_number):
        self.__user_id = counterId
        self.__user_username = user_username
        self.__user_password = user_password
        self.__user_email = user_email
        self.__user_number = user_number

    def get_id(self):
        return self.__user_id

    def get_user_username(self):
        return self.__user_username

    def get_user_password(self):
        return self.__user_password

    def get_user_email(self):
        return self.__user_email

    def get_user_number(self):
        return self.__user_number

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_user_username(self, user_username):
        self.__user_username = user_username

    def set_user_password(self, user_password):
        self.__user_password = user_password

    def set_user_email(self, user_email):
        self.__user_email = user_email

    def set_user_number(self, user_number):
        self.__user_number = user_number

class Product():
    def __init__(self, counterId,combine_id ,name, price, quantity, remark, file):
        self.__product_id = counterId
        self.__combine_id = combine_id
        self.__name = name
        self.__price = price
        self.__quantity = quantity
        self.__file = file
        self.__remark = remark

    def get_product_id(self):
        return self.__product_id

    def get_combine_id(self):
        return self.__combine_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_quantity(self):
        return self.__quantity

    def get_file(self):
        return self.__file

    def get_remark(self):
        return self.__remark

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def set_combine_id(self, combine_id):
        self.__combine_id = combine_id

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_file(self, file):
        self.__file = file

    def set_remark(self, remark):
        self.__remark = remark

class Order():
    def __init__(self,count_id,product_name, quantity,product_price,remarks):

        self.__order_id = count_id
        self.__product_name = product_name
        self.__quantity = quantity
        self.__product_price = product_price
        self.__remarks = remarks

    # accessor
    def get_order_id(self):
        return self.__order_id

    def get_product_name(self):
        return self.__product_name

    def get_price(self):
        return self.__product_price

    def get_quantity(self):
        return self.__quantity

    def get_remarks(self):
        return self.__remarks


    # mutator
    def set_order_id(self, order_id):
        self.__order_id = order_id

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_price(self, product_price):
        self.__product_price = product_price

    def set_remarks(self, remarks):
        self.__remarks = remarks

class Payment():
    def __init__(self,payment_id,name, address, payment, price,credit,delivery_status, remark):
        self.__payment_id = payment_id
        self.__name = name
        self.__address = address
        self.__payment = payment
        self.__price = price
        self.__credit = credit
        self.__delivery_status = delivery_status
        self.__remark = remark

    # accessor
    def get_payment_id(self):
        return self.__payment_id

    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address

    def get_payment(self):
        return self.__payment

    def get_price(self):
        return self.__price

    def get_credit(self):
        return self.__credit

    def get_delivery_status(self):
        return self.__delivery_status

    def get_remark(self):
        return self.__remark

    # mutator
    def set_payment_id(self,payment_id):
        self.__payment_id = payment_id

    def set_name(self, name):
        self.__name = name

    def set_address(self, address):
        self.__address = address

    def set_payment(self, payment):
        self.__payment = payment

    def set_price(self, price):
        self.__price = price

    def set_credit(self,credit):
        self.__credit = credit

    def set_delivery_status(self, delivery_status):
        self.__delivery_status = delivery_status

    def set_remark(self, remark):
        self.__remark = remark
