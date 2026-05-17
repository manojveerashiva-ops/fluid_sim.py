import os
import sys
import time
import math
import random

# Core Simulation Parameters
WIDTH, HEIGHT = 70, 35
GRAVITY = 0.15
DAMPING = 0.85  # Energy loss on wall bounce
DENSITY_RADIUS = 3.5
TERM_CHARS = " .:-=+*#%@"

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.2, 0.2)

def update_physics(particles, target_x, target_y):
    # Update positions and handle boundaries
    for p in particles:
        # Apply Gravity
        self_grav = GRAVITY
        
        # Attract to mouse/target point if active
        if target_x is not None and target_y is not None:
            dx = target_x - p.x
            dy = target_y - p.y
            dist = math.sqrt(dx*dx + dy*dy) + 0.1
            if dist < 15:
                p.vx += (dx / dist) * 0.2
                p.vy += (dy / dist) * 0.2
                self_grav *= 0.2 # Float toward target

        p.vy += self_grav
        p.x += p.vx
        p.y += p.vy

        # Wall Collisions
        if p.x < 0: p.x = 0; p.vx *= -DAMPING
        if p.x >= WIDTH: p.x = WIDTH - 1; p.vx *= -DAMPING
        if p.y < 0: p.y = 0; p.vy *= -DAMPING
        if p.y >= HEIGHT: p.y = HEIGHT - 1; p.vy *= -DAMPING

def render_frame(particles):
    # Initialize blank screen buffer
    grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    # Calculate density map (how close particles are to each other)
    for p in particles:
        px, py = int(p.x), int(p.y)
        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
            grid[py][px] += 3  # High density at core

    # Smooth out density to create a fluid look
    output = []
    for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            # Calculate local density around this pixel
            density = 0
            for p in particles:
                dist = math.sqrt((p.x - x)**2 + (p.y - y)**2)
                if dist < DENSITY_RADIUS:
                    density += (DENSITY_RADIUS - dist)
            
            # Map density to an ASCII character
            char_index = min(int(density * 0.8), len(TERM_CHARS) - 1)
            row += TERM_CHARS[char_index]
        output.append(row)
    
    # ANSI escape code to clear screen efficiently without flickering
    sys.stdout.write("\033[H" + "\n".join(output))
    sys.stdout.flush()

def main():
    # Create an initial cluster of fluid particles
    particles = [Particle(random.uniform(20, 50), random.uniform(5, 15)) for _ in range(120)]
    
    # Setup ANSI screen
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[?25l") # Hide cursor
    
    frame = 0
    try:
        while True:
            # Create a moving vortex/attractor point that orbits over time
            angle = frame * 0.08
            target_x = WIDTH / 2 + math.cos(angle) * 20
            target_y = HEIGHT / 2 + math.sin(angle * 1.5) * 8
            
            # Simulate and Render
            update_physics(particles, target_x, target_y)
            render_frame(particles)
            
            time.sleep(0.03) # ~30 FPS
            frame += 1
    except KeyboardInterrupt:
        print("\033[?25h") # Restore cursor on exit
        print("\nSimulation ended.")

if __name__ == "__main__":
    main()
