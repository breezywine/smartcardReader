from smartcard.System import readers
from smartcard.util import toHexString, toBytes
from smartcard.Exceptions import CardConnectionException, NoCardException

# https://www3.hidglobal.com/sites/default/files/resource_files/plt-03099_a.5_-_omnikey_sw_dev_guide_0.pdf
APDU_get = {
    "productName"   : "FF 70 07 6B 08 A2 06 A0 04 A0 02 82 00 00",
    "serialNumber"  : "FF 70 07 6B 08 A2 06 A0 04 A0 02 92 00 00",


}

#Establish connection with the card reader
reader = readers()[0]
print(reader)
connection = reader.createConnection()

try:
    connection.connect()

    #Transmit APDU command to retrieve data from the card
    command = toBytes(APDU_get["uid"])   
    response, sw1, sw2 = connection.transmit(command)
    
    str_rsp = toHexString(response)
    str_sw = toHexString([sw1, sw2])
    #Print the response data
    if sw1 == 0x90 and sw2 == 0x00:
        print("Data successfully read from the card:")
        print(toHexString(response))
    else:
        print("Error reading data from the card.")
        print("rsp = {}\tstatus = {}".format(str_rsp, str_sw))
        
    # Disconnect from the card reader
    connection.disconnect()
    
except NoCardException:
    print("ERROR: Card not present")
    