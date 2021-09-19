import hashlib
import string
import random
import xlsxwriter

# Function for generating unique strings to hash attack.
def createString(s):
    newS = []
    sprime = ""
    incrStringLen = True

    # Create a char array of string
    for i in s:
        newS.append(i)

    # Increment string by 1
    for i in range(len(newS)):
        if (newS[i] < 'z'):
            newS[i] = chr(ord(newS[i]) + 1)
            incrStringLen = False
            break
    
    # All values in string are 'z', reset to '0' and add a new char
    if (incrStringLen == True):
        # Reset the string to all 0's
        for i in range(len(newS)):
            newS[i] = '0'

        # Add a '0', increasing string length by 1
        newS.append('0')

    # Convert char array to string
    for i in newS:
        sprime += i

    return sprime

# Function for returning an integer value from a hex string
def stringToHex(s): return int(s,16)

# Wrapper for SHA256 that completes the SHA256 hash and then truncates to specified 'n' bits
def wrapperSHA256(s, n):
    
    if(n == 8): result = hashlib.sha256(s.encode()).hexdigest()[:2]
    elif(n == 10): 
        result = hashlib.sha256(s.encode()).hexdigest()[:3]
        # Keep first byte
        temp = stringToHex(result) & 0xFF0
        # Truncate last byte
        temp2 = ((stringToHex(result) & 0x00F) >> 2) << 2
        result = hex(temp ^ temp2)[2:]       
    elif(n == 12): result = hashlib.sha256(s.encode()).hexdigest()[:3]
    elif(n == 14):
        result = hashlib.sha256(s.encode()).hexdigest()[:4]
        # Keep first byte
        temp = stringToHex(result) & 0xFF00
        # Truncate last byte
        temp2 = ((stringToHex(result) & 0x00FF) >> 2) << 2
        result = hex(temp ^ temp2)[2:]
    elif(n == 16): result = hashlib.sha256(s.encode()).hexdigest()[:4]
    elif(n == 18):
        result = hashlib.sha256(s.encode()).hexdigest()[:5]
        # Keep first 2 bytes
        temp = stringToHex(result) & 0xFFF00
        # Truncate last byte
        temp2 = ((stringToHex(result) & 0x000FF) >> 2) << 2
        result = hex(temp ^ temp2)[2:]
    elif(n == 20): result = hashlib.sha256(s.encode()).hexdigest()[:5]
    elif(n == 22):
        result = hashlib.sha256(s.encode()).hexdigest()[:6]
        # Keep first 2 bytes
        temp = stringToHex(result) & 0xFFFF00
        # Truncate last byte
        temp2 = ((stringToHex(result) & 0x0000FF) >> 2) << 2
        result = hex(temp ^ temp2)[2:]

    return result

def main():
    
    n = 8
    c = 0
    workbook = xlsxwriter.Workbook('hashattackresults.xlsx')
    collisionsheet = workbook.add_worksheet('collision_sheet')
    preimagesheet = workbook.add_worksheet('preimagesheet')

    # Complete Collision Attack
    while (n < 24):
        succCollAttack = []
        for j in range(50): 
            counter = 0
            collisionLibrary = []
            collisionFound = False

            while(1):
                s = ''.join(random.choice(string.ascii_lowercase) for i in range(10)) # Pulled from https://www.educative.io/edpresso/how-to-generate-a-random-string-in-python
                counter += 1

                # Get hash value
                value = wrapperSHA256(s, n)

                # Check array for match
                for i in range(len(collisionLibrary)):
                    if (value == collisionLibrary[i]): collisionFound = True

                if (collisionFound == True): break                    
                
                # If there was no match, append the value to the library
                collisionLibrary.append(value)
            
            succCollAttack.append(counter)
        # Write values to excel sheet
        for r in range(50):
            collisionsheet.write(r, c, succCollAttack[r])

        n += 2
        c += 1
    
    n = 8
    c = 0

    # Conduct Pre-Image Attack
    while(n < 24):
        randomStringLibrary = []
        succPreImgAttack = []

        # Generate a library of 50 random strings of length 20
        for i in range(50):
            s = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
            randomStringLibrary.append(s) 
        
        for i in range(50):
            counter = 0
            collisionFound = False

            while(1):
                counter += 1
                
                # Get has value
                value = wrapperSHA256(randomStringLibrary[i], n)

                s = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
                attackvalue = wrapperSHA256(s, n)

                if (value == attackvalue): collisionFound = True
                if (collisionFound == True): break
            
            succPreImgAttack.append(counter)

        for r in range(50):
            preimagesheet.write(r, c, succPreImgAttack[r])
        n += 2
        c += 1
          
    workbook.close()

if __name__ == "__main__":
    main()