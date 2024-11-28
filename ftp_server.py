from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Set up user credentials
authorizer = DummyAuthorizer()
authorizer.add_user("user1", "password1", r"D:\Salman_Kotai_Electronics\ftp-files", perm="elradfmw")  # Chan                                                                                                             ge username, password, and directory as needed
authorizer.add_anonymous(r"D:\Salman_Kotai_Electronics\ftp-files", perm="elradfmw")  # Allow anonymous acc                                                                                                             ess (optional)

# Create FTP handler and assign the authorizer
handler = FTPHandler
handler.authorizer = authorizer

# Set up the FTP server
server = FTPServer(("0.0.0.0", 2121), handler)  # Use port 21 for FTP
server.serve_forever()
