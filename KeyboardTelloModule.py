import pygame
from djitellopy import Tello

# Initialize pygame and window
def init():
    pygame.init()
    pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Tello Keyboard Control")

# Key mappings
KEY_COMMANDS = {
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

# Main control loop
def main():
    init()
    tello = Tello()
    tello.connect()
    print("Battery:", tello.get_battery(), "%")
    print("KeyboardTelloModule initialized.")

    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == pygame.K_ESCAPE:
                        running = False

                    elif key in KEY_COMMANDS:
                        command = KEY_COMMANDS[key]
                        if isinstance(command, str):
                            getattr(tello, command)()
                        else:
                            action, value = command
                            getattr(tello, action)(value)

    finally:
        print("Exiting and releasing Tello resources.")
        tello.end()
        pygame.quit()

if __name__ == "__main__":
    main()
