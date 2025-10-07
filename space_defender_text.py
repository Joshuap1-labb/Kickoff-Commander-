#!/usr/bin/env python3
"""
Space Defender - Text-Based Version
A simple text-based space shooter that works in any terminal!
"""

import os
import sys
import time
import random
import threading
from collections import deque

class TextSpaceDefender:
    def __init__(self):
        self.width = 60
        self.height = 20
        self.player_x = self.width // 2
        self.player_y = self.height - 2
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.running = True
        self.enemy_spawn_timer = 0
        self.enemy_spawn_rate = 20
        
        # Game symbols
        self.player_char = '^'
        self.enemy_char = 'V'
        self.bullet_char = '|'
        self.empty_char = ' '
        self.wall_char = '#'
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw_game(self):
        """Draw the game screen"""
        self.clear_screen()
        
        # Top border
        print('+' + '-' * self.width + '+')
        
        # Game area
        for y in range(self.height):
            line = '|'
            for x in range(self.width):
                char = self.empty_char
                
                # Draw player
                if x == self.player_x and y == self.player_y:
                    char = self.player_char
                
                # Draw enemies
                for enemy in self.enemies:
                    if enemy['x'] == x and enemy['y'] == y:
                        char = self.enemy_char
                        break
                
                # Draw bullets
                for bullet in self.bullets:
                    if bullet['x'] == x and bullet['y'] == y:
                        char = self.bullet_char
                        break
                
                line += char
            line += '|'
            print(line)
        
        # Bottom border
        print('+' + '-' * self.width + '+')
        
        # Game info
        print(f"Score: {self.score} | Lives: {self.lives} | Level: {self.level}")
        print("Controls: A/D to move, S to shoot, Q to quit")
        
        if self.game_over:
            print("GAME OVER! Press R to restart or Q to quit")
    
    def move_player(self, direction):
        """Move the player left or right"""
        if direction == 'left' and self.player_x > 0:
            self.player_x -= 1
        elif direction == 'right' and self.player_x < self.width - 1:
            self.player_x += 1
    
    def shoot(self):
        """Player shoots a bullet"""
        self.bullets.append({
            'x': self.player_x,
            'y': self.player_y - 1,
            'direction': -1  # Moving up
        })
    
    def spawn_enemy(self):
        """Spawn a new enemy"""
        if self.enemy_spawn_timer <= 0:
            self.enemies.append({
                'x': random.randint(0, self.width - 1),
                'y': 0,
                'speed': random.uniform(0.5, 1.5)
            })
            self.enemy_spawn_timer = self.enemy_spawn_rate
        else:
            self.enemy_spawn_timer -= 1
    
    def update_enemies(self):
        """Update enemy positions"""
        for enemy in self.enemies[:]:
            enemy['y'] += enemy['speed']
            if enemy['y'] >= self.height:
                self.enemies.remove(enemy)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
    
    def update_bullets(self):
        """Update bullet positions"""
        for bullet in self.bullets[:]:
            bullet['y'] += bullet['direction']
            if bullet['y'] < 0 or bullet['y'] >= self.height:
                self.bullets.remove(bullet)
    
    def check_collisions(self):
        """Check for collisions between bullets and enemies"""
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if (bullet['x'] == enemy['x'] and 
                    abs(bullet['y'] - enemy['y']) < 1):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break
        
        # Check if enemy hit player
        for enemy in self.enemies[:]:
            if (enemy['x'] == self.player_x and 
                abs(enemy['y'] - self.player_y) < 1):
                self.enemies.remove(enemy)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
    
    def update_level(self):
        """Update game level based on score"""
        new_level = self.score // 100 + 1
        if new_level > self.level:
            self.level = new_level
            self.enemy_spawn_rate = max(5, self.enemy_spawn_rate - 2)
    
    def restart_game(self):
        """Restart the game"""
        self.player_x = self.width // 2
        self.player_y = self.height - 2
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.enemy_spawn_rate = 20
    
    def get_input(self):
        """Get user input in a non-blocking way"""
        import select
        import tty
        import termios
        
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
        return None
    
    def run(self):
        """Main game loop"""
        print("🚀 Space Defender - Text Edition")
        print("Controls: A/D to move, S to shoot, Q to quit, R to restart")
        print("Press Enter to start...")
        input()
        
        # Set up terminal for single character input
        old_settings = None
        try:
            if os.name != 'nt':  # Not Windows
                old_settings = termios.tcgetattr(sys.stdin)
                tty.setraw(sys.stdin.fileno())
        except:
            pass
        
        try:
            while self.running:
                if not self.game_over:
                    # Get input
                    key = self.get_input()
                    if key:
                        key = key.lower()
                        if key == 'a':
                            self.move_player('left')
                        elif key == 'd':
                            self.move_player('right')
                        elif key == 's':
                            self.shoot()
                        elif key == 'q':
                            break
                    elif key == 'r' and self.game_over:
                        self.restart_game()
                    
                    # Update game
                    self.spawn_enemy()
                    self.update_enemies()
                    self.update_bullets()
                    self.check_collisions()
                    self.update_level()
                
                # Draw game
                self.draw_game()
                
                # Game speed
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n👋 Game interrupted!")
        finally:
            # Restore terminal settings
            if old_settings:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        
        print("Thanks for playing Space Defender!")

def main():
    game = TextSpaceDefender()
    game.run()

if __name__ == "__main__":
    main()
