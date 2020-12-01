import glob
import os

file_list = glob.glob('./milb_photos/*.jpg')
# file_list = glob.glob('./prospect_photos/*.jpg')

for file in file_list:
	print(file)
	with open(file, 'rb') as f:
		im = f.read()
	os.remove(file)
	file = file.replace('.jpg', '.png')
	with open(file, 'wb') as f:
		f.write(im)
