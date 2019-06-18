import sys
from spectral import open_image, imshow

if __name__ == "__main__":
	img = open_image(sys.argv[1]).load()
	view = imshow(img, (79, 69, 57))
	x = input()
