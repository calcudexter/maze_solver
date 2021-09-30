import cv2
import numpy as np

img = cv2.imread('worse-maze.jpeg', 0)
thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 199, 5)
ker = np.asarray([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype='uint8')
thresh = cv2.erode(thresh, ker, 2)
thresh = cv2.GaussianBlur(thresh, (3, 3), 0)
# thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 199, 0)
ret, thresh = cv2.threshold(thresh, 100, 255, cv2.THRESH_BINARY)
# thresh = cv2.dilate(thresh, ker, 1)

thresh = cv2.resize(thresh, (img.shape[1]//2,  img.shape[0]//2))
ret, thresh = cv2.threshold(thresh, 200, 255, cv2.THRESH_BINARY)
thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

thresh = cv2.copyMakeBorder(thresh, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[255, 0, 0])

thresh[thresh.shape[0]//2, thresh.shape[1]//2] = [0, 0, 255]

cv2.imwrite("processed_maze.png", thresh)

cv2.imshow("maze", thresh)
key = cv2.waitKey(0)
cv2.destroyAllWindows()