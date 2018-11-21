
_version_ = "2"

import pygame, math, os, sys, time
from pygame.locals import *
pygame.init()
pygame.display.set_caption("Autonomous")







class Point():
    # takes an x value and a y value from the Alliance Station. The field is vertical.
    def __init__(self, x, y, speed=0):
        self.x = x
        self.y = y
        self.speed = speed

    # takes point as argument, returns angle to turn from 0.
    def getAngle(self, point):
        angle = 0
        if ((point.x - self.x >= 0) and (point.y - self.y <= 0)):
            angle = -90 - \
                math.degrees(math.atan2(
                    (self.y - point.y), (self.x - point.x)))
        if ((point.x - self.x <= 0) and (point.y - self.y >= 0)):
            angle = 180 + \
                (90 - (math.degrees(math.atan2((self.y - point.y), (self.x - point.x)))))
        if ((point.x - self.x >= 0) and (point.y - self.y >= 0)):
            angle = -90 - \
                math.degrees(math.atan2(
                    (self.y - point.y), (self.x - point.x)))
        if ((point.x - self.x <= 0) and (point.y - self.y <= 0)):
            angle = 180 + \
                (90 - (math.degrees(math.atan2((self.y - point.y), (self.x - point.x)))))

        if angle > 360:
            angle += -360
        if angle < 0:
            angle += 360

        if point.x < self.x:
            angle = -angle

        if angle < 0:
            angle = -360 - angle

        return angle

    def getDistance(self, point):
        return (
            ((self.y - point.y)**2) + ((self.x - point.x)**2)
        ) ** 0.5

    def getSpeed(self):
        return self.speed







# Distance Traveled == (leftSpeed + rightSpeed)/2 * time
class Line():
    def __init__(self):
        self.listOfPoints = []

    def addPoint(self, x, y, speed=0):
        self.listOfPoints.append(
            Point(x, y, speed)
        )

    def eatPoint(self):
        if len(self.listOfPoints) > 0:
            self.listOfPoints = self.listOfPoints[1:]

    def nextPoint(self):
        return self.listOfPoints[1]

    def thisPoint(self):
        return self.listOfPoints[0]


class Path(Line):
    # def __init__(self, token_x, token_y):
    def __init__(self):
        super().__init__()

        self.speed = 0
        self.setSpeed(1)

        # self.token = Point(token_x, token_y)

    def setSpeed(self, speed):
        # sets speed of the robot in feet per second
        self.speed = speed

    def getSpeed(self):
        return self.speed

    def timeToNextPoint(self):
        return self.thisPoint().getDistance(
            self.nextPoint()
        ) / self.getSpeed()

    def currentGyro(self):
        return self.thisPoint().getAngle(
            self.nextPoint()
        )

    def currentDistance(self):
        return self.thisPoint().getDistance(
            self.nextPoint()
        )

    def currentSpeed(self):
        return self.thisPoint().getSpeed()

    def reset(self):
        self.listOfPoints = []




class Field():
    def __init__(self, image):
        self.image = pygame.image.load(
                        os.path.join(
                                os.path.dirname(sys.argv[0]),
                                image)
                                )
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height

    def pixelCoordinatesToFeet(self, x, y):
        return ((y / self.height) * (323.38 / 12)), ((x / self.width) * 54)

    def mouseCoordinatesToFeet(self, pos):
        return ((pos[1] / self.height) * (323.38 / 12)), ((pos[0] / self.width) * 54)

    def feetCoordinatesToPixels(self, pos):
        return ((pos[1] / 27) * self.height), ((pos[0] / 54) * self.width)

    def draw(self, display):
        display.blit(self.image, (0,0))




# class GraphicalPoint()
class GraphicalCircle():
    def __init__(self, color, position, radius, width):
        self.color = color
        self.position = position
        self.radius = radius
        self.width = width

    def draw(self, display):
        pygame.draw.circle(display,
                           self.color,
                           self.position,
                           self.radius,
                           self.width
                            )






class GraphicalLine():
    def __init__(self, color, initialPosition, finalPosition, width):
        self.color = color
        self.initialPosition = initialPosition
        self.finalPosition = finalPosition
        self.width = width

    def draw(self, display):
        pygame.draw.line(display,
                           self.color,
                           self.initialPosition,
                           self.finalPosition,
                           self.width
                            )


class GraphicalChassis():
    def __init__(self):
        self.pos = (0,0)

    def move(self, pos):
        self.pos = pos

    def draw(self, display):
        pygame.draw.circle(
            display,
            (255,0,0),
            self.pos,
            22,
            1
            )







class App():
    def __init__(self):

        self.field = Field('resources/field.png')
        self.width = self.field.width
        self.height = self.field.height
        DEPTH = 32
        DISPLAY = (self.width, self.height)
        FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.display = pygame.display.set_mode(DISPLAY,FLAGS, DEPTH)
        self.display.fill((255, 255, 255))

        self.path = Path()
        self.path.setSpeed(6)

        self.chassis = GraphicalChassis()

        self.drawnObjects = [self.field, self.chassis]

        self.pressed = False
        self.eventLoop()


    def clearDrawnObjects(self):
        self.drawnObjects = [self.field, self.chassis]

    def eventLoop(self):

        startingY = self.height / 2
        startingX = 21.783
        settingStartPosition = True

        lastMousePos = (0,0)
        buildingPath = True

        while buildingPath:


            while settingStartPosition:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)

                    # if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    #     startingY += 3.2675
                    #
                    # if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    #     startingY -= 3.2675
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                        startingY += 3.2675 * 2

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        startingY -= 3.2675 * 2

                    if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                        print("\n\n" + "-"*3 + "STARTING POS" + "-"*3)
                        print("FEET FROM LEFT WALL: " + str((startingY / self.height) * (323.38 / 12)))
                        print("FEET FROM RIGHT WALL: " + str(27 - (startingY / self.height) * (323.38 / 12)))
                        print("-"*20)

                        self.drawnObjects.append(
                            GraphicalCircle((255,255,255), (int(startingX), int(startingY)), 10, 3)
                        )

                        self.path.addPoint(
                            self.field.mouseCoordinatesToFeet((int(startingX), int(startingY)))[0],
                            self.field.mouseCoordinatesToFeet((int(startingX), int(startingY)))[1],
                            self.path.getSpeed()
                        )

                        offset = 20

                        self.drawnObjects.append(
                            GraphicalLine((255,255,255), (int(startingX), int(startingY)), (int(startingX)+offset, int(startingY)), 3)
                            )

                        self.drawnObjects.append(
                            GraphicalCircle((255,255,255), (int(startingX+offset), int(startingY)), 10, 3)
                        )

                        self.path.addPoint(
                            self.field.mouseCoordinatesToFeet((int(startingX+offset), int(startingY)))[0],
                            self.field.mouseCoordinatesToFeet((int(startingX+offset), int(startingY)))[1],
                            self.path.getSpeed()
                        )

                        lastMousePos = (startingX+offset, startingY)
                        settingStartPosition = False

                self.chassis.move((int(startingX), int(startingY)))

                for image in self.drawnObjects:
                    image.draw(self.display)

                pygame.display.update()


            self.chassis.move(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                    # buildingPath = False
                    # os.system("clear")
                    self.generateAutoCode()
                    lookingAtPath = True
                    while lookingAtPath:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                                self.clearDrawnObjects()
                                self.path.reset()
                                lookingAtPath = False
                                settingStartPosition = True
                                print("\n\n" + "-"*15 + "RESET" + "-"*15 + "\n\n")



            if pygame.mouse.get_pressed()[0]:
                if not self.pressed:
                    self.pressed = True
                    # print("COORDS IN FEET: " + str(self.field.mouseCoordinatesToFeet(pygame.mouse.get_pos())))

                    if len(self.path.listOfPoints) > 0:
                        self.drawnObjects.append(
                            GraphicalLine((255,255,255), lastMousePos, pygame.mouse.get_pos(), 3)
                            )

                    self.drawnObjects.append(
                        GraphicalCircle((255,255,255), pygame.mouse.get_pos(), 10, 3)
                        )

                    lastMousePos = pygame.mouse.get_pos()
                    self.path.addPoint(
                        self.field.mouseCoordinatesToFeet(pygame.mouse.get_pos())[0],
                        self.field.mouseCoordinatesToFeet(pygame.mouse.get_pos())[1],
                        self.path.getSpeed()
                        )

            else:
                self.pressed = False

            for image in self.drawnObjects:
                image.draw(self.display)

            pygame.display.update()


    def generateAutoCode(self):
        instructionsForAuto = ""

        for i in range(0, len(self.path.listOfPoints) - 1):
            print(
                "DRIVE FOR THIS LONG: " + str(self.path.timeToNextPoint()) + '\n' +
                "AT THIS ANGLE: " + str(self.path.currentGyro()) + '\n' +
                "AT THIS SPEED: " + str(self.path.currentSpeed())
            )

            # instructionsForAuto += "autoDrive(" + str(self.path.timeToNextPoint()) + ', ' + str(self.path.currentGyro()) + ', ' + str(self.path.currentSpeed()) + ")\n"
            instructionsForAuto += "autoDrive(" + str(self.path.currentGyro()) + ', ' + str(self.path.currentDistance()*12) + ")\n"

            self.path.eatPoint()
            print("-" * 20)

        print("\n\n" + "-"*3 + "GENERATED CODE" + "-"*3)
        print(instructionsForAuto)


if __name__ == "__main__":
    App()
