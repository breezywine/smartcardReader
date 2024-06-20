
# ---
# Check if file argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

# Check if file exists
file="$1"
if [ ! -f "$file" ]; then
    echo "Error: File '$file' not found."
    exit 1
fi

# warning if uses "0_CAPK"
if [[ "$1" == *"0_CAPK"* ]]; then
    echo "Warning: should use '1_CAPK' instead of '0_CAPK'"
fi

# ---
# File Variables
BINARY_FILE=$1
HEADER_FILE="header.bin"
OUTPUT_FILE=${BINARY_FILE%.*}".SYS"
# assign output filename for SIRIUS
if [[ "$BINARY_FILE" == *"0_ENTRY_POINT_CONFIGURATION"* ]]; then
    OUTPUT_FILE="ENTPT.SYS"
fi
if [[ "$BINARY_FILE" == *"0_PROCESSING_CONFIGURATION"* ]]; then
    OUTPUT_FILE="PROCE.SYS"
fi
if [[ "$BINARY_FILE" == *"0_TERMINAL_CONFIGURATION"* ]]; then
    OUTPUT_FILE="TERML.SYS"
fi
if [[ "$BINARY_FILE" == *"1_CAPK"* ]]; then
    OUTPUT_FILE="CAPK1.SYS"
fi

# ---
# Define the header components in Big Endian
# SIRIUS: 2 bytes file length (start from file slot till EOF) | 1 byte file slot | 4 bytes version
# KENETICS: 2 byte file ID | 1 byte file version | 4 bytes version
HEADER_SIZE=7 
FILE_LENGTH_SIZE=2

FILE_LENGTH=$(stat -c%s "$BINARY_FILE")
FILE_LENGTH=$((FILE_LENGTH + HEADER_SIZE - FILE_LENGTH_SIZE))
FILE_LENGTH_HEX=$(printf "%04X" $FILE_LENGTH)
FILE_LENGTH_BYTES=$(echo $FILE_LENGTH_HEX | sed 's/../\\x& /g' | awk '{print $1$2}')

FILE_SLOT_HEX=$(printf "%02X" "${BINARY_FILE:0:1}") # 01 CAPK, the rest should be 00
FILE_SLOT_BYTES="\x${FILE_SLOT_HEX}"

read -p "Enter the file version: " FILE_VERSION
# FILE_VERSION="20240131"
FILE_VERSION_BYTES=$(echo $FILE_VERSION | sed 's/../\\x& /g' | awk '{print $1$2$3$4}')



# ---
# printout
echo -ne "\t" && echo "FILE_LENGTH      $FILE_LENGTH_BYTES"
echo -ne "\t" && echo "FILE_SLOT        $FILE_SLOT_BYTES"
echo -ne "\t" && echo "FILE_VERSION     $FILE_VERSION_BYTES"

# Create the 16-byte header
echo -ne "${FILE_LENGTH_BYTES}${FILE_SLOT_BYTES}${FILE_VERSION_BYTES}" > "$HEADER_FILE"



# ---
# Concatenate header, binary file, and CRC
cat "$HEADER_FILE" "$BINARY_FILE" > "$OUTPUT_FILE"

# Clean up temporary files
rm "$HEADER_FILE"

echo "Packed $BINARY_FILE into $OUTPUT_FILE with 7 bytes header."