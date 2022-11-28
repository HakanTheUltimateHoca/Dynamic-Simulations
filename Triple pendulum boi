import copy
import time

import numpy as np
import pygame


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


def draw_everything(screen, l1, l2, l3, t1, t2, t3, m1, m2, m3, center):
    screen.fill(color.black)
    p1 = l1 * pygame.math.Vector2(np.sin(t1), np.cos(t1)) + center
    p2 = l2 * pygame.math.Vector2(np.sin(t2), np.cos(t2)) + p1
    p3 = l3 * pygame.math.Vector2(np.sin(t3), np.cos(t3)) + p2
    pygame.draw.aalines(screen, color.white, False, [center, p1, p2, p3])
    pygame.draw.circle(screen, color.fistikgreen, p1, 5 * m1)
    pygame.draw.circle(screen, color.fistikgreen, p2, 5 * m2)
    pygame.draw.circle(screen, color.fistikgreen, p3, 5 * m3)
    pygame.display.update()


mainClock = pygame.time.Clock()


def main():
    # Initials
    g = 10
    m1, m2, m3 = 1, 1.5, 3
    l1, l2, l3 = 150, 150, 150
    theta1, theta2, theta3 = 0.3, 0.7, 0.2
    omega1, omega2, omega3 = 0, 0, 0
    dt = 0.01
    m23 = m2 + m3
    m123 = m1 + m2 + m3
    center = pygame.math.Vector2(400, 100)

    # Window
    pygame.init()
    WIDTH = 800
    HEIGHT = 600
    SIZE = (WIDTH, HEIGHT)
    window = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("sarkac boy")
    window.fill(color.black)

    # lööp
    # a = A(Bw - g * d) / det

    running = True
    while running:

        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == pygame.KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == pygame.QUIT:
                running = False

        c12 = np.cos(theta1 - theta2)
        c13 = np.cos(theta1 - theta3)
        c23 = np.cos(theta2 - theta3)
        s12 = np.sin(theta1 - theta2)
        s13 = np.sin(theta1 - theta3)
        s23 = np.sin(theta2 - theta3)
        s21 = -s12
        s31 = -s13
        s32 = -s23

        A11 = 1 - (m3 * c23 * c23) / m23
        A12 = (m3 * l2 * c13 * c23) / (m123 * l1) - (m23 * l2 * c12) / (m123 * l1)
        A13 = (m3 * l3 * c12 * c23) / (m123 * l1) - (m3 * l3 * c13) / (m123 * l1)
        A21 = (m3 * l1 * c13 * c23) / (m23 * l2) - (l1 * c12) / l2
        A22 = 1 - (m3 * c13 * c13) / m123
        A23 = (m3 * l3 * c12 * c13) / (m123 * l2) - (m3 * l3 * c23) / (m23 * l2)
        A31 = (l1 * c12 * c23) / l3 - (l1 * c13) / l3
        A32 = (m23 * l2 * c12 * c13) / (m123 * l3) - (l2 * c23) / l3
        A33 = 1 - (m23 * c12 * c12) / m123

        det = (m23 * m123 + 2 * m3 * m23 * c12 * c13 * c23 - m3 * m3 * c12 * c12 - m3 * m23 * c13 - m2 * m123 * c23) / (
                m23 * m123)

        B11 = 0
        B12 = (m23 * l2 * s21) / (m123 * l1)
        B13 = (m3 * l3 * s31) / (m123 * l1)
        B21 = (l1 * s12) / l2
        B22 = 0
        B23 = (m3 * l3 * s32) / (m23 * l2)
        B31 = (l1 * s13) / l3
        B32 = (l2 * s23) / l3
        B33 = 0

        w1 = omega1 * omega1
        w2 = omega2 * omega2
        w3 = omega3 * omega3

        d1 = np.sin(theta1) / l1
        d2 = np.sin(theta2) / l2
        d3 = np.sin(theta3) / l3

        f1 = B11 * w1 + B12 * w2 + B13 * w3 - g * d1
        f2 = B21 * w1 + B22 * w2 + B23 * w3 - g * d2
        f3 = B31 * w1 + B32 * w2 + B33 * w3 - g * d3

        alpha1 = A11 * f1 + A12 * f2 + A13 * f3
        alpha2 = A21 * f1 + A22 * f2 + A23 * f3
        alpha3 = A31 * f1 + A32 * f2 + A33 * f3
        alpha1 /= det
        alpha2 /= det
        alpha3 /= det

        omega1 += alpha1 * dt
        omega2 += alpha2 * dt
        omega3 += alpha3 * dt
        theta1 += omega1 * dt
        theta2 += omega2 * dt
        theta3 += omega3 * dt

        draw_everything(window, l1, l2, l3, theta1, theta2, theta3, m1, m2, m3, center)


# Run this baby
if __name__ == '__main__':
    main()
