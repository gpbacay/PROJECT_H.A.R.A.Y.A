import pygame

# Initialize Pygame
pygame.init()

# Load the GIF file
gif_path = "path_to_your_gif.gif"
gif = pygame.movie.Movie(gif_path)

# Set up the display
screen = pygame.display.set_mode(gif.get_size())
pygame.display.set_caption("GIF Player")

# Set the initial playback speed (in frames per second)
playback_speed = 30  # Adjust this value to change the initial speed

# Play the GIF
gif.play()

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Adjust the playback speed dynamically
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playback_speed += 10  # Increase the speed by 10 frames per second
            elif event.key == pygame.K_DOWN:
                playback_speed -= 10  # Decrease the speed by 10 frames per second

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the current GIF frame
    screen.blit(gif.get_surface(), (0, 0))

    # Update the display
    pygame.display.flip()

    # Adjust the playback speed
    clock.tick(playback_speed)

# Clean up
pygame.quit()

#if __name__ == '__main__':
    
#_____________________python test16.py