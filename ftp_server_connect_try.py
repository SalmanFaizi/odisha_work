import os
import shutil
import time
from ftplib import FTP
import socket
import mysql.connector
from mysql.connector import Error

def connect_to_ftp_server(host, username, password):
    try:
        ftp = FTP()
        print(f"Attempting to connect to {host}...")
        ftp.connect(host, 2121, timeout=10)  # Add timeout for clarity
        ftp.login(user=username, passwd=password)
        print(f"Connected to FTP server: {host}")
        return ftp
    except socket.timeout:
        print("Connection timed out. Server may be unreachable.")
    except socket.gaierror:
        print("Invalid host address.")
    except Exception as e:
        print(f"Failed to connect to FTP server: {e}")
    return None

def list_files(ftp):
    try:
        files = ftp.nlst()  # Get the list of files
        print("Files on the server:")
        print("\n".join(files))
        return files
    except Exception as e:
        print(f"Failed to list files: {e}")
        return []

def clean_directory(directory):
    """Remove all files from the directory."""
    if os.path.exists(directory):
        print(f"Cleaning directory: {directory}")
        shutil.rmtree(directory)  # Remove the entire directory
    os.makedirs(directory)  # Recreate the directory

def download_files(ftp, files, download_dir):
    clean_directory(download_dir)  # Clean the directory before downloading
    for file_name in files:
        local_path = os.path.join(download_dir, file_name)
        print(f"Downloading {file_name} to {local_path}...")
        try:
            with open(local_path, 'wb') as local_file:
                ftp.retrbinary(f"RETR {file_name}", local_file.write)
            print(f"Downloaded: {file_name}")
        except Exception as e:
            print(f"Failed to download {file_name}: {e}")

def parse_file(file_path):
    """Parse the file to extract name and phone."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data = {}
    for line in lines:
        if line.startswith("name="):
            data["name"] = line.split("=", 1)[1].strip()
        elif line.startswith("phone="):
            data["phone"] = line.split("=", 1)[1].strip()
    return data

def insert_data_into_database(data):
    """Insert data into MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",    # Replace with your MySQL host
            user="root",         # Replace with your MySQL username
            password="Password", # Replace with your MySQL password
            database="ftp"   # Replace with your database name
        )
        if connection.is_connected():
            cursor = connection.cursor()
            sql_query = "INSERT INTO data (name, phone) VALUES (%s, %s)"
            cursor.execute(sql_query, (data["name"], data["phone"]))
            connection.commit()
            print(f"Inserted into database: {data}")
    except Error as e:
        print(f"Failed to insert data into database: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def process_downloaded_files(folder_path):
    """Process the downloaded files to extract and push data."""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        print(f"Processing file: {file_path}")
        data = parse_file(file_path)
        print(f"Parsed data: {data}")
        if "name" in data and "phone" in data:
            insert_data_into_database(data)
        else:
            print("Invalid data format. Skipping file.")

def main():
    # FTP server details
    host = "192.168.1.10"
    username = "user"
    password = "password"
    download_dir = "download"  # Directory to save downloaded files

    while True:
        ftp = connect_to_ftp_server(host, username, password)
        if ftp is not None:
            files_from_server = list_files(ftp)
            if files_from_server:
                # Get the last 5 files
                last_5_files = files_from_server[-1:]
                print(f"Last 5 files to download: {last_5_files}")
                download_files(ftp, last_5_files, download_dir)
            
            # Close the connection
            ftp.quit()
            print("Disconnected from FTP server.")
        
        # Process downloaded files and push to database
        process_downloaded_files(download_dir)

        # Wait for 1 minute before repeating
        print("Waiting for 1 minute before the next operation...")
        time.sleep(60)

if __name__ == "__main__":
    main()
