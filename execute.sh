#!/bin/bash

# Set the project directory
project_directory="/home/subashchandrabose/Documents/Python/luggage/"

# Check if the templates directory exists
if [ -d "$project_directory/templates" ]; then
    # Create the client_login.html file
    cat <<EOL > "$project_directory/templates/client_login.html"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Client Login</title>
    <!-- Add any additional styling or meta tags here -->
</head>
<body>

<h2>Client Login</h2>

<form action="{{ url_for('client_login') }}" method="post">
    <label for="clientUsername">Username:</label>
    <input type="text" id="clientUsername" name="clientUsername" required>

    <label for="clientPassword">Password:</label>
    <input type="password" id="clientPassword" name="clientPassword" required>

    <button type="submit">Login</button>
</form>

<!-- Add any additional content or links here -->

</body>
</html>
EOL
    cat <<EOL > "$project_directory/templates/supplier_login.html"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Supplier Login</title>
    <!-- Add any additional styling or meta tags here -->
</head>
<body>

<h2>Supplier Login</h2>

<form action="{{ url_for('supplier_login') }}" method="post">
    <label for="supplierUsername">Username:</label>
    <input type="text" id="supplierUsername" name="supplierUsername" required>

    <label for="supplierPassword">Password:</label>
    <input type="password" id="supplierPassword" name="supplierPassword" required>

    <button type="submit">Login</button>
</form>

<!-- Add any additional content or links here -->

</body>
</html>
EOL

    # Create manager_login.html
    cat <<EOL > "$project_directory/templates/manager_login.html"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manager Login</title>
    <!-- Add any additional styling or meta tags here -->
</head>
<body>

<h2>Manager Login</h2>

<form action="{{ url_for('manager_login') }}" method="post">
    <label for="managerUsername">Username:</label>
    <input type="text" id="managerUsername" name="managerUsername" required>

    <label for="managerPassword">Password:</label>
    <input type="password" id="managerPassword" name="managerPassword" required>

    <button type="submit">Login</button>
</form>

<!-- Add any additional content or links here -->

</body>
</html>
EOL
 cat <<EOL > "$project_directory/templates/client_register.html"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Client Registration</title>
    <!-- Add any additional styling or meta tags here -->
</head>
<body>

<h2>Client Registration</h2>

<form action="{{ url_for('client_register') }}" method="post">
    <label for="clientUsername">Username:</label>
    <input type="text" id="clientUsername" name="clientUsername" required>

    <label for="clientPassword">Password:</label>
    <input type="password" id="clientPassword" name="clientPassword" required>

    <button type="submit">Register</button>
</form>

<!-- Add any additional content or links here -->

</body>
</html>
EOL

    # Create supplier_register.html
    cat <<EOL > "$project_directory/templates/supplier_register.html"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Supplier Registration</title>
    <!-- Add any additional styling or meta tags here -->
</head>
<body>

<h2>Supplier Registration</h2>

<form action="{{ url_for('supplier_register') }}" method="post">
    <label for="supplierUsername">Username:</label>
    <input type="text" id="supplierUsername" name="supplierUsername" required>

    <label for="supplierPassword">Password:</label>
    <input type="password" id="supplierPassword" name="supplierPassword" required>

    <button type="submit">Register</button>
</form>

<!-- Add any additional content or links here -->

</body>
</html>
EOL

    # Create manager_register.html
    cat <<EOL > "$project_directory/templates/manager_register.html"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manager Registration</title>
    <!-- Add any additional styling or meta tags here -->
</head>
<body>

<h2>Manager Registration</h2>

<form action="{{ url_for('manager_register') }}" method="post">
    <label for="managerUsername">Username:</label>
    <input type="text" id="managerUsername" name="managerUsername" required>

    <label for="managerPassword">Password:</label>
    <input type="password" id="managerPassword" name="managerPassword" required>

    <button type="submit">Register</button>
</form>

<!-- Add any additional content or links here -->

</body>
</html>
EOL

    echo "HTML files created successfully!"
else
    echo "Error: templates directory not found. Please make sure the 'templates' directory exists in $project_directory."
fi