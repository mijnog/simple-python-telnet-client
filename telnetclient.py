import socket
import sys
import signal

def signal_handler():
    """
    Signal handler for graceful exit when receiving a SIGINT (Ctrl+C).
    This function will close the global socket 's' and exit the program.
    """
    print("\nExiting...")
    s.close()  # Ensure the socket is closed before exiting (s is a global variable)
    sys.exit(0)

def main():
    # Check for command line arguments
    if len(sys.argv) < 2:
        print("Usage: python telnet_client.py <ip_address> [port]")
        sys.exit(1)

    ip_address = sys.argv[1]  # Get the IP address from the arguments
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 23  # Default to port 23 if not provided

    global s  # Declare 's' as global to use it in both the main function and the signal handler
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new TCP socket

    # Set up signal handler for graceful exit
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler())

    try:
        s.connect((ip_address, port))  # Attempt to connect to the specified IP address and port
        print(f"Connected to {ip_address} on port {port}")

        while True:
            command = input("Enter command (or 'exit' to quit): ")
            if command.strip().lower() == 'exit':  # Check if the user wants to exit
                print("Exiting...")
                break  # Exit the loop

            s.sendall(command.encode('utf-8') + b'\n')  # Send the command to the server
            response = s.recv(4096)  # Receive the response from the server
            print(response.decode('utf-8'))  # Decode and print the response

    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any exceptions that occur during the connection

    finally:
        s.close()  # Ensure the socket is closed when done

if __name__ == "__main__":
    main()  # Start the main function when the script is executed
