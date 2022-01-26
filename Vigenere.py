def encrypt(p, key):
    p = p.lower()
    key = key.lower()
    a = []              #number version of plain text
    b = []              #number version of key
    c = []              #number version of cipher
    cipher = ""         #cipher after encryption
    # convert plain text to number
    for character in p:
        if (ord(character) > 96 and ord(character) < 123):
            a.append(ord(character) - 97)
        elif (ord(character) == 229):
            a.append(26)
        elif (ord(character) == 228):
            a.append(27)
        elif (ord(character) == 246):
            a.append(28)
    # convert key to number
    for character in key:
        if (ord(character) > 96 and ord(character) < 123):
            b.append(ord(character) - 97)
        elif (ord(character) == 229):
            b.append(26)
        elif (ord(character) == 228):
            b.append(27)
        elif (ord(character) == 246):
            b.append(28)


    # transfer plaint number to cipher number
    number_transfer(a, b, c)

    # convert number version of cipher to text
    for e in c:
        if e < 26:
            cipher += chr(e+97)
        elif e == 26:
            cipher += "å"
        elif e == 27:
            cipher += "ä"
        elif e == 28:
            cipher += "ö"
    return cipher


def number_transfer(a, b, c):
    for i in range(0, len(a)):
        c.append((a[i] + (b[i % len(b)]))%29)

if __name__ == '__main__':

    p = input("Please input your plaintext:")
    key = input("Please input your key:")
    encrypt(p, key)
    print("The cipher is: " + encrypt(p, key))
