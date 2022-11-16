import keyboard
import pygame
import usb.core
import usb.util

VID = 0x0079 #0x18F8 mouse # 0079 dance pad
PID = 0x0011 #0x0F99 mouse # 0011 dance pad

device = usb.core.find(idVendor = VID, idProduct = PID)
if device is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
device.set_configuration()

# get an endpoint instance
config = device.get_active_configuration()
interface = config[(0,0)]

endpoint = usb.util.find_descriptor(
    interface,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_IN)

assert endpoint is not None

endpoint_address = endpoint.bEndpointAddress
packet_size = endpoint.wMaxPacketSize

# used for placing pygame window on top of all other windows
import win32gui
import win32con

def on_top(window):
    win32gui.SetWindowPos(window, win32con.HWND_TOPMOST,100,100,200,200,0)

if __name__ == '__main__':
    win = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Dance Dance Revolution')
    pygame.font.init()

    center = pygame.transform.scale(pygame.image.load('arrows/center.png'), (150, 150))

    up = pygame.transform.scale(pygame.image.load('arrows/up.png'), (150, 150))
    down = pygame.transform.scale(pygame.image.load('arrows/down.png'), (150, 150))
    left = pygame.transform.scale(pygame.image.load('arrows/left.png'), (150, 150))
    right = pygame.transform.scale(pygame.image.load('arrows/right.png'), (150, 150))
    
    up_left = pygame.transform.scale(pygame.image.load('arrows/up_left.png'), (150, 150))
    up_right = pygame.transform.scale(pygame.image.load('arrows/up_right.png'), (150, 150))
    down_left = pygame.transform.scale(pygame.image.load('arrows/down_left.png'), (150, 150))
    down_right = pygame.transform.scale(pygame.image.load('arrows/down_right.png'), (150, 150))

    pressed = 0
    def press(keys, debounce = 30):
        global pressed
        if pressed == 0:
            keyboard.press_and_release(keys)
            pressed = debounce

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        win.fill((255, 255, 255))

        on_top(pygame.display.get_wm_info()['window'])

        data = device.read(endpoint_address, packet_size)

        middle = format(data[4], '08b')
        arrows = format(data[5], '08b')
        other = format(data[6], '08b')

        if int(middle[0]) == 1:
            win.blit(center, (170, 170))
            press('space')

        if int(arrows[0]) == 1:
            win.blit(right, (330, 170))
            press('right')
        if int(arrows[1]) == 1:
            win.blit(up, (170, 10))
            press('up')
        if int(arrows[2]) == 1:
            win.blit(down, (170, 330))
            press('down')
        if int(arrows[3]) == 1:
            win.blit(left, (10, 170))
            press('left')

        if int(other[4]) == 1:
            win.blit(up_right, (330, 10))
            press(['up', 'right'])
        if int(other[5]) == 1:
            win.blit(up_left, (10, 10))
            press(['up', 'left'])
        if int(other[6]) == 1:
            win.blit(down_right, (330, 330))
            press(['down', 'right'])
        if int(other[7]) == 1:
            win.blit(down_left, (10, 330))
            press(['down', 'left'])

        if pressed > 0:
            pressed -= 1

        pygame.display.update()