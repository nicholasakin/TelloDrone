import pygame
import cv2
from djitellopy import Tello
import threading

# Initialize pygame window
def init():
    pygame.init()
    pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Tello Keyboard + Camera Control")

# Key mappings to Tello commands
KEY_COMMANDS = {
    pygame.K_q: "quit",
    pygame.K_t: "takeoff",
    pygame.K_l: "land",
    pygame.K_UP: ("move_forward", 30),
    pygame.K_DOWN: ("move_back", 30),
    pygame.K_LEFT: ("move_left", 30),
    pygame.K_RIGHT: ("move_right", 30),
    pygame.K_w: ("move_up", 30),
    pygame.K_s: ("move_down", 30),
    pygame.K_a: ("rotate_counter_clockwise", 30),
    pygame.K_d: ("rotate_clockwise", 30),
}

# Thread function for camera feed
def camera_stream(frame_read, stop_flag):
    while not stop_flag["stop"]:
        frame = frame_read.frame
        frame = cv2.resize(frame, (720, 480))
        cv2.imshow("Tello Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_flag["stop"] = True
            break

    cv2.destroyAllWindows()

def main():
    init()
    tello = Tello()
    tello.connect()
    print("Battery:", tello.get_battery(), "%")

    tello.streamon()
    frame_read = tello.get_frame_read()

    # Control flag to stop both threads
    stop_flag = {"stop": False}

    # Start video stream in a thread
    cam_thread = threading.Thread(target=camera_stream, args=(frame_read, stop_flag))
    cam_thread.start()

    try:
        while not stop_flag["stop"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_flag["stop"] = True

                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == pygame.K_ESCAPE or key == pygame.K_q:
                        stop_flag["stop"] = True
                    elif key in KEY_COMMANDS:
                        command = KEY_COMMANDS[key]
                        if isinstance(command, str):
                            getattr(tello, command)()
                        else:
                            action, value = command
                            getattr(tello, action)(value)

    finally:
        stop_flag["stop"] = True
        cam_thread.join()
        tello.streamoff()
        tello.end()
        pygame.quit()
        print("Exited cleanly.")

if __name__ == "__main__":
    main()
