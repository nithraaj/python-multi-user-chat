# Multi user chat app

This project is a group chat application that allows the users to chat with
multiple users via a graphical user interface. It consists of two
components - the server and the client.

## Usage

Start the server  
```python3 chat_server.py <ip-address> <port>```

Start the client  
```python3 chat_client_gui.py```

## Note

This code was tested on Ubuntu, and should work on any linux OS. This code may not work on Windows as _select_ library is not supported in Windows.