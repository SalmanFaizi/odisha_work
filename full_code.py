# import os
# import shutil
# import time
# from ftplib import FTP
# import json
# import mysql.connector
# from mysql.connector import Error
# from concurrent.futures import ThreadPoolExecutor

# # Read FTP configuration from JSON file
# def load_ftp_config(config_file):
#     with open(config_file, 'r') as file:
#         return json.load(file)

# # Connect to FTP server
# def connect_to_ftp_server(host, username, password):
#     try:
#         ftp = FTP()
#         ftp.connect(host, 2121, timeout=10)  # Adjust port as necessary
#         ftp.login(user=username, passwd=password)
#         print(f'connected succussfully to the {host}')
#         return ftp
#     except Exception as e:
#         print(f"Failed to connect to FTP server {host}: {e}")
#         return None

# # Download files from FTP server
# def download_files(ftp, download_dir):
#     try:
#         files = ftp.nlst()
#         files=files[:-1]
#         clean_directory(download_dir)
#         for file_name in files:
#             local_path = os.path.join(download_dir, file_name)
#             with open(local_path, 'wb') as local_file:
#                 ftp.retrbinary(f"RETR {file_name}", local_file.write)
#         return os.listdir(download_dir)  # Return list of downloaded files
#         print("downloading files sucusfull")
#     except Exception as e:
#         print(f"Error downloading files: {e}")
#         return []

# # Parse text files
# def parse_file(file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#     data = {}
#     for line in lines:
#         if line.startswith("name="):
#             data["name"] = line.split("=", 1)[1].strip()
#         elif line.startswith("phone="):
#             data["phone"] = line.split("=", 1)[1].strip()
#     return data

# # Insert data into MySQL
# def insert_data_into_database(data):
#     try:
#         connection = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="Password",
#             database="ftp"
#         )
#         if connection.is_connected():
#             cursor = connection.cursor()
#             sql_query = "INSERT INTO data (name, phone) VALUES (%s, %s)"
#             cursor.execute(sql_query, (data["name"], data["phone"]))
#             connection.commit()
#             print("Data inserted succussfully",(data["name"], data["phone"]))
#     except Error as e:
#         print(f"Database error: {e}")
#     finally:
#         if connection.is_connected():
#             connection.close()

# # Process FTP server
# def process_ftp_server(ftp_config):
#     print(f"Processing server: {ftp_config['host']}")
#     ftp = connect_to_ftp_server(ftp_config['host'], ftp_config['username'], ftp_config['password'])
#     if ftp:
#         download_dir = f"download_{ftp_config['host']}"  # Unique directory for each server
#         files = download_files(ftp, download_dir)
#         for file_name in files:
#             file_path = os.path.join(download_dir, file_name)
#             data = parse_file(file_path)
#             if "name" in data and "phone" in data:
#                 insert_data_into_database(data)
#         ftp.quit()
#     # else:
#     #     print("An error occured after connecting..")

# # Clean directory
# def clean_directory(directory):
#     if os.path.exists(directory):
#         shutil.rmtree(directory)
#     os.makedirs(directory)

# # Main function
# def main():
#     ftp_configs = load_ftp_config('ftp_config.json')
#     with ThreadPoolExecutor(max_workers=3) as executor:
#         executor.map(process_ftp_server, ftp_configs)
#         # time.sleep(1000)

# if __name__ == "__main__":
#     main()



import os
import shutil
import time
from ftplib import FTP
import json
import mysql.connector
from mysql.connector import Error
from concurrent.futures import ThreadPoolExecutor

# Read FTP configuration from JSON file
def load_ftp_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

# Connect to FTP server
def connect_to_ftp_server(host, username, password):
    try:
        ftp = FTP()
        ftp.connect(host, 2121, timeout=10)  # Adjust port if necessary
        ftp.login(user=username, passwd=password)
        print(f"Connected successfully to the FTP server: {host}")
        return ftp
    except Exception as e:
        print(f"Failed to connect to FTP server {host}: {e}")
        return None

# Download last file from FTP server
def download_last_file(ftp, download_dir):
    try:
        files = ftp.nlst()
        files = sorted(files)  # Sort files to ensure order
        if files:
            last_file = files[-1]
            clean_directory(download_dir)
            local_path = os.path.join(download_dir, last_file)
            with open(local_path, 'wb') as local_file:
                ftp.retrbinary(f"RETR {last_file}", local_file.write)
            print(f"Downloaded: {last_file} from {ftp.host}")
            return local_path
        else:
            print(f"No files found on FTP server: {ftp.host}")
            return None
    except Exception as e:
        print(f"Error downloading file from FTP server: {ftp.host}: {e}")
        return None

# Parse text files
def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data = {}
    for line in lines:
        if line.startswith("name="):
            data["name"] = line.split("=", 1)[1].strip()
        elif line.startswith("phone="):
            data["phone"] = line.split("=", 1)[1].strip()
    return data

# Insert data into MySQL
def insert_data_into_database(data):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password",
            database="ftp"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            sql_query = "INSERT INTO data (name, phone) VALUES (%s, %s)"
            cursor.execute(sql_query, (data["name"], data["phone"]))
            connection.commit()
            print(f"Data inserted successfully: {data}")
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Process FTP server
def process_ftp_server(ftp_config):
    print(f"Processing server: {ftp_config['host']}")
    ftp = connect_to_ftp_server(ftp_config['host'], ftp_config['username'], ftp_config['password'])
    if ftp:
        download_dir = f"download_{ftp_config['host']}"  # Unique directory for each server
        file_path = download_last_file(ftp, download_dir)
        if file_path:
            data = parse_file(file_path)
            if "name" in data and "phone" in data:
                insert_data_into_database(data)
        ftp.quit()
    else:
        print(f"Skipping server: {ftp_config['host']} due to connection issues.")

# Clean directory
def clean_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

# Main function
def main():
    ftp_configs = load_ftp_config('ftp_config.json')
    while True:
        print("Starting FTP processing...")
        with ThreadPoolExecutor(max_workers=len(ftp_configs)) as executor:
            executor.map(process_ftp_server, ftp_configs)
        print("FTP processing completed. Waiting for 30 seconds...")
        time.sleep(30)

if __name__ == "__main__":
    main()
