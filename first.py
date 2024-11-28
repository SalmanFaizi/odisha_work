from ftplib import FTP

# Connect to the server using anonymous login
ftp = FTP('192.168.1.6')
ftp.login()  # No username/password needed
print("Connected as anonymous user.")
ftp.quit()
