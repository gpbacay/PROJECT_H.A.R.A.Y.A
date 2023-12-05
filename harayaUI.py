import sys
import imageio
import pygame
from pygame.locals import *
from PIL import Image
import random
from threading import Thread

class harayaUI():
    #os.environ['SDL_VIDEO_WINDOW_POS'] = '1140,420'
    
    # Initialize Pygame
    pygame.init()

    global is_random, gif_path, running, is_waiting
    is_random = 0
    gif_path = "Resources\\listen.gif"
    running = True
    is_waiting = False
    
    def isSpeaking(num:int):
        global is_random
        is_random = num
        
    def isWaiting(truthValue:bool):
        global is_waiting
        is_waiting = truthValue
        return is_waiting
    
    def setGIF(new_gif_path:str):
        global gif_path
        gif_path = new_gif_path

    def runUI():
        global running, gif_path
        # Load the GIF frames using imageio
        gif_reader = imageio.get_reader(gif_path)
        
        # Set up the display
        first_frame = gif_reader.get_data(0)
        screen = pygame.display.set_mode(first_frame.shape[:2])
        pygame.display.set_caption("H.A.R.A.Y.A")
        icon_image = pygame.image.load("Resources\\harayasorb_icon.png")
        pygame.display.set_icon(icon_image)

        # Set the initial playback speed (in frames per second)
        playback_speed = 1000

        # Play the GIF
        current_frame = 0
        play_gif = True
                    
        # Main loop
        clock = pygame.time.Clock()
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False

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

                        speaking = random.randint(0,is_random)
                        if speaking == 0:
                            if is_waiting == False:
                                gif_path = "Resources\\listen.gif"
                            else:
                                gif_path = "Resources\\waiting.gif"
                        elif speaking == 1:
                            gif_path = "Resources\\speak.gif"
                        gif_reader = imageio.get_reader(gif_path)
                        current_frame += 1
                        playback_speed = random.randint(14, 15)
                        clock.tick(playback_speed)
                    except EOFError:
                        # Reached the end of the GIF, restart from the beginning
                        gif_reader.close()
                        gif_reader = imageio.get_reader(gif_path)
                        current_frame = 0
            except:
                break
        
        # Clean up
        gif_reader.close()
        sys.exit()

if __name__ == '__main__':
    runUI = harayaUI.runUI
    isSpeaking = harayaUI.isSpeaking
    isWaiting = harayaUI.isWaiting
    runUI()
    pygame.quit()
    sys.exit()
    
#_____________________python harayaUI.py