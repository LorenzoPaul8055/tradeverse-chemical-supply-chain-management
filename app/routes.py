from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import app, db
from app.models import Product, Order, Transaction, User
from app.forms import ProductForm, OrderForm, LoginForm
from werkzeug.security import check_password_hash

# Admin Dashboard
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('login'))
    
    products = Product.query.all()
    orders = Order.query.all()
    transactions = Transaction.query.all()
    return render_template('admin_dashboard.html', products=products, orders=orders, transactions=transactions)

# Product Management - Add Product
@app.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('login'))

    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data,
                          price=form.price.data, quantity=form.quantity.data)
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully", "success")
        return redirect(url_for('view_inventory'))
    
    return render_template('add_product.html', form=form)

# Product Management - View Inventory
@app.route('/admin/view_inventory')
@login_required
def view_inventory():
    if current_user.role != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('login'))

    products = Product.query.all()
    return render_template('view_inventory.html', products=products)

# Product Management - Edit Product
@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if current_user.role != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('login'))

    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        db.session.commit()
        flash("Product updated successfully", "success")
        return redirect(url_for('view_inventory'))
    
    return render_template('edit_product.html', form=form, product=product)

# Product Management - Delete Product
@app.route('/admin/delete_product/<int:product_id>')
@login_required
def delete_product(product_id):
    if current_user.role != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('login'))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully", "success")
    return redirect(url_for('view_inventory'))

# Order Management - View Orders
@app.route('/admin/view_orders')
@login_required
def view_orders():
    if current_user.role != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('login'))

    orders = Order.query.all()
    return render_template('view_orders.html', orders=orders)

# Order Management - View Order Details
@app.route('/admin/order/<int:order_id>')
@login_required
def view_order_details(order_id):
    if current_user.role != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('login'))

    order = Order.query.get_or_404(order_id)
    return render_template('view_order_details.html', order=order)

# Order Management - Update Order Status
@app.route('/admin/update_order_status/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order_status(order_id):
    if current_user.role != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('login'))

    order = Order.query.get_or_404(order_id)
    if request.method == 'POST':
        order.status = request.form['status']
        db.session.commit()
        flash("Order status updated", "success")
        return redirect(url_for('view_orders'))

    return render_template('update_order_status.html', order=order)

# Transaction Management - View Transaction History
@app.route('/admin/transaction_history')
@login_required
def transaction_history():
    if current_user.role != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('login'))

    transactions = Transaction.query.all()
    return render_template('transaction_history.html', transactions=transactions)

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for('admin_dashboard'))
        flash("Invalid username or password", "danger")

    return render_template('login.html', form=form)

# User Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('login'))

