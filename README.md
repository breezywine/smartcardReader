# smartcardReader
```console

C:\PythonScript\smartcard>py omnikey_reader.py
HID Global OMNIKEY 3x21 Smart Card Reader 0

# get productName
Data successfully read from the card:
BD 0F 82 0D 4F 4D 4E 49 4B 45 59 20 33 30 32 31 00
        header   BD 0F 82
        data     .OMNIKEY 3021.
        status   90 00

# get productPlatform
Data successfully read from the card:
BD 0A 83 08 41 56 69 61 74 6F 52 00
        header   BD 0A 83
        data     .AViatoR.
        status   90 00

# get serialNumber
Data successfully read from the card:
BD 02 92 00
        header   BD 02 92
        data     .
        status   90 00

# get firmwareLabel
Data successfully read from the card:
BD 32 96 30 41 56 52 43 43 2D 31 2E 33 2E 31 2E 32 30 38 2D 32 30 31 36 30 32 30 33 54 30 39 30 36 32 35 2D 38 31 34 37 31 35 46 46 31 45 38 36 2D 52 4F 4D
        header   BD 32 96
        data     0AVRCC-1.3.1.208-20160203T090625-814715FF1E86-ROM
        status   90 00

# get firmwareVersion
Data successfully read from the card:
BD 05 85 03 01 03 01
        header   BD 05 85
        data     ....
        status   90 00

# get hardwareVersion
Data successfully read from the card:
BD 11 89 0F 50 43 42 2D 30 30 31 30 30 20 52 45 56 32 00
        header   BD 11 89
        data     .PCB-00100 REV2.
        status   90 00

```
