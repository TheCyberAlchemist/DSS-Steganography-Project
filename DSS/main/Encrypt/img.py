from PIL import Image
imgc = Image.open("D:\Semester-6\DSS\Project\DSS-Steganography-Project\DSS\media\image\image.jpg")
imgo = Image.open("D:\Semester-6\DSS\Project\DSS-Steganography-Project\DSS\media\encrypt\image.jpg")
a = 0
for i in range(imgc.size[0]):
	for j in range(imgo.size[1]):
		if imgo.getpixel((i,j)) != imgc.getpixel((i,j)):
			print(imgo.getpixel((i,j)),"\t",imgc.getpixel((i,j)))
			a += 1
		# a += 1
print(a)
		