#!/usr/bin/env python3
"""
Space Defender - Python Pygame Version
A classic space shooter game where you defend Earth from alien invaders!
"""

import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 5
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self, keys):
        # Movement controls
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x = max(0, self.x - self.speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x = min(SCREEN_WIDTH - self.width, self.x + self.speed)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y = max(0, self.y - self.speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y = min(SCREEN_HEIGHT - self.height, self.y + self.speed)
            
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self, screen):
        # Draw player as a spaceship
        points = [
            (self.x + self.width // 2, self.y),  # Top point
            (self.x, self.y + self.height),      # Bottom left
            (self.x + self.width // 4, self.y + self.height * 3 // 4),  # Left wing
            (self.x + self.width * 3 // 4, self.y + self.height * 3 // 4),  # Right wing
            (self.x + self.width, self.y + self.height)  # Bottom right
        ]
        pygame.draw.polygon(screen, GREEN, points)
        pygame.draw.polygon(screen, WHITE, points, 2)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = random.uniform(1, 3)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.shoot_timer = random.randint(60, 180)  # Random shooting interval
        
    def update(self):
        self.y += self.speed
        self.rect.y = self.y
        self.shoot_timer -= 1
        
    def draw(self, screen):
        # Draw enemy as a triangle
        points = [
            (self.x + self.width // 2, self.y + self.height),  # Bottom point
            (self.x, self.y),  # Top left
            (self.x + self.width, self.y)  # Top right
        ]
        pygame.draw.polygon(screen, RED, points)
        pygame.draw.polygon(screen, WHITE, points, 2)
        
    def should_shoot(self):
        return self.shoot_timer <= 0
        
    def reset_shoot_timer(self):
        self.shoot_timer = random.randint(60, 180)

class Bullet:
    def __init__(self, x, y, direction=1, color=GREEN):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 10
        self.speed = 8
        self.direction = direction  # 1 for up, -1 for down
        self.color = color
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self):
        self.y -= self.speed * self.direction
        self.rect.y = self.y
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def is_off_screen(self):
        return self.y < -self.height or self.y > SCREEN_HEIGHT

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.speed = 2
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.type = random.choice(['rapid_fire', 'extra_life', 'shield'])
        self.animation_timer = 0
        
    def update(self):
        self.y += self.speed
        self.rect.y = self.y
        self.animation_timer += 1
        
    def draw(self, screen):
        # Animate the power-up
        size = 25 + 5 * math.sin(self.animation_timer * 0.2)
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        if self.type == 'rapid_fire':
            color = YELLOW
        elif self.type == 'extra_life':
            color = RED
        else:  # shield
            color = CYAN
            
        pygame.draw.circle(screen, color, (int(center_x), int(center_y)), int(size // 2))
        pygame.draw.circle(screen, WHITE, (int(center_x), int(center_y)), int(size // 2), 2)

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 0
        self.max_radius = 30
        self.timer = 0
        self.max_timer = 20
        
    def update(self):
        self.timer += 1
        self.radius = (self.timer / self.max_timer) * self.max_radius
        
    def draw(self, screen):
        if self.timer < self.max_timer:
            # Create explosion effect with multiple circles
            for i in range(3):
                alpha = 255 - (self.timer * 12)
                if alpha > 0:
                    color = (255, 255 - i * 50, 0)
                    pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 
                                     int(self.radius - i * 5))
        
    def is_finished(self):
        return self.timer >= self.max_timer

class StarField:
    def __init__(self):
        self.stars = []
        for _ in range(100):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.5, 2)
            })
    
    def update(self):
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, screen):
        for star in self.stars:
            brightness = int(255 * (1 - star['y'] / SCREEN_HEIGHT))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Defender - Python Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.running = True
        self.game_over = False
        self.paused = False
        self.score = 0
        self.lives = 3
        self.level = 1
        self.enemy_spawn_timer = 0
        self.power_up_spawn_timer = 0
        self.rapid_fire_timer = 0
        self.rapid_fire_active = False
        self.shield_active = False
        self.shield_timer = 0
        
        # Game objects
        self.player = Player(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 60)
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        self.power_ups = []
        self.explosions = []
        self.star_field = StarField()
        
        # Spawn rates
        self.enemy_spawn_rate = 120  # frames
        self.power_up_spawn_rate = 600  # frames
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.shoot()
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    def shoot(self):
        if not self.rapid_fire_active:
            self.bullets.append(Bullet(self.player.x + self.player.width // 2 - 2, 
                                     self.player.y, 1, GREEN))
        else:
            # Rapid fire - shoot multiple bullets
            for i in range(3):
                offset = (i - 1) * 10
                self.bullets.append(Bullet(self.player.x + self.player.width // 2 - 2 + offset, 
                                         self.player.y, 1, YELLOW))
    
    def spawn_enemy(self):
        if self.enemy_spawn_timer <= 0:
            x = random.randint(0, SCREEN_WIDTH - 30)
            self.enemies.append(Enemy(x, -30))
            self.enemy_spawn_timer = self.enemy_spawn_rate
        else:
            self.enemy_spawn_timer -= 1
    
    def spawn_power_up(self):
        if self.power_up_spawn_timer <= 0 and random.random() < 0.1:
            x = random.randint(0, SCREEN_WIDTH - 25)
            self.power_ups.append(PowerUp(x, -25))
            self.power_up_spawn_timer = self.power_up_spawn_rate
        else:
            self.power_up_spawn_timer -= 1
    
    def update(self):
        if self.paused or self.game_over:
            return
            
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        
        # Update star field
        self.star_field.update()
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.y > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
            elif enemy.should_shoot():
                self.enemy_bullets.append(Bullet(enemy.x + enemy.width // 2 - 2, 
                                               enemy.y + enemy.height, -1, RED))
                enemy.reset_shoot_timer()
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
        
        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.enemy_bullets.remove(bullet)
        
        # Update power-ups
        for power_up in self.power_ups[:]:
            power_up.update()
            if power_up.y > SCREEN_HEIGHT:
                self.power_ups.remove(power_up)
        
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_finished():
                self.explosions.remove(explosion)
        
        # Spawn new objects
        self.spawn_enemy()
        self.spawn_power_up()
        
        # Update power-up effects
        if self.rapid_fire_active:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer <= 0:
                self.rapid_fire_active = False
        
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
        
        # Check collisions
        self.check_collisions()
        
        # Update level
        self.update_level()
    
    def check_collisions(self):
        # Bullet vs Enemy
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.explosions.append(Explosion(enemy.x + enemy.width // 2, 
                                                   enemy.y + enemy.height // 2))
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break
        
        # Enemy Bullet vs Player
        if not self.shield_active:
            for bullet in self.enemy_bullets[:]:
                if bullet.rect.colliderect(self.player.rect):
                    self.explosions.append(Explosion(self.player.x + self.player.width // 2, 
                                                   self.player.y + self.player.height // 2))
                    self.enemy_bullets.remove(bullet)
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                    break
        
        # Enemy vs Player
        if not self.shield_active:
            for enemy in self.enemies[:]:
                if enemy.rect.colliderect(self.player.rect):
                    self.explosions.append(Explosion(enemy.x + enemy.width // 2, 
                                                   enemy.y + enemy.height // 2))
                    self.explosions.append(Explosion(self.player.x + self.player.width // 2, 
                                                   self.player.y + self.player.height // 2))
                    self.enemies.remove(enemy)
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                    break
        
        # Power-up vs Player
        for power_up in self.power_ups[:]:
            if power_up.rect.colliderect(self.player.rect):
                self.activate_power_up(power_up.type)
                self.power_ups.remove(power_up)
    
    def activate_power_up(self, power_type):
        if power_type == 'rapid_fire':
            self.rapid_fire_active = True
            self.rapid_fire_timer = 300  # 5 seconds at 60 FPS
        elif power_type == 'extra_life':
            self.lives += 1
        elif power_type == 'shield':
            self.shield_active = True
            self.shield_timer = 600  # 10 seconds at 60 FPS
    
    def update_level(self):
        new_level = self.score // 100 + 1
        if new_level > self.level:
            self.level = new_level
            self.enemy_spawn_rate = max(30, self.enemy_spawn_rate - 10)
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw star field
        self.star_field.draw(self.screen)
        
        # Draw game objects
        if not self.game_over:
            self.player.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
        
        for power_up in self.power_ups:
            power_up.draw(self.screen)
        
        for explosion in self.explosions:
            explosion.draw(self.screen)
        
        # Draw shield effect
        if self.shield_active:
            pygame.draw.circle(self.screen, CYAN, 
                             (self.player.x + self.player.width // 2, 
                              self.player.y + self.player.height // 2), 
                             self.player.width + 10, 3)
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Lives
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 50))
        
        # Level
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (10, 90))
        
        # Power-up indicators
        if self.rapid_fire_active:
            rapid_text = self.small_font.render("RAPID FIRE!", True, YELLOW)
            self.screen.blit(rapid_text, (SCREEN_WIDTH - 150, 10))
        
        if self.shield_active:
            shield_text = self.small_font.render("SHIELD ACTIVE!", True, CYAN)
            self.screen.blit(shield_text, (SCREEN_WIDTH - 150, 40))
        
        # Game over screen
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, RED)
            restart_text = self.small_font.render("Press R to restart", True, WHITE)
            quit_text = self.small_font.render("Press ESC to quit", True, WHITE)
            
            self.screen.blit(game_over_text, 
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, 
                           (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2))
            self.screen.blit(quit_text, 
                           (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 + 30))
        
        # Pause screen
        if self.paused and not self.game_over:
            pause_text = self.font.render("PAUSED", True, YELLOW)
            resume_text = self.small_font.render("Press P to resume", True, WHITE)
            
            self.screen.blit(pause_text, 
                           (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 - 20))
            self.screen.blit(resume_text, 
                           (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 + 20))
    
    def restart_game(self):
        self.game_over = False
        self.score = 0
        self.lives = 3
        self.level = 1
        self.enemy_spawn_rate = 120
        self.rapid_fire_active = False
        self.shield_active = False
        
        self.player = Player(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 60)
        self.enemies.clear()
        self.bullets.clear()
        self.enemy_bullets.clear()
        self.power_ups.clear()
        self.explosions.clear()
    
    def run(self):
        print("🚀 Space Defender - Python Edition")
        print("Controls:")
        print("  WASD or Arrow Keys - Move")
        print("  SPACE - Shoot")
        print("  P - Pause")
        print("  R - Restart (when game over)")
        print("  ESC - Quit")
        print("\nStarting game...")
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()