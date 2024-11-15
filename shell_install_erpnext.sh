#!/bin/bash

# This script installs ERPNext and Frappe Bench on Ubuntu 22.04 (or later)
# Usage: ./install_erpnext.sh <site-name> <mysql-root-password>

# Check if the correct number of arguments is provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <site-name> <mysql-root-password>"
    exit 1
fi

SITE_NAME=$1
MYSQL_ROOT_PASSWORD=$2

# Function to run commands with sudo
run_command() {
    echo "Running: $1"
    sudo $1
}

# Install required packages
install_required_packages() {
    echo "Installing required packages..."
    sudo apt-get update -y
    sudo apt-get upgrade -y
    sudo apt-get install -y git python3-dev python3.10-dev python3-setuptools python3-pip python3-distutils python3.10-venv software-properties-common mariadb-server mariadb-client redis-server xvfb libfontconfig wkhtmltopdf libmysqlclient-dev curl npm
}

# Configure MySQL
configure_mysql() {
    echo "Configuring MySQL..."
    
    # Run mysql_secure_installation with the root password
    mysql_secure_command="mysql_secure_installation <<EOF
$MYSQL_ROOT_PASSWORD
Y
Y
N
Y
Y
EOF"
    eval "$mysql_secure_command"
    
    # Modify my.cnf to set utf8mb4 as character set
    echo -e "\n[mysqld]\ncharacter-set-client-handshake = FALSE\ncharacter-set-server = utf8mb4\ncollation-server = utf8mb4_unicode_ci\n" | sudo tee -a /etc/mysql/my.cnf
    echo -e "\n[mysql]\ndefault-character-set = utf8mb4\n" | sudo tee -a /etc/mysql/my.cnf

    sudo service mysql restart
}

# Install Node.js, NPM, and Yarn
install_node_and_yarn() {
    echo "Installing Node.js, NPM, and Yarn..."
    curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
    source ~/.profile
    nvm install 18
    npm install -g yarn
}

# Install Frappe Bench
install_frappe_bench() {
    echo "Installing Frappe Bench..."
    sudo pip3 install frappe-bench
}

# Setup Bench and create a new site
setup_bench() {
    echo "Setting up Bench and creating the site..."
    bench init --frappe-branch version-15 frappe-bench
    cd frappe-bench
    bench new-site $SITE_NAME
}

# Install ERPNext and other apps
install_erpnext_and_apps() {
    echo "Installing ERPNext and other apps..."
    cd frappe-bench
    bench get-app --branch version-15 erpnext
    bench --site $SITE_NAME install-app erpnext
}

# Setup production environment
setup_production() {
    echo "Setting up production environment..."
    bench setup production frappe
    bench setup nginx
    sudo service nginx reload
}

# Enable scheduler and disable maintenance mode
enable_scheduler() {
    echo "Enabling scheduler and disabling maintenance mode..."
    bench --site $SITE_NAME enable-scheduler
    bench --site $SITE_NAME set-maintenance-mode off
}

# Configure SSL (optional)
configure_ssl() {
    echo "Configuring SSL (optional)..."
    # Ensure you have your DNS setup correctly
    bench config dns_multitenant on
    bench setup add-domain subdomain.yourdomain.com --site $SITE_NAME
    sudo snap install core
    sudo snap refresh core
    sudo snap install --classic certbot
    sudo ln -s /snap/bin/certbot /usr/bin/certbot
    sudo certbot --nginx
}

# Main function
main() {
    # Install dependencies
    install_required_packages
    
    # Configure MySQL
    configure_mysql
    
    # Install Node.js, NPM, Yarn
    install_node_and_yarn
    
    # Install Frappe Bench
    install_frappe_bench
    
    # Setup Bench and create the site
    setup_bench
    
    # Install ERPNext and other apps
    install_erpnext_and_apps
    
    # Setup production environment
    setup_production
    
    # Enable scheduler and disable maintenance mode
    enable_scheduler
    
    # Optionally configure SSL (requires custom domain setup)
    configure_ssl
    
    echo "ERPNext installation complete! Visit your site at http://<server-ip> or https://<subdomain>"
}

# Run the main function
main
