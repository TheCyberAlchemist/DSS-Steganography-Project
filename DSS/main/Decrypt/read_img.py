import PIL
from PIL import Image
import numpy as np
import hashlib
def messageToBinary(message):
  if type(message) == str:
    return ''.join([ format(ord(i), "08b") for i in message ])
  elif type(message) == bytes or type(message) == np.ndarray:
    return [ format(i, "08b") for i in message ]
  elif type(message) == int or type(message) == np.uint8:
    return format(message, "08b")
  else:
    raise TypeError("Input type not supported")

def BinaryToString(binary):
    str_data =' '
    for i in range(0, len(binary), 8):
        temp_data = binary[i:i + 8]
        decimal_data = int(temp_data)
        str_data = str_data + chr(decimal_data)
    return str_data


def gethash(input_input_image_name = "media/encrypt/image.png"):
    with open(input_input_image_name,"rb") as f:
        hash = f.read()
        if hash[-1:] != b"\x82":
            print(hash[-1:])  
            print("hi")  
            b = hash[-64:]
            other_file = hash[:-64]
            #print(b)
            with open(input_input_image_name,"wb") as f:
                del_hash = f.write(other_file)
                return b
        else:
            print("Hi2")
            return False

def checkhash(hash, input_input_image_name = "media/encrypt/image.png"):
    ''' 
      Returns if the given hash is correct for the given file
      else Returns False
    '''
    hash = hash.decode("utf-8")
    with open(input_input_image_name,"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest();
        
        print(readable_hash)
        print(hash)
        if readable_hash == hash:
            return True
        else:
            return False


import base64
import re

def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)

def decrypt_text(user_name,message):
    '''
        This function is used to decrypt the message
        using the private key of the user
    '''
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
    from base64 import b64decode
    from main.models import keys
    from django.contrib.auth import get_user_model

    message = decode_base64(message)
    cipher_text = message

    user_key = keys.objects.get(user_id=get_user_model().objects.get(username=user_name))
    # cipher_text = b64decode(message)
    keyPvt = RSA.importKey(user_key.private_key)
    cipher = PKCS1_OAEP.new(keyPvt)
    decrypted = cipher.decrypt(cipher_text)
    print("Decrypted string :: ",str(decrypted))
    return decrypted



def decrypt(text,s):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char == " ":
            result += " "
        elif (char.isupper()):
            result += chr((ord(char) - s-65) % 26 + 65)
        else:
            result += chr((ord(char) - s - 97) % 26 + 97)
    return result

def img2message(input_input_image_name = "media/encrypt/image.png"):
    # print("here")
    img = PIL.Image.open(input_input_image_name)
    # img = image
    pixel = img.load()
    binary_mess = ""
    for i in range(10):
        for j in range(img.size[1]):
            pix = img.getpixel((i,j))
            pix = pix[:3]
            r,g,b = pix
            r = messageToBinary(r)
            g = messageToBinary(g)
            b = messageToBinary(b)
            binary_mess += r[-1]
            binary_mess += g[-1]
            binary_mess += b[-1]
            all_bytes = [ binary_mess[i: i+8] for i in range(0, len(binary_mess), 8) ]
    extracted_data = ""
    for byte in all_bytes:
        if extracted_data[-3:] == "~~~":
            print("here in break")
            break
        extracted_data += chr(int(byte, 2))
    print("Extracted data: ",extracted_data)
    return extracted_data

if __name__ == "__main__":
    key = int(input("Enter decrytion key:- "))
    img2message(key)

def decrypt_main(key,image_path):
    getHash = gethash()
    if getHash == False:
        return "Your message is altered"
    else:
        check = checkhash(getHash)
        if check == True:
            cipher_text = img2message()
            print(cipher_text[:-3])
            a= cipher_text[:-3]
            decrypted_text = decrypt(a,key)
            decrypt(a,key)
            print("Decrypted text: ",decrypted_text)
            return decrypted_text
        else:
            return "Your message is altered"