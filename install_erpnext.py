import os
import subprocess
import sys

def run_command(command, sudo=False):
    """Run a shell command, optionally with sudo."""
    if sudo:
        command = f"sudo {command}"
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=True)
    return result

def install_required_packages():
    """Install all the required packages."""
    packages = [
        "git", 
        "python3-dev", "python3.10-dev", "python3-setuptools", "python3-pip", "python3-distutils", 
        "python3.10-venv", 
        "software-properties-common", 
        "mariadb-server", "mariadb-client", 
        "redis-server", 
        "xvfb", "libfontconfig", "wkhtmltopdf", 
        "libmysqlclient-dev", 
        "curl", "npm"
    ]
    
    for package in packages:
        run_command(f"apt-get install -y {package}", sudo=True)

def configure_mysql(mysql_root_password):
    """Configure MySQL server."""
    # Run mysql_secure_installation with the root password
    mysql_secure_command = f"mysql_secure_installation <<EOF\n{mysql_root_password}\nY\nY\nN\nY\nY\nEOF"
    run_command(mysql_secure_command, sudo=True)
    
    # Modify my.cnf to set utf8mb4 as character set
    my_cnf_file = "/etc/mysql/my.cnf"
    with open(my_cnf_file, "a") as f:
        f.write("\n[mysqld]\ncharacter-set-client-handshake = FALSE\ncharacter-set-server = utf8mb4\ncollation-server = utf8mb4_unicode_ci\n")
        f.write("\n[mysql]\ndefault-character-set = utf8mb4\n")
    
    run_command("sudo service mysql restart", sudo=True)

def install_node_and_yarn():
    """Install Node, NPM, and Yarn."""
    run_command("curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash", sudo=True)
    run_command("source ~/.profile", sudo=True)
    run_command("nvm install 18", sudo=True)
    run_command("npm install -g yarn", sudo=True)

def install_frappe_bench():
    """Install Frappe Bench."""
    run_command("sudo pip3 install frappe-bench", sudo=True)

def setup_bench(site_name):
    """Setup the bench and create a new site."""
    run_command("bench init --frappe-branch version-15 frappe-bench", sudo=True)
    run_command(f"cd frappe-bench && bench new-site {site_name}", sudo=True)

def install_erpnext_and_apps(site_name):
    """Install ERPNext and other apps."""
    run_command(f"cd frappe-bench && bench get-app --branch version-15 erpnext", sudo=True)
    run_command(f"cd frappe-bench && bench --site {site_name} install-app erpnext", sudo=True)

def setup_production():
    """Set up production server with NGINX and Supervisor."""
    run_command("bench setup production frappe", sudo=True)
    run_command("bench setup nginx", sudo=True)
    run_command("sudo service nginx reload", sudo=True)

def enable_scheduler(site_name):
    """Enable scheduler and disable maintenance mode."""
    run_command(f"bench --site {site_name} enable-scheduler", sudo=True)
    run_command(f"bench --site {site_name} set-maintenance-mode off", sudo=True)

def configure_ssl(site_name):
    """Set up SSL and NGINX for custom domain."""
    run_command(f"cd /home/frappe/frappe-bench && bench config dns_multitenant on", sudo=True)
    run_command(f"bench setup add-domain subdomain.yourdomain.com --site {site_name}", sudo=True)
    run_command("sudo snap install core", sudo=True)
    run_command("sudo snap refresh core", sudo=True)
    run_command("sudo snap install --classic certbot", sudo=True)
    run_command("sudo ln -s /snap/bin/certbot /usr/bin/certbot", sudo=True)
    run_command("sudo certbot --nginx", sudo=True)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 install_erpnext.py <site-name> <mysql-root-password>")
        sys.exit(1)
    
    site_name = sys.argv[1]
    mysql_root_password = sys.argv[2]
    
    print(f"Starting ERPNext setup for site: {site_name}")
    
    # Install dependencies
    install_required_packages()
    
    # Configure MySQL
    configure_mysql(mysql_root_password)
    
    # Install Node, NPM, Yarn
    install_node_and_yarn()
    
    # Install Frappe Bench
    install_frappe_bench()
    
    # Setup bench and create a new site
    setup_bench(site_name)
    
    # Install ERPNext
    install_erpnext_and_apps(site_name)
    
    # Setup production server
    setup_production()
    
    # Enable scheduler and disable maintenance mode
    enable_scheduler(site_name)
    
    # Optionally configure SSL (requires DNS setup)
    configure_ssl(site_name)
    
    print("ERPNext installation complete! Visit your site at http://<server-ip> or https://<subdomain>")

if __name__ == "__main__":
    main()


# For running the project we need to write theis with arguments like - 
# python3 install_erpnext.py <site-name> <mysql-root-password>

