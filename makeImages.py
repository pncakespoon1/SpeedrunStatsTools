import cv2

FPS = 30
FRAME_SKIP = FPS
dsize = (1920, 1080)
letter = "j"
resize_to_bt = False


def download_frames(file):
    cur_frame = 0
    video = cv2.VideoCapture(str(file))
    while video.isOpened():
        cur_frame += 1
        if not video.grab():
            break
        if cur_frame % FRAME_SKIP:
            continue

        _, frame = video.retrieve()
        frame = cv2.resize(frame, dsize)
        if resize_to_bt:
            frame = frame[200:880, 630:1290]
        cv2.imwrite("D:/ResetEfficiency/nn_images/unsorted_images" + "/frame" + letter + str(cur_frame) + ".png", frame)
        cv2.imshow('window', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


download_frames("D:/ResetEfficiency/vods/0023semperzz.mp4")
