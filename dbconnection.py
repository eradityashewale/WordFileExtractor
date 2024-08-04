import configparser
import pyodbc

# Read the existing configuration from the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Get SQL Server credentials from the configuration
server = config['SQLServer']['server']
database = config['SQLServer']['database']
driver = config['SQLServer']['driver']

# Check if SQL Server authentication is used
if config.has_option('SQLServer', 'username') and config.has_option('SQLServer', 'password'):
    username = config['SQLServer']['username']
    password = config['SQLServer']['password']
    # Create a connection string with SQL Server authentication
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;'
else:
    # Create a connection string with Windows authentication
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

def create_connection():
    return pyodbc.connect(conn_str)