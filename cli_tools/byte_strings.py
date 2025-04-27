def format_byte_string(byte_string):
    """Format a byte string in multiple representations."""
    # Hex representation
    hex_repr = ' '.join([f'\\x{byte:02x}' for byte in byte_string])
    
    # Hex array representation
    hex_array = [hex(byte) for byte in byte_string]
    
    # Decimal representation
    decimal_array = [str(byte) for byte in byte_string]
    
    # Try UTF-8 decoding
    try:
        utf8_decoded = byte_string.decode('utf-8')
    except UnicodeDecodeError:
        utf8_decoded = "Not valid UTF-8"
    
    # ASCII representation (replacing non-printable chars with dots)
    ascii_repr = ''.join([chr(byte) if 32 <= byte <= 126 else '.' for byte in byte_string])
    
    return {
        'raw': byte_string,
        'hex': hex_repr,
        'hex_array': hex_array,
        'decimal': decimal_array,
        'utf8': utf8_decoded,
        'ascii': ascii_repr
    }

# Example byte string (you can modify this or input your own)
example = b'Hello\x00\x1B[31m\xF0\x9F\x98\x80\x7F\xFF World!'

# Function to print the formatted output
def print_byte_string_info(byte_string):
    result = format_byte_string(byte_string)
    print("\nByte String Analysis:")
    print("-" * 50)
    print(f"Raw bytes: {result['raw']}")
    print(f"Hex format: {result['hex']}")
    print(f"Hex array: {result['hex_array']}")
    print(f"Decimal values: {result['decimal']}")
    print(f"ASCII representation: {result['ascii']}")
    print(f"UTF-8 decoded (if possible): {result['utf8']}")
    print("-" * 50)

# Test with the example
print_byte_string_info(example)

# You can also input your own byte string using Python byte string syntax
print("\nInput your byte string using Python syntax.")
print("For example: b'\\x1bc\\xff\\xfb'")
user_input = input("Enter a byte string (or press Enter to skip): ")
if user_input:
    try:
        # Safely evaluate the input as a Python expression
        custom_bytes = eval(user_input)
        if isinstance(custom_bytes, bytes):
            print_byte_string_info(custom_bytes)
        else:
            print("Input must evaluate to a bytes object")
    except Exception as e:
        print(f"Error processing input: {e}")
