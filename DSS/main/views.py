from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
# Create your views here.
from main.Encrypt.write_img import *
from main.Decrypt.read_img import *
import PIL
from io import BytesIO
from .models import * 

def login(request):
	return render(request, 'login.html')

def home(request):
	return render(request, 'home.html')

def decrypt_text(user_name,message):
	'''
		This function is used to decrypt the message
		using the private key of the user
	'''
	from Crypto.PublicKey import RSA
	from Crypto.Cipher import PKCS1_OAEP
	from base64 import b64decode

	message = decode_base64(message)
	cipher_text = message

	user_key = keys.objects.get(user_id=get_user_model().objects.get(username=user_name))
	# cipher_text = b64decode(message)
	keyPvt = RSA.importKey(user_key.private_key)
	cipher = PKCS1_OAEP.new(keyPvt)
	decrypted = cipher.decrypt(cipher_text)
	print("Decrypted string :: ",str(decrypted))
	return decrypted

def show_encryption(request):
	# RSAkey = RSA.generate(1024)
	dev_key = keys.objects.get(user_id=get_user_model().objects.get(username="Dev"))
	print()
	context = {
	}
	if request.method == 'POST':		
		key = request.POST.get("key")
		file = request.FILES.get("file")
		message = request.POST.get("message")

		with open(f'media/image/image.png', 'wb+') as destination:
			for chunk in file.chunks():
				destination.write(chunk)
		if request.user.username == "Dev":
			user_name = "Javal"
		else:
			user_name = "Dev"
		# print("Encrypted using public key of: ",user_name)
		# encrypt_main_2(message, user_name)
		encrypt_main(
			message=request.POST.get("message"),
			key=request.POST.get("key"),
			input_image_name=f'media/image/image.png',
			output_file_name=f'media/encrypt/image.png',
			# image=request.FILES['file']
		)

	return render(request, 'encryption.html',context)



def show_decryption(request):
	if request.method == "POST":
		key = request.POST.get("key")
		file = request.FILES.get("file")
		print(key,type(key))
		with open(f'media/encrypt/image.png', 'wb+') as destination:
			for chunk in file.chunks():
				destination.write(chunk)
		message = decrypt_main(int(key),"asd")

		return render(request, 'output.html',{'message':message})
	return render(request, 'decryption.html')

#region extra code

# code to assign keys to the users
	# dev = get_user_model().objects.all()[1]

	# dev.keys.public_key
	# # print(RSAkey.privatekey().exportKey())
	# dev.keys.public_key = RSAkey.publickey().exportKey()
	# dev.keys.private_key = RSAkey.exportKey()
	# dev.keys.save()
# endcode

#endregion 