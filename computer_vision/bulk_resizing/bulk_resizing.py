# Works well if in the same directory

import cv2
import glob

images = glob.glob(
    "*.jpg",
)  # glob.glob membuat list path berdasarkan pola di directorynya(?);
print(images)
for image in images:
    img = cv2.imread(image, 0)
    re = cv2.resize(img, (100, 100))
    cv2.imshow("Hey", re)
    cv2.waitKey(500)
    cv2.destroyAllWindows()
    cv2.imwrite(
        "res_" + image, re
    )  # 'image' di sini maksudnya nama file yang diwakilkan variable di 'for' loop-nya

# SCRIPT BARU BISA KERJA BENER KALO DAH DI 'CD' KE FOLDER TEMPAT SCRIPT
# cd bulk_resizing lalu run
