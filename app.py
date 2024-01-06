from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, session, g
from models.products import ProductModel
from models.contact import ContactModel
from models.order import OrderModel
from models.dbconnect import DatabaseConnection
from models.brands import BrandModel
from models.users import UserModel
from werkzeug.utils import secure_filename
import os
from flask import request
app = Flask(__name__)
db_connection = DatabaseConnection()
app.secret_key = 'your_secret_key'
user_model = UserModel()
product_model = ProductModel()
contact_model = ContactModel()
order_model = OrderModel()
brand_model = BrandModel(db_connection)
UPLOAD_FOLDER = '/static/img/products'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cart = []

@app.before_request
def before_request():
    g.dn = session.get('user_id', 0)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_model.login(username,password)
        if user:
            if user['PQ']!=2:
                session.clear()
                flash('Đăng nhập thành công', 'success')
                session['user_id'] = user['ID']
                session['address'] = user['Diachi']
                session['name'] = user['Hoten']
                session['pq'] = user['PQ']
                return redirect("/")
            else:
                return render_template('login.html', ban="Tài khoản này đã bị khoá!")
        else:
            return render_template('login.html', ban="Tên đăng nhập hoặc mật khẩu không đúng!")
    session.clear()
    return render_template('login.html')

@app.route('/logout')
def logout():
    #session.pop('user_id', None)
    cart.clear()
    session.clear()
    return redirect("/")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        tk=request.form['tk']
        x = user_model.check_tk(tk)
        if x:
            return render_template('register.html',ban="Tài khoản đã tồn tại!")
        else:
            ht=request.form['name']
            mk=request.form['mk']
            e=request.form['email']
            sdt=request.form['sdt']
            dc=request.form['dc']
            user_model.register(ht,tk,mk,e,sdt,dc)
            return redirect("/login")
    return render_template('register.html')
    

@app.route('/img/<path:filename>')
def serve_img(filename):
    return send_from_directory('static/img', filename)

@app.route('/img/products/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/img/products', filename)

@app.route('/static/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static/css', filename)

@app.route('/')
def get_data():
    products = product_model.get_products()
    brands = brand_model.get_brands()
    return render_template('index.html', products=products, brands=brands , product_count=0)

@app.route('/products')
def get_AllProduct():
    products = product_model.get_products()
    return render_template('products.html', products=products)

@app.route('/contact')
def contact():
    contact = contact_model.get_contact()
    return render_template('contact.html', contact=contact)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    product_name = request.form['product_name']
    product_img = request.form['product_img']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])
    for item in cart:
        if item['id'] == product_id:
            item['_shopping_quantity'] += quantity
            return redirect('/')
    product = {
        'id': product_id,
        'name': product_name,
        'img': product_img,
        'price': price,
        '_shopping_quantity': quantity
    }
    cart.append(product)
    return redirect('/')

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form['product_id']
    for item in cart:
        if item['id'] == product_id:
            cart.remove(item)
            break
    return redirect('/cart')

@app.route('/cart')
def view_cart():
    total = sum(product['price'] * product['_shopping_quantity'] for product in cart)
    return render_template('cart.html', cart=cart, total_money=total)

@app.route('/checkout')
def checkout():
    if 'user_id' in session:
        user_id = session['user_id']
        address = session['address']
    else:
        return redirect('/login')
    total = sum(product['price'] * product['_shopping_quantity'] for product in cart)
    order_id = order_model.create_order(user_id, total, address)
    for product in cart:
        product_id = product['id']
        quantity = product['_shopping_quantity']
        price_per_unit = product['price']
        price = price_per_unit * quantity
        order_model.create_order_detail(order_id, product_id, quantity, price)
    cart.clear()
    return """
    <script>
        alert('Đặt hàng thành công!');
        window.location.href = '/cart';
    </script>
    """
@app.route('/admin')
def admin():
    if 'user_id' in session and 'pq' in session:
        if session['pq'] == 1:
            return render_template('admin/adminHome.html')
        else:
            return redirect("/")
    else:
        return redirect("/login")

@app.route('/admin/products')
def adminProducts():
    if 'user_id' in session and 'pq' in session:
        if session['pq'] == 1:
            products = product_model.get_products()
            return render_template('admin/products/adminProducts.html', products=products, title="Quản lý sản phẩm")
        else:
            return redirect("/")
    else:
        return redirect("/login")

@app.route('/admin/products/addproduct', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        img = request.files['img']
        loaisp = request.form['loaisp']

        if img:
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.root_path, 'static', 'img', 'products', filename))
        else:
            filename = None

        product_model.create_product(name, price, description, filename, loaisp)
        flash('Sản phẩm đã được thêm thành công', 'success')
        return redirect('/admin/products')
    brands=brand_model.get_brands()
    return render_template('admin/products/addProduct.html', brands=brands, title="Thêm sản phẩm")

@app.route('/admin/products/editproduct/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = product_model.get_product_by_id(product_id)
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        img = request.files['img']
        loaisp = int(request.form['loaisp'])
        x = request.form['x']
        if img:
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.root_path, 'static', 'img', 'products', filename))
        else:
            filename = x

        product_model.update_product(product_id, name, price, description, filename, loaisp)
        flash('Sản phẩm đã được cập nhật thành công', 'success')
        return redirect('/admin/products')
    brands=brand_model.get_brands()
    return render_template('admin/products/detail.html', brands=brands, product=product)

@app.route('/admin/products/deleteproduct/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product_model.delete_product(product_id)
    flash('Sản phẩm đã được xóa thành công', 'success')
    return redirect('/admin/products')

@app.route('/admin/orders')
def adminOrders():
    if 'user_id' in session and 'pq' in session:
        if session['pq'] == 1:
            order = order_model.get_orders()
            return render_template('admin/orders/adminOrders.html', orders=order, title="Quản lý đơn hàng")
        else:
            return redirect("/")
    else:
        return redirect("/login")
    
@app.route('/admin/orders/<int:order_id>', methods=['GET', 'POST'])
def Orderdetail(order_id):
    if 'user_id' in session and 'pq' in session:
        if session['pq'] == 1:
            if request.method == 'POST':
                tt=request.form['tt']
                order_model.update_order(order_id,tt)
                return redirect("/admin/orders")
            order = order_model.get_orders_detail(order_id)
            return render_template('admin/orders/adminOrderdetail.html', order=order, title="Chi tiết đơn hàng")
        else:
            return redirect("/")
    else:
        return redirect("/login")

@app.route('/admin/users')
def adminUsers():
    if 'user_id' in session and 'pq' in session:
        if session['pq'] == 1:
            users = user_model.get_users()
            return render_template('admin/users/adminUsers.html', users=users, title="Quản lý người dùng")
        else:
            return redirect("/")
    else:
        return redirect("/login")

@app.route('/admin/users/adduser', methods=['GET', 'POST'])
def AddUser():
    if 'user_id' in session and 'pq' in session:
        if session['pq'] == 1:
            if request.method == 'POST':
                ht=request.form['name']
                tk=request.form['tk']
                mk=request.form['mk']
                e=request.form['email']
                sdt=request.form['sdt']
                dc=request.form['dc']
                pq=request.form['pq']
                user_model.create_user(ht,tk,mk,e,sdt,dc,pq)
                return redirect("/admin/users")
            return render_template('admin/users/adminAddUser.html', title="Thêm người dùng")
        else:
            return redirect("/")
    else:
        return redirect("/login")        

@app.route('/admin/users/<int:user_id>', methods=['GET', 'POST'])
def Userdetail(user_id):
    if 'user_id' in session and 'pq' in session:
        if session['pq'] == 1:
            if request.method == 'POST':
                ht=request.form['name']
                tk=request.form['tk']
                mk=request.form['mk']
                e=request.form['email']
                sdt=request.form['sdt']
                dc=request.form['dc']
                pq=request.form['pq']
                user_model.update_user(user_id, ht,tk,mk,e,sdt,dc,pq)
                return redirect("/admin/users")
            user = user_model.get_user_detail(user_id)
            return render_template('admin/users/adminUserdetail.html', user=user, title="Thông tin người dùng")
        else:
            return redirect("/")
    else:
        return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True)
