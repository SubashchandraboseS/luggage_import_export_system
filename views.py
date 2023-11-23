# views.py
from flask import render_template, request, redirect, url_for,session
from flask import session, jsonify

from models import db, Manager,Client,Supplier,Product
from time import sleep
def init_app(app):
    @app.route('/')
    def index():
        # Check if the user is logged in (session contains 'user_type' and 'username')
        user_type = session.get('user_type')
        username = session.get('username')
        return render_template('index.html', user_type=user_type, username=username)


    @app.route('/client/login', methods=['GET', 'POST'])
    def client_login():
        if request.method == 'POST':
            print("client login")
            username = request.form.get('clientUsername')
            password = request.form.get('clientPassword')
            print(username,password)
            client = Client.query.filter_by(username=username, password=password).first()
            if client:
                print("client name is",client)
                # Set user_type and username in the session
                session['user_type'] = 'client'
                session['username'] = username
                return redirect(url_for('client_dashboard'))
        return render_template('client_login.html')

    @app.route('/client/dashboard')
    def client_dashboard():
        # Check if the user is logged in
        if 'user_type' in session and session['user_type'] == 'client':
            username = session.get('username')
            user_type= session.get('user_type')
            print("dashboard")
            return render_template('client_dashboard.html', username=username,user_type=user_type)
        return render_template('client_login.html')
        # If not logged in, redirect to the login page
        

    # Similar modifications can be made for manager and supplier



    @app.route('/client/register', methods=['GET', 'POST'])
    def client_register():
        if request.method == 'POST':
            username = request.form.get('clientUsername')
            password = request.form.get('clientPassword')
            new_client = Client(username=username, password=password)
            db.session.add(new_client)
            db.session.commit()
            # Add registration logic for the client
            return redirect(url_for('index'))
        return render_template('client_register.html')
        ################# MANAGER ########################
    @app.route('/manager/login', methods=['GET', 'POST'])
    def manager_login():
        if request.method == 'POST':
            username = request.form.get('managerUsername')
            password = request.form.get('managerPassword')
            manager = Manager.query.filter_by(username=username, password=password).first()
            if manager:
                session['user_type'] = 'manager'
                session['username'] = username
                return redirect(url_for('manager_dashboard'))
        return render_template('manager_login.html')
#MANAGER DASHBOARD
    @app.route('/manager/dashboard')
    def manager_dashboard():
        if 'user_type' in session and session['user_type'] == 'manager':
            username = session.get('username')
            user_type = session.get('user_type')
            return render_template('manager_dashboard.html', username=username, user_type=user_type)
        return render_template('manager_login.html')
    ###########Manager Register######################
    @app.route('/manager/register', methods=['GET', 'POST'])
    def manager_register():
        if request.method == 'POST':
            username = request.form.get('managerUsername')
            password = request.form.get('managerPassword')
            new_manager = Manager(username=username, password=password)
            db.session.add(new_manager)
            db.session.commit()
        # Add registration logic for the manager
            return redirect(url_for('index'))
        return render_template('manager_register.html')

    ######### SUPPLIER ##################
    @app.route('/supplier/login', methods=['GET', 'POST'])
    def supplier_login():
        if request.method == 'POST':
            username = request.form.get('supplierUsername')
            password = request.form.get('supplierPassword')
            supplier = Supplier.query.filter_by(username=username, password=password).first()
            if supplier:
                session['user_type'] = 'supplier'
                session['username'] = username
                return redirect(url_for('supplier_dashboard'))
        return render_template('supplier_login.html')

    @app.route('/supplier/dashboard',methods=['GET', 'POST'])
    def supplier_dashboard():
        if 'user_type' in session and session['user_type'] == 'supplier':
            username = session.get('username')
            user_type = session.get('user_type')

            # Get the list of products for the current supplier
            products = get_products_for_supplier()

            return render_template('supplier_dashboard.html', username=username, user_type=user_type, products=products)

        return render_template('supplier_login.html')

    @app.route('/supplier/register', methods=['GET', 'POST'])
    def supplier_register():
        if request.method == 'POST':
            username = request.form.get('supplierUsername')
            password = request.form.get('supplierPassword')
            new_supplier = Supplier(username=username, password=password)
            db.session.add(new_supplier)
            db.session.commit()
            # Add registration logic for the supplier
            return redirect(url_for('index'))
        return render_template('supplier_register.html')
        # Logout route
    @app.route('/logout')
    def logout():
        # Clear the session
        session.clear()
        return redirect(url_for('index'))
    @app.route('/logoutlink')
    def logoutlink():
        # Clear the session
        session.clear()
        return "logged out succcesfully"
    @app.route('/clear_session', methods=['GET'])
    def clear_session():
        session.clear()
        return jsonify(success=True)
###Supplier add new projects html###########
# app.py


    @app.route('/supplier/new_product', methods=['GET', 'POST'])
    def new_product():
        # Check if the user is a supplier and logged in
        if 'user_type' in session and session['user_type'] == 'supplier':
            if request.method == 'POST':
                # Retrieve form data
                name = request.form.get('product_name')
                category = request.form.get('product_category')
                price = float(request.form.get('product_price'))
                location = request.form.get('product_location')

                # Get the supplier ID using the session username
                supplier = Supplier.query.filter_by(username=session['username']).first()
                if supplier:
                    supplier_id = supplier.id

                    # Create a new Product instance
                    new_product = Product(name=name, category=category, price=price, location=location, supplier_id=supplier_id)

                    # Add the new product to the database
                    db.session.add(new_product)
                    db.session.commit()
                    print("POST Rendering supplier_dashboard.html")
                    return redirect(url_for('supplier_dashboard'))
            print("Rendering supplier_dashboard.html")
            # Render the form template for GET requests
            return render_template('supplier_dashboard.html', products=get_products_for_supplier())
        
        # Redirect to the supplier login page if the user is not logged in or not a supplier
        return render_template('supplier_login.html')


    # Helper function to get products for the current supplier
    def get_products_for_supplier():
        print("==============get_products function")
        if 'user_type' in session and session['user_type'] == 'supplier':
            supplier = Supplier.query.filter_by(username=session['username']).first()
            if supplier:
                products = Product.query.filter_by(supplier_id=supplier.id).all()
                return products
        return []
