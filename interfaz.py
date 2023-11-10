import PySimpleGUI as sg
import paramiko
import os
import ast

# Function to connect to Raspberry Pi
def connect_to_raspberry(ip_address, username, password):
    try:
        # Create an SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the Raspberry Pi
        client.connect(ip_address, username=username, password=password)
        print(f"Connected to {ip_address}")

        return client
    
    except paramiko.AuthenticationException:
        print(f"Failed to connect to {ip_address} (Authentication failed)")
    except paramiko.SSHException as e:
        print(f"Failed to connect to {ip_address} ({str(e)})")
    print("Connecting to Raspberry Pi...")

# Function to check if the application in computer B is running
def is_application_running(client, application_name):

    # Check if the application is running
    command = f"pgrep -f facedetection.py"
    stdin, stdout, stderr = client.exec_command(command)
    process_list = stdout.read().decode().splitlines()
    
    if process_list:
        print(f"The application '{application_name}' is running on Raspberry.")
        return True, process_list
    else:
        print(f"The application '{application_name}' is not running on Raspberry.")
        return False, process_list

# Function to disconnect from Raspberry Pi
def disconnect_from_raspberry(client):
    _, stdout, _ = client.exec_command('hostname')
    hostname = stdout.read()
    # Close the SSH connection
    print("Disconnecting from Raspberry Pi...")
    client.close()
    print(f"Connection closed to {hostname}")

# Function to run the application in computer B
def run_application(client, application_name):
    print("Running app on Raspberry")
    
    stdin, stdout, stderr = client.exec_command("cd /usr/bin/ ;python3 facedetection.py")
    
# Function to stop the application in computer B
def stop_application(client, application_name, process_list):
    print("Stopping app on Raspberry")

    # Execute command to stop the application
    command = f"kill "+process_list
    client.exec_command(command)

    print(f"The application '{application_name}' has been stopped on computer B.")

# Function to import folder
def import_data(client):
    print("Importing data...")
    try:
        # Create an SCP client
        scp_client = client.open_sftp()
        try:
            os.remove('C:/Users/emabr/emotions_detected.csv')
            scp_client.get('/usr/bin/emotions_detected.csv','C:/Users/emabr/emotions_detected.csv')
        except:
        # Copy each file from the source folder to the destination folder on computer A
            scp_client.get('/usr/bin/emotions_detected.csv','C:/Users/emabr/emotions_detected.csv')

        # Close the SCP client and SSH connection
        scp_client.close()

        print("Files copied successfully.")
    except Exception as e:
        print("An error occurred:", str(e))


# Function to verify connection
def verify_connection(client):
    if client is None:
        return False
    return True  # Replace with your verification logic

# Create the GUI layout
layout = [
    [sg.Button("Connect", size=(15, 3),pad=((100, 100), (10, 0)),font=("Helvetica", 20), key="-CONNECT-",button_color='red on white')],
    [sg.Button("Run App", key="-RUN_APP-",button_color='red on white',size=(15, 3),font=("Helvetica", 20), pad=((100, 100), (10, 0)))],
    [sg.Button("Request Data", size=(15, 3),pad=((100, 100), (20, 0)),font=("Helvetica", 20),button_color='black on white',key="-REQUEST_DATA-")],
    [sg.Text("Connection Status: ", font=("Helvetica", 12)), sg.Text("Disconnected", key="-STATUS-", font=("Helvetica", 12), background_color="red")],
    [sg.Text("Application Running", font=("Helvetica", 12)), sg.Text("Application Not Running", key="-APP_STATUS-", font=("Helvetica", 12), background_color="red")],
    [sg.Image(key="-IMAGE-")]
]

# Create the window
window = sg.Window("Face Emotion Detector", layout, size=(500,500),background_color='black')

connected = False  # Initially set the connected status as False

# Usage
username = "root"  # Replace with your username on computer B
password = ""  # Replace with your password on computer B
ip_address = "192.168.0.104"  # Replace with the IP address of computer B
application_name = "facedetecion.py" # Application name to check if running


# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == "-CONNECT-":
        if connected:
            client = disconnect_from_raspberry(client)
            connected = verify_connection(client)
            window["-STATUS-"].update("Disconnected", background_color="red")
            window["-CONNECT-"].update("Connect",button_color='green')
        else:
            client = connect_to_raspberry(ip_address, username, password)
            connected = verify_connection(client)
            if connected:
                window["-STATUS-"].update("Connected", background_color="green")
                window["-CONNECT-"].update("Disconnect",button_color='red')
        
    
    elif event == "-REQUEST_DATA-":
        import_data(client)

    elif event == "-RUN_APP-":
        if connected:
            if window[event].get_text() == "Run App":
                # Call the run_application function
                run_application(client, application_name)
                window[event].update("Stop App",button_color='green on white')
            else:
                # Call the stop_application function
                stop_application(client, application_name, process_list)
                window[event].update("Run App",button_color='red on white')
        else:
            print("Not connected to Raspberry")

    # Verify connection and update the status display
    connection_status = verify_connection(client)
    if connection_status:
        window["-STATUS-"].update("Connected", background_color="green")
        connected = True
        window["-CONNECT-"].update("Disconnect",button_color='green on white')
    else:
        window["-STATUS-"].update("Disconnected", background_color="red")
        connected = False
        window["-CONNECT-"].update("Connect",button_color='red on white')

    # Update the application status
    if connection_status:
        running,knum=is_application_running(client, application_name)
        
        if running:
            window["-APP_STATUS-"].update("Application Running", background_color="green")
            try:
                process_list = knum[-1]
            except:
                process_list = ''
        else:
            window["-APP_STATUS-"].update("Application Not Running", background_color="red")


# Close the window
window.close()

