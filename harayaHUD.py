import imageio
import pygame
from pygame.locals import *
from PIL import Image
import random
import os
from threading import Thread

class harayaHUD():
    os.environ['SDL_VIDEO_WINDOW_POS'] = '1240,520'

    global is_random, gif_path
    is_random = 0
    gif_path = "harayasorb.gif"
    
    def setIsRandom(num=0):
        global is_random
        is_random = num
    
    def setGIF(new_gif_path = ""):
        global gif_path
        gif_path = new_gif_path

    def runHUD():
        # Initialize Pygame
        pygame.init()

        # Load the GIF frames using imageio
        gif_reader = imageio.get_reader(gif_path)

        # Set up the display
        first_frame = gif_reader.get_data(0)
        screen = pygame.display.set_mode(first_frame.shape[:2])
        pygame.display.set_caption("H.A.R.A.Y.A")
        icon_image = pygame.image.load("ai.png")
        pygame.display.set_icon(icon_image)

        # Set the initial playback speed (in frames per second)
        playback_speed = 1000

        # Play the GIF
        current_frame = 0
        play_gif = True

        # Main loop
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        setIsRandom(0)
                    elif event.key == K_DOWN:
                        setIsRandom(1)

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

                    # Adjust the playback speed randomly
                    playback_speed = random.randint(19, 20)

                    selector = random.randint(0,is_random)
                    if selector == 0:
                        current_frame += 1
                        clock.tick(playback_speed)
                    elif selector == 1:
                        current_frame -= 1
                        if current_frame < -1000:
                            current_frame = len(gif_reader) - 1
                        elif current_frame >= len(gif_reader):
                            current_frame = -1000
                        clock.tick(playback_speed)
                        
                except EOFError:
                    # Reached the end of the GIF, restart from the beginning
                    gif_reader.close()
                    gif_reader = imageio.get_reader(gif_path)
                    current_frame = 0

        # Clean up
        gif_reader.close()
        pygame.quit()

if __name__ == '__main__':
    runHUD = harayaHUD.runHUD
    setIsRandom = harayaHUD.setIsRandom
    tRandomize = Thread(target=runHUD)
    tRandomize.start()
    #setIsRandom(1)
    
#_____________________python harayaHUD.py