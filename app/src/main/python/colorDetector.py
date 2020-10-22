#https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
#https://realpython.com/python-opencv-color-spaces/
import cv2
import numpy as np
from skimage import io
from PIL import Image
import math


#Colour Conversion Tools------------------------------------------------------------------------------------------------
def colourranking(Ls,As,Bs):



    #Manually Enter In Colour LAB---------------------------------------------------------------------------------------
    Lb1, Ab1, Bb1 = 60.8081,-22.8923,52.2434
    Lb2, Ab2, Bb2 = 64.8841,-14.7152,53.7066
    Lb3, Ab3, Bb3 = 56.298,-3.4002,42.8545
    Lb4, Ab4, Bb4 = 58.7974,0.5304,44.8976
    Lb5, Ab5, Bb5 = 59.7416,6.3574,42.1835
    Lb6, Ab6, Bb6 = 59.5708,10.6589,45.616
    Lb7, Ab7, Bb7 = 57.968,26.1983,44.4026
    Lb8, Ab8, Bb8 = 60.6354,27.4197,43.1853
    Lb9, Ab9, Bb9 = 54.8862,40.1025,41.511
    Lb10, Ab10, Bb10 = 58.3059,47.9044,43.6169

    #Creates Delta Calcs For Each Colour--------------------------------------------------------------------------------
    Delta1 = math.sqrt(((Ls - Lb1) ** 2) + ((As - Ab1) ** 2) + ((Bs - Bb1) ** 2))
    Delta2 = math.sqrt(((Ls - Lb2) ** 2) + ((As - Ab2) ** 2) + ((Bs - Bb2) ** 2))
    Delta3 = math.sqrt(((Ls - Lb3) ** 2) + ((As - Ab3) ** 2) + ((Bs - Bb3) ** 2))
    Delta4 = math.sqrt(((Ls - Lb4) ** 2) + ((As - Ab4) ** 2) + ((Bs - Bb4) ** 2))
    Delta5 = math.sqrt(((Ls - Lb5) ** 2) + ((As - Ab5) ** 2) + ((Bs - Bb5) ** 2))
    Delta6 = math.sqrt(((Ls - Lb6) ** 2) + ((As - Ab6) ** 2) + ((Bs - Bb6) ** 2))
    Delta7 = math.sqrt(((Ls - Lb7) ** 2) + ((As - Ab7) ** 2) + ((Bs - Bb7) ** 2))
    Delta8 = math.sqrt(((Ls - Lb8) ** 2) + ((As - Ab8) ** 2) + ((Bs - Bb8) ** 2))
    Delta9 = math.sqrt(((Ls - Lb9) ** 2) + ((As - Ab9) ** 2) + ((Bs - Bb9) ** 2))
    Delta10 = math.sqrt(((Ls - Lb10) ** 2) + ((As - Ab10) ** 2) + ((Bs - Bb10) ** 2))

    #Creates Dictonary--------------------------------------------------------------------------------------------------
    ClosestColour = {'Colour-1':Delta1, 'Colour-2':Delta2, 'Colour-3':Delta3, 'Colour-4':Delta4, 'Colour-5':Delta5,
                     'Colour-6':Delta6, 'Colour-7':Delta7, 'Colour-8':Delta8,'Colour-9':Delta9,'Colour-10':Delta10}

    #Prints Results-----------------------------------------------------------------------------------------------------

    bestmatch =  str(min(ClosestColour, key=ClosestColour.get))
    closestdelta = str(min(ClosestColour.values()))
    print(bestmatch)
    print(closestdelta)



    return (bestmatch,closestdelta)

def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v
def rgb2lab ( inputColor ) :

    num = 0
    RGB = [0, 0, 0]

    for value in inputColor :
        value = float(value) / 255

        if value > 0.04045 :
            value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
        else :
            value = value / 12.92

        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0,]

    X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
    Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
    Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
    XYZ[ 0 ] = round( X, 4 )
    XYZ[ 1 ] = round( Y, 4 )
    XYZ[ 2 ] = round( Z, 4 )

    XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
    XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
    XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883

    num = 0
    for value in XYZ :

        if value > 0.008856 :
            value = value ** ( 0.3333333333333333 )
        else :
            value = ( 7.787 * value ) + ( 16 / 116 )

        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]

    L = ( 116 * XYZ[ 1 ] ) - 16
    a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
    b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )

    Lab [ 0 ] = round( L, 4 )
    Lab [ 1 ] = round( a, 4 )
    Lab [ 2 ] = round( b, 4 )

    return Lab


def processimage (ImageToProcess):

    print(ImageToProcess)

    cap = cv2.imread(ImageToProcess)
    frame = cap
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Colours to filter
    lower_red = np.array([0, 100, 0])
    upper_red = np.array([255, 255, 255])

    #Apply colour filter to image
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    print('Code 1 finished running')
    print('Loading...')
    imgname = ImageToProcess
    print(imgname)
    print('Loading...')
    #Variables--------------------------------------------------------------------------------------------------------------
    imglocation = ImageToProcess

    colourtoignore = [100,100,100]
    numberofcolourstoshow = 20


    #Read Images------------------------------------------------------------------------------------------------------------
    img = res


    #Count Colors-----------------------------------------------------------------------------------------------------------
    # colors = img2.convert('RGB').getcolors(maxcolors=1000000) #this converts the mode to RGB
    # print(len(colors))

    #Average Pixels (RGB)---------------------------------------------------------------------------------------------------


    #Finds black pixels
    notblack = []
    black = []
    for pixel in img:
     for colour in pixel:
        if np.all(colour < colourtoignore):
            black.append(colour)
            # print('Black')
        else:
            # print('Not Black')
            notblack.append(colour)


    averageignoredcolour = np.mean(notblack,axis=0) # Axis 0 will act on all the ROWS in each COLUM # Axis 1 will act on all the COLUMNS in each ROW

    average = img.mean(axis=0).mean(axis=0)


    #Most Dominant Pixels (RGB)---------------------------------------------------------------------------------------------
    pixels = np.float32(img.reshape(-1, 3))
    pixelstoignore = np.delete(pixels, np.where((pixels < colourtoignore).all(axis=1)), axis=0)

    # pixelstoignore = pixels[pixels != [[0,0,0]]] #Numpy Indexing!


    n_colors = numberofcolourstoshow #len(colors) #Change to top X
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixelstoignore, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]


    #Prints Average, Dominant and Top X RGB codes)--------------------------------------------------------------------------
    LABColours = rgb2lab(averageignoredcolour)
    HSVColours = rgb_to_hsv(averageignoredcolour[0],averageignoredcolour[1],averageignoredcolour[2])


    #Analysis colours to find closest match to Tomato Grade-----------------------------------------------------------------
   # sht.range('A'+str(rownumber)).value = imgname
   # sht.range('B'+str(rownumber)).value = LABColours
   # sht.range('E'+str(rownumber)).value = HSVColours
   # sht.range('H'+str(rownumber)).value = averageignoredcolour


    number1 = colourranking(LABColours[0],LABColours[1],LABColours[2]) #This is what we need returned
    number2 = str(averageignoredcolour[0])
    number3 = str(averageignoredcolour[1])
    number4 = str(averageignoredcolour[2])
    return (number1,number2,number3,number4)
    print('***********Done!***********')



#processimage (r'/storage/emulated/0/Pictures/background.jpg')