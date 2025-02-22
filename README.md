# Chatroom Application

This is a simple multi-client chatroom application built using Python with `socket` and `threading` modules. It allows multiple clients to connect to a server and exchange messages in real time through a command-line or GUI interface.

## Features
- Multi-client support
- Real-time message broadcasting
- Simple GUI using Tkinter
- Graceful handling of client disconnections

## Requirements
Ensure you have Python 3 installed on your system.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/duyle1062/chatroomAPP.git
   cd chatroomAPP
   ```
2. Install dependencies (if any are required, such as Tkinter for GUI):
   ```sh
   pip install tk
   ```

## Usage

### Start the Server
Run the server script with:
```sh
python server.py <host> -p <port>
```
Example:
```sh
python server.py 127.0.0.1 -p 1060
```

### Start the Client
Run the client script with:
```sh
python client.py <server_ip> -p <port>
```
Example:
```sh
python client.py 127.0.0.1 -p 1060
```

## Troubleshooting
- **Client cannot connect to the server?**
  - Check if the server is running.
  - Ensure the correct IP and port are being used.
  - Open the port in Windows Firewall:
    ```sh
    netsh advfirewall firewall add rule name="Chatroom" dir=in action=allow protocol=TCP localport=1060
    ```

- **Messages not being received?**
  - Ensure the server’s `broadcast` function is working correctly.
  - Check for any network connection issues.
  - Restart the client and server.

## Future Improvements
- Implement user authentication
- Support encrypted communication
- Improve UI design

## License
This project is licensed under the MIT License.

## Author
Developed by **duyle1062**

