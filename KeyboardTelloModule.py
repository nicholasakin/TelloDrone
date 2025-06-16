import pygame

def init():
    pygame.init()
    windows = pygame.display.set_mode((640, 480))
    # pygame.joystick.init()
    # if pygame.joystick.get_count() == 0:
    #     print("No joystick found.")
    #     return None
    # joystick = pygame.joystick.Joystick(0)
    # joystick.init()
    # return joystick

if __name__ == "__main__":
    init()
    print("KeyboardTelloModule initialized.")
    # You can add more functionality here, such as handling keyboard events.
    # For example, you could use pygame.event.get() to check for key presses.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                print(f"Key pressed: {pygame.key.name(event.key)}")