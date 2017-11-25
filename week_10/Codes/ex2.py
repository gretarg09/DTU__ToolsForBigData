import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np

def getHashLshAlgorithm(img):
    # Resize to 9x8 pixels
    img = cv2.resize(img,(9,8))

    # Compare adjacent values (x>y)
    img_compared = np.empty((8,8))
    for i,row in enumerate(img):
        for j,column in enumerate(row):
            # the resulting matrix has one fewer columns
            # as we are compeering values
            if j + 1 == len(row):
                break
            else:
                img_compared[i][j] = row[j] > row[j+1]

    # use the hash function from David (given on Aula)
    hash_string = ""
    for difference in img_compared:
        decimal_value = 0
        hex_string = []
        for index, value in enumerate(difference):
            if value:
                decimal_value += 2**(index % 8)
            if (index % 8) == 7:
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value = 0
        hash_string = hash_string +''.join(hex_string) + ' ' 
    return hash_string





if __name__ == '__main__':

    filenames = ['../cat.png', '../cat_mod.png','../cat_mod_more.png','../cat_orange.png']
    
    for name in filenames:
        print "The hash for the figure {}:".format(name)
        print getHashLshAlgorithm(cv2.imread(name, cv2.IMREAD_GRAYSCALE))
