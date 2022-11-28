import copy
import time

import numpy as np
from scipy import integrate
import pygame

DiffTime = 0

class color:
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)
    grantblue = (38, 115, 185)
    darkgray = (100, 100, 100)
    purple = (106, 50, 159)
    fistikgreen = (106, 168, 79)
class diffusion:
    def Diffuse(f, x, t, X: tuple, diffcoeff, N: int):
        a0 = integrate.quad(f, X[0], X[1])[0] / (X[1] - X[0])

        def a(n):
            return (2 / (X[1] - X[0])) * \
                   integrate.quad(lambda x: f(x) * np.cos((n * np.pi * (x - X[0])) / (X[1] - X[0])), X[0], X[1])[0]

        y = a0
        for i in range(1, N + 1):
            y += a(i) * np.exp(-((i * np.pi * diffcoeff / (X[1] - X[0])) ** 2 * t)) * np.cos(
                i * np.pi * ((x - X[0]) / (X[1] - X[0])))
        return y
    def DiffuseUpdate(f, screen, x, xBounds, diffcoeff, N):
        global DiffTime
        Curve1 = list(zip(x, diffusion.Diffuse(f, x, DiffTime, xBounds, diffcoeff, N)))
        Curve2 = list(zip(x, f(x)))
        pygame.draw.aalines(screen, color.grantblue, closed=False, points=Curve1)
        pygame.draw.aalines(screen, color.white, closed=False, points=Curve2)
        DiffTime += 1
def PolynomialInterpolation(t, Points):
    x = [i[0] for i in Points]
    y = [i[1] for i in Points]
    n = len(Points)
    # Part 1
    M = np.array([])
    for i in range(n):
        M = np.append(M,y[i])
        for j in range(n):
            M = np.append(M,x[i] ** j)
    M.resize((n,n+1))
    # Part 2
    Coeff = np.zeros(n+1)
    Coeff[0] = np.linalg.det(np.delete(M,0,axis=1))
    for i in range(1,n+1):
        Coeff[i] = ((-1)**((i-1)%2)) * np.linalg.det(np.delete(M,i,axis=1)) / Coeff[0]
    Y = 0
    for i in range(n):
        Y += Coeff[i+1] * (t**i)
    return Y

PointList = []
mainClock = pygame.time.Clock()

def main():
    global PointList, DiffTime

    # Window
    pygame.init()
    WIDTH = 800
    HEIGHT = 600
    SIZE = (WIDTH, HEIGHT)
    window = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Diffusion sim")
    window.fill(color.black)

    xBounds = (0, WIDTH - 1)
    x = np.linspace(*xBounds, WIDTH // 2)

    PointsAtMoment = 0
    ToDiffuse = False

    def AppendPointList():
        global PointList
        pos = pygame.mouse.get_pos()
        PointList.append(pos)
    # start = time.time()
    ClearButtonWidth = 150
    ClearButtonHeight = 75
    ResetButtonWidth = 150
    ResetButtonHeight = 75
    # end = time.time()
    # print(end-start)
    def DrawClearButton():
        pygame.draw.rect(window, color.fistikgreen,
                         (WIDTH - ClearButtonWidth, HEIGHT - ClearButtonHeight, ClearButtonWidth, ClearButtonHeight))
    def DrawResetButton():
        pygame.draw.rect(window, color.grantblue, (0, HEIGHT - ResetButtonHeight, ResetButtonWidth, ResetButtonHeight))

    def parabola(x):
        return HEIGHT * x * (WIDTH - x) / ((WIDTH // 2) ** 2)

    def FuncToDraw(x):
        return PolynomialInterpolation(x, CurrentPoints)

    def f(x):
        return HEIGHT * x * (WIDTH - x) * x / (500 * (WIDTH // 2) ** 2)

    alpha = 30
    # Diffusion coefficient

    # Number of cosines added (more detail = more lag)
    n = 10

    # lööp
    running = True
    while running:
        window.fill(color.black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Buttons
            OnClearButton = pygame.mouse.get_pos()[0] > WIDTH - ClearButtonWidth and pygame.mouse.get_pos()[
                1] > HEIGHT - ClearButtonHeight
            OnResetButton = pygame.mouse.get_pos()[0] < ClearButtonWidth and pygame.mouse.get_pos()[
                1] > HEIGHT - ClearButtonHeight
            if event.type == pygame.MOUSEBUTTONUP:
                if not (OnClearButton or OnResetButton):
                    AppendPointList()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OnClearButton:
                    DiffTime = 0
                    if PointsAtMoment != len(PointList):
                        # Update function
                        if len(PointList) > 1:
                            ToDiffuse = True
                        CurrentPoints = copy.deepcopy(PointList)
                    else:
                        # Reset function when double click on button
                        PointList = []
                        ToDiffuse = False
                    PointsAtMoment = len(PointList)
                if OnResetButton:
                    DiffTime = 0

        # Draw lines
        if len(PointList) > 1:
            pygame.draw.lines(window, color.purple, False, PointList, 1)
        list(map(lambda x: pygame.draw.circle(window, color.fistikgreen, x, 3), PointList))

        DrawClearButton()
        DrawResetButton()

        # Animation
        if ToDiffuse:
            diffusion.DiffuseUpdate(FuncToDraw, window, x, xBounds, alpha, n)
        pygame.display.update()


# Run this baby
if __name__ == '__main__':
    main()
