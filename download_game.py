#!/usr/bin/env python3
"""
Download Space Defender game files
This creates downloadable versions of the game
"""

import os

def create_downloadable_files():
    """Create files that can be easily downloaded"""
    
    # Text-based game (works anywhere)
    text_game = '''#!/usr/bin/env python3
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
            print("\\n👋 Game interrupted!")
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
'''
    
    # Write the text game
    with open('space_defender_text.py', 'w') as f:
        f.write(text_game)
    
    print("✅ Created space_defender_text.py")
    print("📁 You can download this file to your Windows computer")
    print("🚀 Then run: python space_defender_text.py")
    
    # Also create a simple HTML version
    html_game = '''<!DOCTYPE html>
<html>
<head>
    <title>Space Defender - Web Version</title>
    <style>
        body { font-family: monospace; background: black; color: green; }
        .game { white-space: pre; font-size: 12px; }
        .controls { margin-top: 10px; }
    </style>
</head>
<body>
    <h1>🚀 Space Defender - Web Version</h1>
    <div class="game" id="gameArea"></div>
    <div class="controls">
        <p>Controls: A/D to move, S to shoot, R to restart</p>
        <p>Score: <span id="score">0</span> | Lives: <span id="lives">3</span></p>
    </div>
    
    <script>
        class WebSpaceDefender {
            constructor() {
                this.width = 40;
                this.height = 15;
                this.playerX = Math.floor(this.width / 2);
                this.playerY = this.height - 2;
                this.enemies = [];
                this.bullets = [];
                this.score = 0;
                this.lives = 3;
                this.gameOver = false;
                this.enemySpawnTimer = 0;
                this.enemySpawnRate = 20;
                
                this.setupEventListeners();
                this.gameLoop();
            }
            
            setupEventListeners() {
                document.addEventListener('keydown', (e) => {
                    if (this.gameOver && e.key.toLowerCase() === 'r') {
                        this.restart();
                        return;
                    }
                    if (this.gameOver) return;
                    
                    switch(e.key.toLowerCase()) {
                        case 'a': this.movePlayer(-1); break;
                        case 'd': this.movePlayer(1); break;
                        case 's': this.shoot(); break;
                    }
                });
            }
            
            movePlayer(direction) {
                this.playerX = Math.max(0, Math.min(this.width - 1, this.playerX + direction));
            }
            
            shoot() {
                this.bullets.push({x: this.playerX, y: this.playerY - 1, direction: -1});
            }
            
            spawnEnemy() {
                if (this.enemySpawnTimer <= 0) {
                    this.enemies.push({
                        x: Math.floor(Math.random() * this.width),
                        y: 0,
                        speed: 0.5 + Math.random()
                    });
                    this.enemySpawnTimer = this.enemySpawnRate;
                } else {
                    this.enemySpawnTimer--;
                }
            }
            
            update() {
                if (this.gameOver) return;
                
                this.spawnEnemy();
                
                // Update enemies
                this.enemies = this.enemies.filter(enemy => {
                    enemy.y += enemy.speed;
                    if (enemy.y >= this.height) {
                        this.lives--;
                        if (this.lives <= 0) this.gameOver = true;
                        return false;
                    }
                    return true;
                });
                
                // Update bullets
                this.bullets = this.bullets.filter(bullet => {
                    bullet.y += bullet.direction;
                    return bullet.y >= 0 && bullet.y < this.height;
                });
                
                // Check collisions
                this.checkCollisions();
                
                // Update level
                const newLevel = Math.floor(this.score / 100) + 1;
                if (newLevel > this.level) {
                    this.level = newLevel;
                    this.enemySpawnRate = Math.max(5, this.enemySpawnRate - 2);
                }
            }
            
            checkCollisions() {
                // Bullet vs Enemy
                for (let i = this.bullets.length - 1; i >= 0; i--) {
                    for (let j = this.enemies.length - 1; j >= 0; j--) {
                        if (this.bullets[i].x === this.enemies[j].x && 
                            Math.abs(this.bullets[i].y - this.enemies[j].y) < 1) {
                            this.bullets.splice(i, 1);
                            this.enemies.splice(j, 1);
                            this.score += 10;
                            break;
                        }
                    }
                }
                
                // Enemy vs Player
                for (let enemy of this.enemies) {
                    if (enemy.x === this.playerX && Math.abs(enemy.y - this.playerY) < 1) {
                        this.lives--;
                        if (this.lives <= 0) this.gameOver = true;
                        this.enemies = this.enemies.filter(e => e !== enemy);
                        break;
                    }
                }
            }
            
            draw() {
                let display = '+' + '-'.repeat(this.width) + '+\\n';
                
                for (let y = 0; y < this.height; y++) {
                    let line = '|';
                    for (let x = 0; x < this.width; x++) {
                        let char = ' ';
                        
                        if (x === this.playerX && y === this.playerY) {
                            char = '^';
                        } else {
                            for (let enemy of this.enemies) {
                                if (enemy.x === x && Math.floor(enemy.y) === y) {
                                    char = 'V';
                                    break;
                                }
                            }
                            if (char === ' ') {
                                for (let bullet of this.bullets) {
                                    if (bullet.x === x && Math.floor(bullet.y) === y) {
                                        char = '|';
                                        break;
                                    }
                                }
                            }
                        }
                        
                        line += char;
                    }
                    line += '|\\n';
                    display += line;
                }
                
                display += '+' + '-'.repeat(this.width) + '+';
                
                if (this.gameOver) {
                    display += '\\n\\nGAME OVER! Press R to restart';
                }
                
                document.getElementById('gameArea').textContent = display;
                document.getElementById('score').textContent = this.score;
                document.getElementById('lives').textContent = this.lives;
            }
            
            restart() {
                this.playerX = Math.floor(this.width / 2);
                this.playerY = this.height - 2;
                this.enemies = [];
                this.bullets = [];
                this.score = 0;
                this.lives = 3;
                this.gameOver = false;
                this.enemySpawnRate = 20;
            }
            
            gameLoop() {
                this.update();
                this.draw();
                setTimeout(() => this.gameLoop(), 100);
            }
        }
        
        // Start the game
        new WebSpaceDefender();
    </script>
</body>
</html>'''
    
    with open('space_defender_web.html', 'w') as f:
        f.write(html_game)
    
    print("✅ Created space_defender_web.html")
    print("🌐 You can open this in any web browser")
    
    print("\\n📋 Instructions:")
    print("1. Download both files to your Windows computer")
    print("2. For Python version: python space_defender_text.py")
    print("3. For web version: double-click space_defender_web.html")

if __name__ == "__main__":
    create_downloadable_files()