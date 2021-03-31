
import imageio
import numpy as np
import sys
import math
# reads jpg image "imageFilename".jpg draws in a black rectangle centered at "center" with height "height" and width
# "width" and returns modified image
#def drawRectangleOnImage(imageFilename, center, height, width):


# given a 2D numpy array representing an image, draws a rectangle centered at (centerXAxis, centerYAxis) of
# width "width" and height "height" on it and returns the image in array form. Note that the coordinate
# system used for center coordinates has origin at bottom left pixel of image. 
def drawRectangleOnImage(imageArray, centerXAxis, centerYAxis, height, width):

	# get image height and width
	imageHeight = imageArray.shape[0] 
	imageWidth = imageArray.shape[1]


	# rectangle edge coordinates
	leftEdgeXCoord = centerXAxis - int(width / 2)
	
	rightEdgeXCoord = leftEdgeXCoord + width
	
	topEdgeYCoord = centerYAxis + int(height / 2)

	bottomEdgeYCoord = topEdgeYCoord - height

	# does rectangle overflow? 
	if ((leftEdgeXCoord < 0) or (rightEdgeXCoord < 0)  or (leftEdgeXCoord > (imageWidth - 1)) or (rightEdgeXCoord > (imageWidth - 1))
		or (topEdgeYCoord < 0) or (bottomEdgeYCoord < 0) or (topEdgeYCoord > (imageHeight - 1)) or (bottomEdgeYCoord > (imageHeight - 1))):
		
		print("drawRectangleOnImage error: rectangle does not fit in image")
		
		return

	# draw! 
	for x in range(leftEdgeXCoord, rightEdgeXCoord): 

		for y in range(bottomEdgeYCoord, topEdgeYCoord): 

			# get indeces of imageArray to access
			rowIndex = (imageHeight - (y + 1)) - 1
			columnIndex = x

			# blacken
			imageArray[rowIndex][columnIndex] = 0

	return imageArray


# returns coordinates of pixel that approximates point of circle centered at (centerX, centerYAxis) and 
# of radius "radius", "theta" degrees away from normal
def pixelAt(theta, radius, centerXAxis, centerYAxis):
	y = centerYAxis + (radius * math.sin(math.radians(theta)))
	x = centerXAxis + (radius * math.cos(math.radians(theta)))
	return round(x), round(y)



# given a 2D numpy array representing an image, traces out the bottom half of a circle (unfilled) 
# with radius, "radius", centered at "center" and returns the image in array form.
# Note that the coordinate system used for center coordinates has origin at bottom left pixel of image. 
def traceBottomSemiCircleOnImage(imageArray, centerXAxis, centerYAxis, radius):

	imageHeight = imageArray.shape[0]
	thickness = round(imageHeight / 18)

	# vary radius so that our trace is visible on image (i.e thicken it)
	for r in range(radius, radius + thickness): 

		theta = 0

		while theta >= -180: 

			# get pixel in circle centered at (centerXAxis, centerYAxis) of radius, r, theta degrees
			# away from normal
			pixelX, pixelY = pixelAt(theta, r, centerXAxis, centerYAxis)

			# set corresponding pixel value in "imageArray" to 0
			imageHeight = imageArray.shape[0]
			rowIndex = (imageHeight - (pixelY + 1)) - 1
			columnIndex = pixelX

			imageArray[rowIndex][columnIndex] = 0

			theta = theta - 0.1

	return imageArray


def drawSmileyFace(imageArray): 

	# image dimensions
	imageHeight = imageArray.shape[0]
	imageWidth = imageArray.shape[1]

	# calculate mouth radius and center coordinates
	centerMouthXCoord = int(imageWidth / 2)
	centerMouthYCoord = int(imageHeight / 2)

	radiusMouth = int(min(imageHeight / 4, imageWidth / 4))

	# draw mouth
	traceBottomSemiCircleOnImage(imageArray, centerMouthXCoord, centerMouthYCoord, radiusMouth)

	# calculate eye dimensions and center coordinates
	heightEye = int(radiusMouth / 2)
	widthEye = int(radiusMouth / 6)
	centerRightEyeYCoord = centerMouthYCoord
	centerRightEyeXCoord = centerMouthXCoord + int(radiusMouth / 2)
	centerLeftEyeYCoord = centerRightEyeYCoord
	centerLeftEyeXCoord = centerMouthXCoord - int(radiusMouth / 2)

	# draw them!
	drawRectangleOnImage(imageArray, centerRightEyeXCoord, centerRightEyeYCoord, heightEye, widthEye)
	drawRectangleOnImage(imageArray, centerLeftEyeXCoord, centerLeftEyeYCoord, heightEye, widthEye)

	return imageArray


# takes in an .pgm image filename from command line "overlays a smiley face" on this image and writes this new
# image as 'modified.pgm'
def main():


	# get image filename from command line
	imageFilename = sys.argv[1]	

	# read pgm image as an array (numpy)
	imageArray = imageio.imread(imageFilename)

	# draw in smiley face
	modifiedImageArray = drawSmileyFace(imageArray)

	# save image as modifiedImage.pgm
	imageio.imwrite("modifiedImage.jpg", modifiedImageArray)




	return


main() 

