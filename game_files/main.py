from random import randint
from pygame import *

font.init()

class Plane():
    def __init__(self, x, y, w, h, img):
        self.rect = rect.Rect(x, y, w, h)
        self.img = transform.scale(image.load(img), (w, h))
    def showairplane(self):
        w.blit(self.img, (self.rect.x, self.rect.y))
    def move(self):
        global speedx
        global speedy
        global altitude
        global close
        global planeinrunway1
        global planeinrunway2
        altitude = 750 - player.rect.y
        keys = key.get_pressed()
        if (keys[K_d] or keys[K_RIGHT] or autopilot) and speedx < 1002:
            speedx += 2
        if (keys[K_a] or keys[K_LEFT]) and speedx > 10 and (not autopilot):
            for i in runways:
                if self.rect.colliderect(i):
                    speedx -= 6
            else:
                speedx -= 3
            if speedx < 10:
                speedx = 0
        if keys[K_w] or keys[K_UP]:
            if not (altitude < 110 and speedx < 300):
                speedy += 0.1
        if keys[K_s] or keys[K_DOWN]:
            speedy -= 0.1
        if autopilot:
            speedy = 0
        if speedx > 0:
            speedx -= 0.1
        counterlocal = 1
        for i in runways:
            i.x -= speedx
            if self.rect.colliderect(i) and speedy < -5:
                close = True
            if self.rect.colliderect(i) and counterlocal == 1:
                planeinrunway1 = True
            elif (not self.rect.colliderect(i)) and counterlocal == 1:
                planeinrunway1 = False
            if self.rect.colliderect(i) and counterlocal == 2:
                planeinrunway2 = True
            elif (not self.rect.colliderect(i)) and counterlocal == 2:
                planeinrunway2 = False
            counterlocal += 1
        if not (planeinrunway1 or planeinrunway2) and speedx < 100:
            speedy = -5
            w.blit(font.SysFont('Arial', 100).render("STALL", True, (0, 0, 0)), (100, 100))
        speedx = round(speedx, 1)
        speedy = round(speedy, 1)
        if ((planeinrunway1 or planeinrunway2) != True) or altitude > 101.0:
            self.rect.y -= speedy
        if altitude < 50:
            close = True

closeall = False
while closeall != True:
    w = display.set_mode((1500, 750))
    display.set_caption("Flight simulator 2D")
    player = Plane(100, 650, 187, 100, "airplane_img.png")
    clock = time.Clock()
    close = False
    runway = rect.Rect(0, 700, 100000, 50)
    runway2 = rect.Rect(10000000, 700, 100000, 50)
    runways = [runway, runway2]
    buildings = []
    colours = []
    for i in range(10000):
        height = randint(50, 200)
        buildings.append(rect.Rect((randint(120000, (10000000 - 20000))), (750 - height), randint(50, 100), height))
        colour = randint(50, 150)
        colours.append((colour, colour, colour))
    pause = False
    distancetorunway = round(runway2.x - (player.rect.x + 100), 1)
    speedx = 0
    speedy = 0
    autopilot = False
    planeinrunway1 = False
    timevar = 0
    planeinrunway2 = False
    win = False
    while not close:
        w.fill((100, 100, 255))
        for i in event.get():
            if i.type == QUIT:
                close = True
                closeall = True
            if i.type == KEYDOWN:
                if i.key == K_1:
                    if pause:
                        pause = False
                    else:
                        pause = True
                if i.key == K_e:
                    if autopilot:
                        autopilot = False
                    else:
                        autopilot = True
        if closeall:
            close = True
        for i in runways:
            draw.rect(w, (100, 100, 100), i)
            if player.rect.colliderect(i):
                autopilot = False
        player.showairplane()
        if not pause:
            player.move()
        else:
            w.blit(font.SysFont('Arial', 60).render("Game paused", True, (0, 0, 0)), (100, 100))
        w.blit(font.SysFont('Arial', 30).render('speed: ' + str(speedx) + "km/h", True, (0, 0, 0)), (1000, 100))
        w.blit(font.SysFont('Arial', 30).render('climb: ' + str(speedy) + "deg", True, (0, 0, 0)), (1000, 140))
        w.blit(font.SysFont('Arial', 30).render('altitude: ' + str(altitude) + "m", True, (0, 0, 0)), (1000, 180))
        w.blit(font.SysFont('Arial', 30).render('distance to runway: ' + str(distancetorunway) + "m", True, (0, 0, 0)), (1000, 220))
        if autopilot:
            w.blit(font.SysFont('Arial', 30).render("Autopilot: ON", True, (0, 0, 0)), (1000, 260))
        else:
            w.blit(font.SysFont('Arial', 30).render("Autopilot: OFF", True, (0, 0, 0)), (1000, 260))
        distancetorunway = round(runway2.x - (player.rect.x + 100), 1)
        if player.rect.colliderect(runway2) and speedx == 0:
            close = True
            win = True
        timevar += 1
        counter = 0
        for i in buildings:
            draw.rect(w, colours[counter], i)
            if not pause:
                i.x -= speedx
            if player.rect.colliderect(i):
                close = True
            counter += 1
        display.update()
        clock.tick(60)
    close = False
    timevar /= 3600
    while close != True:
        w.fill((100, 100, 255))
        for i in event.get():
            if i.type == QUIT:
                close = True
                closeall = True
            if i.type == KEYDOWN:
                if i.key == K_1:
                    close = True
        if closeall:
            close = True
        if win:
            w.blit(font.SysFont('Arial', 30).render("You win! Time: " + str(timevar) +"minutes (1-try again)", True, (0, 0, 0)), (50, 130))
        else:
            w.blit(font.SysFont('Arial', 30).render("Crash! (1-try again)", True, (0, 0, 0)), (50, 130))
        display.update()
        clock.tick(60)