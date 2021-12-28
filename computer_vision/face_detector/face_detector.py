import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

img = cv2.imread("photo.jpg")  # Kalau tanpa parameter defaultnya adalah full color mode
gray_img = cv2.cvtColor(
    img, cv2.COLOR_BGR2GRAY
)  # Face detector berakurasi tinggi kalau di grayscale

faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.05, minNeighbors=5)
# Scale factor bila semakin mendekati 1 semakin akurat (dan lama)
# minNeighbors (how many neighbors around the window) bisa dicoba sendiri, tapi "5" generally good
# faces menjadi variable numpy array ndimension dengan list berisi [x, y, w, h]
# Ubah nilai scalefactor bila cv2 detect yang tidak masuk akal

for x, y, w, h in faces:
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 3)
    # cv2.rectangle (image, point pojok kiri atas, point pojok kanan bawah, warna kotak, line thickness)

# Bila gambar tidak muat bisa diresize dulu
# resized = cv2.resize(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)))
# cv2.imshow("Resized and rectangled", resized)

cv2.imshow("Converted to Gray", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
