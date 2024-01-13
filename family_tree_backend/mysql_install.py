import subprocess

# Update package list
update_command = "sudo apt-get update"
subprocess.run(update_command, shell=True)

# Install required packages
install_command = "sudo apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config"
subprocess.run(install_command, shell=True)

# Install MySQL client for Python
pip_install_command = "pip install mysqlclient"
subprocess.run(pip_install_command, shell=True)
i
