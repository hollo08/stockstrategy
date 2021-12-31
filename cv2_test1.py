# import cv2
#
# src = cv2.imread("G:/cv2/test1/test1.jpg")
# gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
# cv2.namedWindow("input", cv2.WINDOW_AUTOSIZE)
# cv2.imshow("input", src)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import numpy as np
import cv2
import matplotlib.pyplot as plt



trainData = np.random.randint(0,100,(25,2)).astype(np.float32)

#print(trainData)


responses = np.random.randint(0,2,(25,1)).astype(np.float32)


red = trainData[responses.ravel()==0]

#print(trainData)

#print(responses.ravel())

#print(red)

plt.scatter(red[:,0],red[:,1],80,'r','^')


#Take Blue families and plot them

blue = trainData[responses.ravel()==1]

plt.scatter(blue[:,0],blue[:,1],80,'b','s')


#plt.show()

newcomer = np.random.randint(0, 100, (1, 2)).astype(np.float32)

plt.scatter(newcomer[:, 0], newcomer[:, 1], 80, 'g', 'o')

knn = cv2.ml.KNearest_create()

knn.train(trainData, cv2.ml.ROW_SAMPLE, responses)

ret, results, neighbours, dist = knn.findNearest(newcomer, 3)

print("result: ", results,"\n")

print("neighbours: ", neighbours,"\n")

print("distance: ", dist)

plt.show()
