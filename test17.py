import imageio
import pygame
from pygame.locals import *
import numpy as np
from PIL import Image
from threading import Thread
import time
import pyautogui

#_____________________________python test17.py
""" def pressUp():
    time.sleep(5)
    print("hi")
    # Simulate pressing the up button
    pyautogui.press("up")
    print("hello")
    time.sleep(5)
    pyautogui.press("down")
t1 = Thread(target=pressUp)
t1.start() """

# Initialize Pygame
pygame.init()

# Load the GIF frames using imageio
gif_path = "orbai1.gif"
gif_reader = imageio.get_reader(gif_path)

# Set up the display
first_frame = gif_reader.get_data(0)
screen = pygame.display.set_mode(first_frame.shape[:2])
pygame.display.set_caption("H.A.R.A.Y.A")

# Set the initial playback speed (in frames per second)
playback_speed = 30  # Adjust this value to change the initial speed

# Play the GIF
current_frame = 0
play_gif = True

# Control variable for direction
reverse = False  # Set to True to reverse the direction

# Control variables for speed adjustment
up = False  # Set to True to decrease the speed
down = False  # Set to True to increase the speed

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # Adjust the playback speed dynamically
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                play_gif = not play_gif  # Toggle pause/play
            elif event.key == K_q:
                running = False  # Terminate the program if 'q' is pressed
            elif event.key == K_UP:
                up = not up  # Toggle up variable
            elif event.key == K_DOWN:
                down = not down  # Toggle down variable
            elif event.key == K_RIGHT:
                reverse = not reverse

    if play_gif:
        try:
            # Clear the screen
            screen.fill((0, 0, 0))

            # Read the current GIF frame
            frame = gif_reader.get_data(current_frame)

            # Convert the frame to a PIL image
            pil_image = Image.fromarray(frame)

            # Convert the PIL image to a Pygame surface
            frame_surface = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)

            # Draw the current GIF frame
            screen.blit(frame_surface, (0, 0))

            # Update the display
            pygame.display.flip()

            # Adjust the playback speed
            if reverse:
                current_frame -= 1
            else:
                current_frame += 1
                
            if up:
                playback_speed += 2000  # Increase the speed by 1000 frames per second
                up = False
            elif down:
                playback_speed -= 2000  # Decrease the speed by 1000 frames per second
                down = False
                

            clock.tick(playback_speed)

            # Move to the next frame
            current_frame += 1
        except EOFError:
            # Reached the end of the GIF, restart from the beginning
            gif_reader.close()
            gif_reader = imageio.get_reader(gif_path)
            current_frame = 0

    
# Clean up
gif_reader.close()
pygame.quit()

#_____________________python test17.py