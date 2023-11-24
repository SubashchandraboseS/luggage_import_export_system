# views.py
from flask import render_template, request, redirect, url_for,session
from flask import session, jsonify,flash
from datetime import datetime
from models import db, Manager,Client,Supplier,Product,Booking
from time import sleep
from flask_migrate import Migrate
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
#############################################################################
   
############################################################################33333
    @app.route('/client/dashboard', methods=['GET', 'POST'])
    def client_dashboard():
        if 'user_type' in session and session['user_type'] == 'client':
            username = session.get('username')
            user_type = session.get('user_type')

            if request.method == 'POST':
                # Handle the search form submission
                search_query = request.form.get('search_query')
                products = search_products(search_query)
            else:
                # Display all active (non-blocked) products by default
                products = get_all_products_for_client()

            # Get the booked products for the client
            booked_products = get_booked_products_for_client()

            # Filter out blocked products from the list
            active_products = [product for product in products if not product.blocked]

            return render_template('client_dashboard.html', username=username, user_type=user_type, products=active_products, booked_products=booked_products)

        return render_template('client_login.html')

#################################################################################
    def get_booked_products_for_client():
        if 'user_type' in session and session['user_type'] == 'client':
            client = Client.query.filter_by(username=session['username']).first()
            if client:
                # Retrieve all booked products associated with the client
                booked_products = Product.query.join(Booking).filter(Booking.client_id == client.id).all()
                return booked_products
        return []
# Helper function to get booked products for the current client
#################################################################################
    # Helper function to search products based on the query
    def search_products(query):
        if query:
            # Perform a search based on the query
            products = Product.query.filter(
                (Product.name.ilike(f"%{query}%")) | (Product.category.ilike(f"%{query}%"))
            ).all()
            return products
        else:
            # Return all products if no query is provided
            return get_all_products_for_client()

    # Helper function to get all products for the current client
    def get_all_products_for_client():
        if 'user_type' in session and session['user_type'] == 'client':
            client = Client.query.filter_by(username=session['username']).first()
            if client:
                # Retrieve all products associated with the client
                products = Product.query.all()
                return products
        return []
    @app.route('/get_product_suggestions_client', methods=['GET'])
    def get_product_suggestions_client():
        # Retrieve the search query from the request parameters
        query = request.args.get('query', '')

        # Get product suggestions based on the query using the search_products function
        suggestions = [product.name for product in search_products(query)]

        # Return the suggestions as JSON
        return jsonify(suggestions)
    #########################Book Product
    @app.route('/client/book_product/<int:product_id>', methods=['POST'])
    def book_product(product_id):
        print("client booked")
        if 'user_type' in session and session['user_type'] == 'client':
            client = Client.query.filter_by(username=session['username']).first()
            if client:
                product = Product.query.get(product_id)
                if product:
                    # Check if the product is not already booked by the client
                    if not Booking.query.filter_by(client_id=client.id, product_id=product.id).first():
                        # Book the product
                        booking = Booking(client_id=client.id, product_id=product.id)
                        db.session.add(booking)
                        db.session.commit()
                        flash('Product booked successfully!', 'success')  # Flash a success message
                    else:
                        flash('You have already booked this product.', 'warning')
        return redirect(url_for('client_login'))
    #############################################
    @app.route('/client/unbook_product/<int:product_id>', methods=['POST'])
    def unbook_product(product_id):
        if 'user_type' in session and session['user_type'] == 'client':
            client = Client.query.filter_by(username=session['username']).first()
            if client:
                product = Product.query.get(product_id)
                if product:
                    # Check if the product is booked by the client
                    booking = Booking.query.filter_by(client_id=client.id, product_id=product.id).first()
                    if booking:
                        # Unbook the product
                        db.session.delete(booking)
                        db.session.commit()
                        flash('Product unbooked successfully!', 'success')
                    else:
                        flash('You have not booked this product.', 'warning')
        return redirect(url_for('client_dashboard'))
################################################################################
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

    @app.route('/supplier/dashboard', methods=['GET', 'POST'])
    def supplier_dashboard():
        if 'user_type' in session and session['user_type'] == 'supplier':
            username = session.get('username')
            user_type = session.get('user_type')

            # Get the list of products for the current supplier
            products = get_products_for_supplier()

            # Get the booked products for the supplier
            booked_products = get_booked_products_for_supplier()

            return render_template('supplier_dashboard.html', username=username, user_type=user_type, products=products, booked_products=booked_products)

        return render_template('supplier_login.html')
################
# Helper function to get booked products for the current supplier
    def get_booked_products_for_supplier():
        if 'user_type' in session and session['user_type'] == 'supplier':
            supplier = Supplier.query.filter_by(username=session['username']).first()
            if supplier:
                # Retrieve all booked products associated with the supplier
                booked_products = Product.query.join(Booking).filter(Booking.product.has(supplier_id=supplier.id)).all()
                return booked_products
        return []
###########33
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
    @app.route('/get_product_suggestions', methods=['GET'])
    def get_product_suggestions():
        query = request.args.get('query', '')
        # Fetch product suggestions based on the query (you can modify this logic)
        suggestions = get_product_suggestions_from_database(query)
        return jsonify(suggestions)

    # Function to fetch product suggestions from the database (modify as needed)
    def get_product_suggestions_from_database(query):
        suggestions = Product.query.filter(
            (Product.name.ilike(f'%{query}%')) | (Product.category.ilike(f'%{query}%'))
        ).limit(5).distinct().all()
        return [suggestion.name for suggestion in suggestions]
# views.py

# ... (existing code)

    @app.route('/manager/manage_products', methods=['GET', 'POST'])
    def manage_products():
        if 'user_type' in session and session['user_type'] == 'manager':
            if request.method == 'POST':
                print("manage products POST method")
                # Handle the form submission to block/unblock products
                product_id = request.form.get('product_id')
                block_status = request.form.get('block_status')

                product = Product.query.get(product_id)
                if product:
                    product.blocked = (block_status == 'block')
                    db.session.commit()

            # Retrieve all products for display in the management interface
            products = Product.query.all()
            return render_template('manage_products.html', products=products)

        return render_template('manager_login.html')
# Add routes to view clients, suppliers, and products
    @app.route('/view_clients')
    def view_clients():
        if 'user_type' in session and session['user_type'] == 'manager':
            clients = Client.query.all()
            return render_template('view_clients.html', clients=clients)
        return render_template('manager_login.html')  # Redirect to login if not a manager

    @app.route('/view_suppliers')
    def view_suppliers():
        if 'user_type' in session and session['user_type'] == 'manager':
            suppliers = Supplier.query.all()
            return render_template('view_suppliers.html', suppliers=suppliers)
        return render_template('manager_login.html')  # Redirect to login if not a manager

    @app.route('/view_products')
    def view_products():
        if 'user_type' in session and session['user_type'] == 'manager':
            products = Product.query.all()
            return render_template('view_products.html', products=products)
        return render_template('manager_login.html')  # Redirect to login if not a manager
