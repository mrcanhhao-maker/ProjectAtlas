import cv2
import time


def test_camera(index):
    print(f"Testing camera index {index}...")
    cap = cv2.VideoCapture(index)

    if not cap.isOpened():
        print(f"Camera {index}: cannot open")
        return False

    ok_count = 0

    for _ in range(20):
        ok, frame = cap.read()
        if ok and frame is not None:
            ok_count += 1
        time.sleep(0.03)

    cap.release()

    print(f"Camera {index}: {ok_count}/20 frames OK")
    return ok_count >= 10


def main():
    working = []

    for index in range(5):
        if test_camera(index):
            working.append(index)

    print("")
    print("Working cameras:", working)

    if working:
        print(f"Recommended camera index: {working[0]}")
    else:
        print("No working camera found")


if __name__ == "__main__":
    main()
