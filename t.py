import pygame as gm
import time
import numpy as np

gm.init()
width, height = 400, 400
bg = 25, 25, 25
screen = gm.display.set_mode((height, width))
screen.fill(bg)

nCx, nCy = 60, 60
Cstate = np.zeros((nCx, nCy))
tamnCx = width / nCx
tamnCy = height / nCy

initial_cells = [(38, 20), (39, 20), (40, 20),
                  (10, 5), (12, 5), (11, 6), (12, 6), (11, 7),
                  (5, 10), (5, 12), (6, 11), (6, 12), (7, 11),
                  (18, 15), (17, 16), (17, 15), (18, 16),
                  (30, 20), (31, 20), (32, 20), (32, 19), (33, 19), (34, 19)]

for cell in initial_cells:
    Cstate[cell] = 1

pausa = False

while True:
    newCstate = np.copy(Cstate)

    time.sleep(0.1)
    screen.fill(bg)
    ev = gm.event.get()

    for evento in ev:
        if evento.type == gm.KEYDOWN:
            pausa = not pausa

        click = gm.mouse.get_pressed()

        if any(click):
            posX, posY = gm.mouse.get_pos()
            celX, celY = int(np.floor(posX / tamnCx)), int(np.floor(posY / tamnCy))
            newCstate[celX, celY] = 1

    for y in range(0, nCx):
        for x in range(0, nCy):
            if not pausa:
                vecinos = (
                    Cstate[(x - 1) % nCx, (y - 1) % nCy] +
                    Cstate[(x) % nCx, (y - 1) % nCy] +
                    Cstate[(x + 1) % nCx, (y - 1) % nCy] +
                    Cstate[(x - 1) % nCx, (y) % nCy] +
                    Cstate[(x + 1) % nCx, (y) % nCy] +
                    Cstate[(x - 1) % nCx, (y + 1) % nCy] +
                    Cstate[(x) % nCx, (y + 1) % nCy] +
                    Cstate[(x + 1) % nCx, (y + 1) % nCy]
                )

                if Cstate[x, y] == 0 and vecinos == 3:
                    newCstate[x, y] = 1

                elif Cstate[x, y] == 1 and not (2 <= vecinos <= 3):
                    newCstate[x, y] = 0

            poly = [((x) * tamnCx, y * tamnCy),
                    ((x + 1) * tamnCx, y * tamnCy),
                    ((x + 1) * tamnCx, (y + 1) * tamnCy),
                    ((x) * tamnCx, (y + 1) * tamnCy)]

            color = (40, 40, 40) if newCstate[x, y] == 0 else (200, 100, 100)
            gm.draw.polygon(screen, color, poly)

    Cstate = np.copy(newCstate)
    gm.display.flip()
