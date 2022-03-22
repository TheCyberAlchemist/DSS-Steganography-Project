import PIL
from PIL import Image
import numpy as np
from main.models import keys
from django.contrib.auth import get_user_model
def messageToBinary(message):
	'''
		This function is used to convert the message into binary
		takes the message as input and returns the binary value
	'''
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
    for i in range(0, len(a), 8):
        temp_data = a[i:i + 8]
        decimal_data = b2d(temp_data)
        str_data = str_data + chr(decimal_data)
    return str_data


def encrypt(text,s):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char == " ":
        	result += " "
        elif (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)
    return result

#def decrypt(message,key):
def message2img(binary_message,input_input_image_name="media/image/image.png",output_file_name="media/encrypt/image.png",image=None):
	'''
		Function to add the binary message to the image
		takes the binary message, the input_image_name and the output_image_name
	'''
	img = PIL.Image.open(input_input_image_name)
	pixel = img.load()
	width, height = img.size
	mess_len = len(binary_message)
	data_index = 0
	Max = width*height*3
	if mess_len >= Max:
		print("Please enter small message....")
	else:
		x,y = 0,0
		for i in range(img.size[0]):
			for j in range(img.size[1]):
				pix = img.getpixel((i,j))
				pix = pix[:3]
				r,g,b = pix
				pix = list(pix)
				r = messageToBinary(r)
				g = messageToBinary(g)
				b = messageToBinary(b)
				if data_index < mess_len:
					# hide the data into least significant bit of red pixel
					pix[0] = int(r[:-1] + binary_message[data_index], 2)
					data_index += 1
				if data_index < mess_len:
					# hide the data into least significant bit of green pixel
					pix[1] = int(g[:-1] + binary_message[data_index], 2)
					data_index += 1
				if data_index < mess_len:
					# hide the data into least significant bit of  blue pixel
					pix[2] = int(b[:-1] + binary_message[data_index], 2)
					data_index += 1
				# if data is encoded, just break out of the loop
				if data_index >= mess_len:
					break				
				pixel[i,j] = tuple(pix)
		img.save(output_file_name)
		print("Your new image is stored with the name stag_img.png")

def encrypt_text(user_name,message):
	'''
		This function is used to encrypt the message
		using the public key of the user
	'''
	from Crypto.PublicKey import RSA
	from Crypto.Cipher import PKCS1_OAEP
	from base64 import b64encode
	user_key = keys.objects.get(user_id=get_user_model().objects.get(username=user_name))
	keyPub = RSA.importKey(user_key.public_key)
	cipher = PKCS1_OAEP.new(keyPub)
	cipher_text = cipher.encrypt(message.encode())
	emsg = b64encode(cipher_text)
	# print("Encrypted string :: ",str(emsg))
	return emsg

def encrypt_main_2(message,user_name):
	cipher_text = encrypt_text(user_name,message)
	# print("Encrypted string :: ",str(cipher_text))
	binary_message = messageToBinary(cipher_text)
	print(binary_message)
	message2img(binary_message)
	pass


def encrypt_main(message,key,input_image_name,output_file_name=None,image=None):
	message = encrypt(message,int(key))
	message += "~~~~" # we used ~~~~ as the end of the message
	print(message)
	binary_message = messageToBinary(message)
	print("The Binary value after string conversion is:",binary_message)
	message2img(binary_message,input_image_name,output_file_name,image)

if __name__ == "__main__":
	#message = "Hi this is Javal"
	#key = 4
	message = input("Enter message:- ")
	key = input("Enter encrytion key:- ")
	message = encrypt(message,int(key))
	message += "thisisend" #we used ~~~~ as the end of the message
	print(message)
	binary_message = messageToBinary(message)
	#print(len(binary_message))
	#print("The Binary value after string conversion is:",binary_message)
	message2img(binary_message)

