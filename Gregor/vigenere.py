from time import time
import numpy as np
from matplotlib import pyplot as plt

swedish_frequencies = [9.38, 1.54, 1.49, 4.70, 10.15, 2.03, 2.86, 2.09, 5.82, 0.61, 3.14, 5.28, 3.47, 8.54, 4.48, 1.84, 0.02, 8.43, 6.59, 7.69, 1.92, 2.42, 0.14, 0.16, 0.71, 0.07, 1.34, 1.80, 1.31]
swedish_ic = 0.060524640000000005

def readFile(path):
    # reads the file from provied path and returns the content of the file as a string 
    f = open(path, encoding="utf-8", mode="r")
    content = f.read()
    f.close()

    return content

def writeFile(path, content):
    # writes the content to the file speficied by the provied path 
    f = open(path, encoding="utf-8", mode="w+")
    f.write(content)
    f.close()
    
def fromASCII(character):
    # returns the integer representation of the provided character
    # return -1 if character is not part of the swedish alphabet
    if ((ord('a') <= ord(character)) and (ord(character) <= ord('z'))):
        return ord(character) - ord('a')
    elif (character == 'å'):
        return 26
    elif (character == 'ä'):
        return 27
    elif (character == 'ö'):
        return 28
    return -1

def toASCII(integer):
    # returns the character represented by the provided integer
    # return '\0' if the integer is not representing a character of the swedish alphabet
    if ((0 <= integer) and (integer <= 25)):
        return chr(integer + ord('a'))
    elif (integer == 26):
        return 'å'
    elif (integer == 27):
        return 'ä'
    elif (integer == 28):
        return 'ö'
    return '\0'

def transformPlainText(plaintext):
    # transform and returns the plaintext as specified in the assignment
    # (only lowercase letters and only characters that are part of the alphabet)
    plaintext = plaintext.lower()

    output = ""
    for c in plaintext:
        if (fromASCII(c) != -1):
            output += c

    return output

def encrypt(key, plaintext):
    # encrypts the plaintext with the key und returns the ciphertext
    # can the used for decryption if the sign of each key element is -
    
    n = len(key)

    position = 0
    ciphertext = ""

    # for every character c
    for character in plaintext:
        # convert from ascii to integer representation
        intRep = fromASCII(character)
        
        # select current key element
        k = key[position]

        # update key position
        position = (position + 1) % n

        # shift character
        shifted = (intRep + k + 29) % 29

        # convert from integer representation to ascii and append to ciphertext
        ciphertext += toASCII(shifted)
    
    return ciphertext

def transform_key(key, sign = 1):
    # translates key from string to array of integer
    # sign = 1 for encryption, sign = -1 for decryption
    return [sign * fromASCII(c) for c in key]

def encrypt_file(keyPath, plaintextPath, ciphertextPath):
    # read, transform and save transformed plaintext
    plaintext = transformPlainText(readFile(plaintextPath))
    writeFile(plaintextPath, plaintext)

    # read and transform key
    key = transform_key(readFile(keyPath))

    # encrypt plaintext with key
    ciphertext = encrypt(key, plaintext)

    print(f"Ciphertext={ciphertext}")

    # write encrypted text (ciphertext)
    writeFile(ciphertextPath, ciphertext)

def decrypt_file(keyPath, plaintextPath, ciphertextPath):
    # read cipher text
    ciphertext = readFile(ciphertextPath)

    # read and transform key
    key = transform_key(readFile(keyPath), - 1)

    # decrypt cipher with key
    plaintext = encrypt(key, ciphertext)

    print(f"Plaintext={plaintext}")

    # write decrypted text (plaintext)
    writeFile(plaintextPath, plaintext)

def character_occurance_counter(keyLength, ciphertext):
    # counts occuring characters for all key characters k_j in x^j
    # calculates all f_i(x^j)
    counts = np.zeros((keyLength, 29))

    for i in range(len(ciphertext)):
        counts[i % keyLength][fromASCII(ciphertext[i])] += 1
    
    return counts

def frequency_analysis(keyLength, ciphertext):
    # implementation of frequency analysis from lecture
    # return the most likley key
    # all other possibilites sorted by their likelyhood for k_j are printed
    print("Frequency analysis:")
    # get occurances equivalent to f_i(x^j)
    occurances = character_occurance_counter(keyLength, ciphertext)

    I = len(ciphertext) / keyLength
    key = ""
    result = []

    # for each position in key
    for j in range(0, keyLength):
        result.append([])
        max = 0
        k_j = 'a'
        # find the character k_j that has the maximal sum
        for k in range(0, 29):
            # compute sum
            sum = 0
            for i in range(0, 29):
                sum += (swedish_frequencies[i] / 100) * (occurances[j][(i + k) % 29] / I)
            # update max
            if sum > max:
                max = sum
                k_j = toASCII(k)

            result[j].append((toASCII(k), sum))
        # update key
        key += k_j

        # print all possible characters for each k_j sorted by their likelyhood
        result[j].sort(key=lambda x: x[1], reverse = True)
        print(f"k_{j}={result[j][:5]}")

    print(f"Key={key}")
    
    return key

def kasiski_test(maxKeyLength, ciphertext):
    # implementation of the kasiski test from text lecture
    # divisors will be displayed as a matplotlib bar chart
    # this method is more helpful to verify the solution of the friedman test
    print("Kasiski Test:")

    # finds identical segments in ciphertext with 3 <= length <= n/2
    # gether them in dict with segment as key and positions as values
    segments = {}
    for length in range(3, len(ciphertext) // 2):
        for position in range(0, len(ciphertext) - length):
            segment = ciphertext[position:position + length]
            if not (segment in segments):
                segments.update({segment : [position]})
            else:
                segments[segment].append(position)
    # remove segements which occur once
    segments = {segment:positions for (segment, positions) in segments.items() if len(positions) > 1}

    distances = {}
    deltas = set()

    # calculate the deltas from the positions of the segments
    for segment, positions in segments.items():
        for i in range(0, len(positions) - 1):
            for j in range(i + 1, len(positions)):
                distance = positions[j] - positions[i]
                if not (segment in distances):
                    distances.update({segment : [distance]})
                else:
                    distances[segment].append(distance)
                deltas.add(distance)

    # for every m with 1 <= m <= maxKeyLength + 1 count for all detlas how often delta % m == 0
    divisors = {}
    for divisor in range(1, maxKeyLength + 1):
        divisors.update({divisor : 0})
        for delta in deltas:
            if (delta % divisor == 0):
                divisors[divisor] += 1

    # print result sorted by count
    print(f"{sorted(divisors.items(), key=lambda x:x[1], reverse = True)}")

    # plot fidings instead of finding greatest common divisor
    plt.bar(divisors.keys(), divisors.values())
    plt.xlabel("Divisors")
    plt.ylabel("No. of divisor of delta")
    plt.title("Possible key lengths")
    plt.show()

    return divisors

def compute_ic(keyLength, ciphertext):
    # calculates the IC^m(x) from the lecture
    occurances = character_occurance_counter(keyLength, ciphertext)
    I = len(ciphertext) / keyLength
    sum = 0
    # sums up all IC(x^j)
    for entry in occurances:
        for f in entry:
            sum += (f * (f - 1) / (I * (I - 1)))

    # compute average
    IC = sum / keyLength

    return IC

def friedman_test(maxKeyLength, ciphertext):
    # implements the friedman test from the lecture
    # return the m which maximizes IC^m(x)
    print("Friedman Test:")
    max = 0
    m = -1
    for i in range(1, maxKeyLength + 1):
        ic = compute_ic(i, ciphertext)
        if ic > max:
            max = ic
            m = i
        print(f"IC^{i}(x)={ic}")
    print(f"m={m}")
    return m

def break_cipher(filename, maxKeyLength, keyLength=0, key=""):
    # get start time
    start = time()
    # read ciphertext
    ciphertext = readFile(filename + ".crypto")

    if len(key) == 0:
        # if no key is provided use frequency analysis to find key
        if keyLength <= 0:
            # if no key length is provided use friedman test to find key length
            keyLength = friedman_test(maxKeyLength, ciphertext)
            #kasiski_test(maxKeyLength, ciphertext) # can be used to verify findings from friedman test
        key = frequency_analysis(keyLength, ciphertext)

    # write key
    writeFile(filename + ".key", key)
    # decrypt ciphertext and write plaintext
    decrypt_file(filename + ".key", filename + ".plain", filename + ".crypto")
    # print run time
    print(f"Runtime={time() - start} s")
    
# use break_cipher
# filename without file ending must be provided to the ciphertext (file needs to end with .crypto)
# maxKeyLength needs to be provided or keyLength if the key length is already known (from previous runs)
# the key can be provided if known
# this can be usefull if only some characters of the key from the previous run are not correct
break_cipher(filename="students/vig_group12", maxKeyLength=16)