import cv2

img = cv2.imread("galaxy.jpg", 0)  # 0 = grayscale, 1 = BGR, -1 = include transparency

resized = cv2.resize(
    img, (int(img.shape[1] / 2), int(img.shape[0] / 2))
)  # cv2.resize(object, (width, height)). Resized by 50% ratio
print(type(img))  # Tipenya adalah numpy array
print(img)
print(img.shape)  # Banyak pixel di Y-axis dan X-axis
print(img.ndim)  # Banyak dimensi

cv2.imshow(
    "Galaxy", resized
)  # (Window's name, object). Image depends on color mode in line 3
cv2.imwrite("Galaxy_resized_half.jpg", resized)  # (Name, object)
cv2.waitKey(
    0
)  # in milisecond. 0 = user input keyboard akan run next line, 1++ sesuai waktu
cv2.destroyAllWindows()
