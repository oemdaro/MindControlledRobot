import socket

if __name__ == "__main__":
    # create socket and bind host
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.100', 8000))
    connection = client_socket.makefile('wb')

    try:
        pass
    except Exception as e:
        raise
    finally:
        connection.close()
        client_socket.close()
