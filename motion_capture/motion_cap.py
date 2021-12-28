import cv2, pandas
from datetime import datetime

df = pandas.DataFrame(columns=["Start", "End"])
first_frame = None
status_list = [None, None]
times = []
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(
        gray, (21, 21), 0
    )  # Gaussian removes noises and inaccuracies
    # (object, (BLURRINESS PARAMETER), STANDARD DEVIATION) (21 and 0 are good numbers)
    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(
        first_frame, gray
    )  # Comparing first frame w/ grayscaled current frames

    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[
        1
    ]  # Threshold menghasilkan tuple dgn 2 values. THRESH_BINARY menggunakan value di index [1], metode lain ada yang pakai [0]
    # cv2.threshold(OBJECT, "INTENSITAS PIXEL DI ATAS ...", "MAKA AKAN DICONVERT JADI PIXEL VALUE...")
    thresh_frame = cv2.dilate(
        thresh_frame, None, iterations=2
    )  # Ga ada array untuk kernel jadinya None. Iteration semakin besar akan semakin smooth

    (cnts, _) = cv2.findContours(
        thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )  # To find contour. Ada metode lain untuk draw contour. Find contour store value ke tuples

    for contour in cnts:
        if cv2.contourArea(contour) < 500:  # Mendetek object dibawah area __ pixel
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    status_list.append(status)

    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Contour Frame", frame)

    key = cv2.waitKey(1)  # Script baru jalan kalau jadi "1"

    if key == ord("q"):
        if status == 1:
            times.append(datetime.now())
        break

# times.append(datetime.now())
print(times)

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i + 1]}, ignore_index=True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows
