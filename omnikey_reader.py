from smartcard.System import readers
from smartcard.util import toHexString, toBytes, toASCIIString 
from smartcard.Exceptions import CardConnectionException, NoCardException

# ANSI escape code for color
reset_color = '\033[0m'
blue_color = "\033[34m"
green_color = '\033[92m'
red_color = '\033[91m'


# https://www3.hidglobal.com/sites/default/files/resource_files/plt-03099_a.5_-_omnikey_sw_dev_guide_0.pdf
APDU = {
    "get productName"   : "FF 70 07 6B 08 A2 06 A0 04 A0 02 82 00 00",
    "get serialNumber"  : "FF 70 07 6B 08 A2 06 A0 04 A0 02 92 00 00",
    "get firmwareLabel" : "FF 70 07 6B 08 A2 06 A0 04 A0 02 96 00 00",

}

def send_APDU_cmd(key_str):
    print("\n# " + key_str)
    apdu_cmd_str_with_space=APDU[key_str]
    command = toBytes(apdu_cmd_str_with_space)   
    response, sw1, sw2 = connection.transmit(command)
    
    str_rsp = toHexString(response)
    str_sw = toHexString([sw1, sw2])
    #Print the response data
    if sw1 == 0x90 and sw2 == 0x00:
        print("Data successfully read from the card:")
        print(str_rsp)
        print("\theader   " + toHexString(response[:3]))
        print("\tdata     " + green_color + toASCIIString(response[3:]) + reset_color)
        print("\tstatus   " + str_sw)
    else:
        print("\tError reading data from the card.")
        print("\trsp = {}\tstatus = {}".format(str_rsp, str_sw))


#Establish connection with the card reader
reader = readers()[0]
print(reader)
connection = reader.createConnection()

try:
    connection.connect()

    #Transmit APDU command to retrieve data from the card
    for key in APDU:
        send_APDU_cmd(key)   
        
    # Disconnect from the card reader
    connection.disconnect()
    
except NoCardException:
    print("ERROR: Card not present")
    