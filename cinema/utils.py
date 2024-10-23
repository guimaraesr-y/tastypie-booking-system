def number_to_char(number):
    return chr(ord('A') + number - 1)

def char_to_number(char):
    return ord(char) - ord('A') + 1
