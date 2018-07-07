import cv2
frame = cv2.imread('ret_image.jpg')
cv2.namedWindow('showimage')
cv2.imshow('name', frame)

key=cv2.waitKey(0)
if key == ord("q"):
    cv2.destroyAllWindows()