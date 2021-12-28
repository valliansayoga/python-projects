import cv2, time

frame_count = 0
time_start = time.time()
video = cv2.VideoCapture(0)
# cv2.VideoCapture() bisa diisi tergantung banyaknya kamera dalam index (dalam hal ini webcam lepi hanya ada 1, jadi diisi 0) atau nama file "video.mp4"
# (0, cv2.CAP_DSHOW) solusi dari internet
while True:
    frame_count += 1
    check, frame = video.read()  # Tanpa while loop, frame hanya capture 1st frame
    # print (check)
    # print (frame)
    # time.sleep(3); Memperlama proses loop
    cv2.imshow("Capturing", frame)

    # cv2.waitKey(0); Loop stop setelah keyboard diteken
    key = cv2.waitKey(1)  # Solusi
    if key == ord("q"):  # Mengganti value cv2.waitkey(0) jadi "q" (?)
        break

time_stop = time.time()
video.release()
cv2.destroyAllWindows
print("Recorded for:", frame_count, "frames")
print("Duration:", round(time_stop - time_start, 2), "second(s)")  # Mengukur waktu
