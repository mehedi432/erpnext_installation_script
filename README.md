# ERPNext Installation Script

This Python script automates the installation of **ERPNext** and **Frappe** (version 15) on an Ubuntu server. The script accepts two arguments:
1. **Site name**: The name of the ERPNext site you want to create (e.g., `myerp.local`).
2. **MySQL root password**: The password for your MySQL root user.

The script automates the following tasks:
- Installs required packages (MySQL, Redis, Node.js, Yarn, etc.).
- Configures MySQL with the provided root password.
- Installs **Frappe Bench**.
- Creates a new site and installs ERPNext.
- Sets up a production environment with NGINX and Supervisor.
- Configures SSL for the site using **Certbot** (if you have a custom domain set up).

---

## Prerequisites

- **Operating System**: Ubuntu 22.04 LTS or later
- **Minimum Recommended Hardware**:
  - 2 CPU cores
  - 4 GB RAM
  - 20 GB Disk Space
- **Root Shell Access** to the server via SSH
- **MySQL root password**
- **Custom Domain (optional)** for SSL configuration (optional)

---

## How to Run the Python Script

### 1. Save the Script

Save the provided Python script as `install_erpnext.py` on your server.

### 2. Install Python Dependencies

Before running the script, ensure you have Python 3 and `pip` installed. If not, install them by running the following:

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip


You also need sudo privileges for some steps (for installing system-wide packages).
3. Run the Script

You need to pass two arguments to the script:

    The site name (e.g., myerp.local)
    The MySQL root password (to configure MySQL securely)

Use the following command to run the script:

python3 install_erpnext.py <site-name> <mysql-root-password>

For example:

python3 install_erpnext.py myerp.local your_mysql_root_password

Replace:

    myerp.local with the site name you wish to use for your ERPNext instance.
    your_mysql_root_password with the root password for your MySQL server.

What the Script Does
1. Installs Required Packages

The script installs all the necessary dependencies such as:

    Git
    Python 3 and related dependencies
    MariaDB (MySQL server)
    Redis server
    Node.js, NPM, Yarn
    Other essential packages like xvfb, libfontconfig, and wkhtmltopdf for PDF generation.

2. Configures MySQL

The script runs the mysql_secure_installation tool using the MySQL root password passed as an argument and updates the MySQL configuration file to support utf8mb4 character set.
3. Installs Node.js and Yarn

Node.js (version 18) and Yarn are installed via nvm (Node Version Manager).
4. Installs Frappe Bench

The script installs Frappe Bench (a tool for managing ERPNext) and initializes a new bench with Frappe v15.
5. Creates a New Site

A new ERPNext site is created using the provided site name.
6. Installs ERPNext

ERPNext is installed on the newly created site, and all required apps (e.g., payments, HRMS) are also installed.
7. Sets Up the Production Server

The script sets up a production environment by configuring NGINX, Supervisor, and enabling the scheduler for ERPNext. It also disables maintenance mode to make the site live.
8. SSL Configuration (Optional)

If you have a custom domain, the script can help you set up SSL certificates using Certbot and configure NGINX to serve the site over HTTPS.
Additional Notes
Security Consideration:

Passing the MySQL root password as a command-line argument may expose the password in the shell’s history or process list (especially if you use tools like ps).

    Secure Alternative: To improve security, you could read the MySQL password from an environment variable instead of passing it as a command-line argument.

    Environment Variable Option: You can modify the script to read the MySQL root password from an environment variable like this:

export MYSQL_ROOT_PASSWORD=your_mysql_root_password
python3 install_erpnext.py myerp.local $MYSQL_ROOT_PASSWORD

Custom Domain and SSL:

For SSL configuration, you must:

    Add an A record to your domain's DNS settings that points to the server IP address.
    Replace subdomain.yourdomain.com in the script with your actual domain/subdomain.

Firewall Considerations:

Make sure the necessary ports are open in your server firewall to allow access to ERPNext:

sudo ufw allow 22,25,143,80,443,3306,3022,8000/tcp
sudo ufw enable

Example Output

When you run the script, you will see output similar to the following:

Starting ERPNext setup for site: myerp.local
Running: sudo apt-get install -y git
...
Running: sudo service mysql restart
Running: cd frappe-bench && bench new-site myerp.local
...
Running: sudo certbot --nginx
ERPNext installation complete! Visit your site at http://<server-ip> or https://<subdomain>

Troubleshooting

    Permission Denied: Ensure you're running the script with appropriate permissions (sudo) for commands that require elevated privileges.

    Missing Dependencies: If the script fails to install any package, you may need to manually install them or check your internet connection.





