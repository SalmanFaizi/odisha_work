from ftplib import FTP
import socket

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
        print("Files on the server:")
        server_files=ftp.retrlines('LIST')
    except Exception as e:
        print(f"Failed to list files: {e}")
    return server_files

# def download_file(ftp, remote_file, local_file):
#     try:
#         with open(local_file, 'wb') as f:
#             ftp.retrbinary(f"RETR {remote_file}", f.write)
#         print(f"File downloaded: {local_file}")
#     except Exception as e:
#         print(f"Failed to download file: {e}")

# def upload_file(ftp, local_file, remote_file):
#     try:
#         with open(local_file, 'rb') as f:
#             ftp.storbinary(f"STOR {remote_file}", f)
#         print(f"File uploaded: {remote_file}")
#     except Exception as e:
#         print(f"Failed to upload file: {e}")

def main():
    # FTP server details
    host = "192.168.1.10"
    username = "user"
    password = "password"
    ftp = connect_to_ftp_server(host, username, password)
    if ftp:
        fiels_from_server=list_files(ftp)
        print(fiels_from_server)
        
        # # # Example: Download a file
        # download_file(ftp, "2024-11-25 14-28-16.txt", "local_file.txt")
        
        # # Example: Upload a file
        # upload_file(ftp, "local_upload.txt", "server_upload.txt")
        
        # Close the connection
        ftp.quit()
        print("Disconnected from FTP server.")

if __name__ == "__main__":
    main()
