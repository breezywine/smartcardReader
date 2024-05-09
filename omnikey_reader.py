from smartcard.System import readers
from smartcard.util import toHexString, toBytes, toASCIIString 



# ANSI escape code for color
reset_color = '\033[0m'
blue_color = "\033[34m"
cyan_color = "\033[0;36m"
green_color = '\033[92m'
red_color = '\033[91m'
yellow_color = "\033[1;33m"





# omnikey common APDU cmd
# https://www3.hidglobal.com/sites/default/files/resource_files/plt-03099_a.5_-_omnikey_sw_dev_guide_0.pdf
APDU = {
    # Reader Information A2h
    # Get A0h
    # Reader Capabilities A0h
    "get deviceID"          : "FF 70 07 6B 08 A2 06 A0 04 A0 02 81 00 00",
    "get productName"       : "FF 70 07 6B 08 A2 06 A0 04 A0 02 82 00 00",
    "get productPlatform"   : "FF 70 07 6B 08 A2 06 A0 04 A0 02 83 00 00",
    "get serialNumber"      : "FF 70 07 6B 08 A2 06 A0 04 A0 02 92 00 00",
    "get firmwareLabel"     : "FF 70 07 6B 08 A2 06 A0 04 A0 02 96 00 00",
    "get firmwareVersion"   : "FF 70 07 6B 08 A2 06 A0 04 A0 02 85 00 00",
    "get hardwareVersion"   : "FF 70 07 6B 08 A2 06 A0 04 A0 02 89 00 00",
    "get vendorName"        : "FF 70 07 6B 08 A2 06 A0 04 A0 02 8F 00 00",
    
}

def send_APDU_cmd(key_str):
    print(blue_color + "\n# " + key_str + reset_color)
    apdu_cmd_str_with_space=APDU[key_str]
    command = toBytes(apdu_cmd_str_with_space)   
    response, sw1, sw2 = connection.transmit(command)
    
    str_rsp = toHexString(response)
    str_sw = toHexString([sw1, sw2])
    #Print the response data
    if sw1 == 0x90 and sw2 == 0x00:
        print("cmd \t" + apdu_cmd_str_with_space)
        print("rsp \t" + str_rsp)
        print("\theader   " + toHexString(response[:3]))
        print("\tlength   " + str(response[3]))
        converted_str = toASCIIString(response[4:])
        if all(c == '.' for c in converted_str):
            print("\tdata     " + cyan_color + toHexString(response[4:]) + reset_color)
        else:
            print("\tdata     " + green_color + converted_str.rstrip('.') + reset_color)
        #print("\tdata     " + green_color + toASCIIString(response[4:]) + reset_color)
        print("\tstatus   " + str_sw)
    else:
        print("\tError reading data from the card.")
        print("\trsp = {}\tstatus = {}".format(str_rsp, str_sw))


#Establish connection with the card reader
reader = readers()[0]
print(yellow_color + str(reader) + reset_color)
connection = reader.createConnection()

try:
    connection.connect()

    #Transmit APDU command to retrieve data from the card
    for key in APDU:
        send_APDU_cmd(key)   
        
    # Disconnect from the card reader
    connection.disconnect()
    
except Exception as e:
    print(red_color + str(e) + reset_color)
    