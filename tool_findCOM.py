import serial.tools.list_ports


def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No serial ports found.")
        return

    print("Available serial ports:")
    for port in ports:
        print(f"{port.device} - {port.description}")

    print(" sudo chmod 777 /dev/ttyACM0 ")
    print(" sudo minicom -D /dev/ttyACM0 -b 115200 ")

if __name__ == "__main__":
    list_serial_ports()

#   pip install pyserial

##############CLI##########################

#   [System.IO.Ports.SerialPort]::GetPortNames()
#   ls /dev/tty*

##############task#####################

# // [System.IO.Ports.SerialPort]::GetPortNames()
#     {   
#         "label": "findCOM",
#         "type": "shell",
#         "command": "powershell",
#         "args": [
#             "-Command",
#             "[System.IO.Ports.SerialPort]::GetPortNames() | ForEach-Object { Write-Host $_ }"
#         ],
#         "problemMatcher": [],
#         "group": "build"
#     }