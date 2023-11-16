import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((800, 600))

# Create some pixel data
width = 800
height = 600
pixel_data = np.random.randint(0, 255, (width, height, 3)).astype(np.uint8).tobytes()

# Create a Surface from the pixel data
image = pygame.image.frombuffer(pixel_data, (width, height), 'RGB')

# Draw the image on the screen
cnt=0
run=True
while run:
    pixel_data = np.random.randint(0, 255, (width, height, 3)).astype(np.uint8).tobytes()

    # Create a Surface from the pixel data
    image = pygame.image.frombuffer(pixel_data, (width, height), 'RGB')
    screen.blit(image, (0, 0))
    pygame.display.flip()
    cnt+=1
    print(cnt)
    if cnt==1000:
        run=False
# Update the display
pygame.quit()