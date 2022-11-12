import pygame
import usb.core
import usb.util
import numpy as np

VID = 0x0079 #0x18F8 mouse # 0079 dance pad
PID = 0x0011 #0x0F99 mouse # 0011 dance pad

dev = usb.core.find(idVendor = VID, idProduct = PID)
if dev is None:
    raise ValueError('Device not found')

#print(dev)

ep = dev[0].interfaces()[0].endpoints()[0]
i = dev[0].interfaces()[0].bInterfaceNumber

#dev.reset()

# This doesn't work on Windows
#if dev.is_kernel_driver_active(i):
#    dev.detach_kernel_driver(i)

dev.set_configuration()
eaddr = ep.bEndpointAddress
#print(eaddr)

'''for i in range(0):
    r = dev.read(eaddr, 8)
    center = format(r[4], '08b')
    arrows = format(r[5], '08b')
    other = format(r[6], '08b')
    print(center, arrows, other)'''

def button_released(previous, current):
    released = []
    for i in range(len(previous)):
        if previous[i] != current[i]:
            released.append(i)
    return released

class Memory():
    def __init__(self, n = 51):
        self.n = n
        self.grid = np.zeros((n, n))

class Interpreter():
    def __init__(self):
        self.memory = Memory()
        self.pointer = (int(self.memory.n/2), int(self.memory.n/2))

    def run(self, program):
        commands = [c for c in program]
        dict = {'←': (-1, 0), '↑': (0, -1), '→': (1, 0), '↓': (0, 1),
                '↖': (-1, -1), '↗': (1, -1), '↘': (1, 1), '↙': (-1, 1)}
        for command in commands:
            pass

print('←↑→↓↖↗↘↙')

if __name__ == '__main__':
    win = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Dance Dance Revolution')
    pygame.font.init()

    u = pygame.transform.scale(pygame.image.load('other/ddr/arrows/u.png'), (150, 150))
    d = pygame.transform.scale(pygame.image.load('other/ddr/arrows/d.png'), (150, 150))
    l = pygame.transform.scale(pygame.image.load('other/ddr/arrows/l.png'), (150, 150))
    r = pygame.transform.scale(pygame.image.load('other/ddr/arrows/r.png'), (150, 150))
    
    ul = pygame.transform.scale(pygame.image.load('other/ddr/arrows/ul.png'), (150, 150))
    ur = pygame.transform.scale(pygame.image.load('other/ddr/arrows/ur.png'), (150, 150))
    dl = pygame.transform.scale(pygame.image.load('other/ddr/arrows/dl.png'), (150, 150))
    dr = pygame.transform.scale(pygame.image.load('other/ddr/arrows/dr.png'), (150, 150))

    program = ''

    previous_arrows, previous_other = [], []
    current_arrows, current_other = [], []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        win.fill((255, 255, 255))

        read = dev.read(eaddr, 8)
        #print(read)
        center = format(read[4], '08b')
        arrows = format(read[5], '08b')
        other = format(read[6], '08b')

        previous_arrows = current_arrows
        previous_other = current_other
        current_arrows = arrows
        current_other = other

        for index in button_released(previous_arrows, current_arrows):
            c = ['←','↑','→','↓']
            program += c[index]
        print(program)

        if int(arrows[0]) == 1:
            win.blit(r, (330, 170))
        if int(arrows[1]) == 1:
            win.blit(u, (170, 10))
        if int(arrows[2]) == 1:
            win.blit(d, (170, 330))
        if int(arrows[3]) == 1:
            win.blit(l, (10, 170))

        if int(other[4]) == 1:
            win.blit(ur, (330, 10))
        if int(other[5]) == 1:
            win.blit(ul, (10, 10))
        if int(other[6]) == 1:
            win.blit(dr, (330, 330))
        if int(other[7]) == 1:
            win.blit(dl, (10, 330))

        pygame.display.update()