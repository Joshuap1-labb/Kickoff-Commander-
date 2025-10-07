#!/usr/bin/env python3
"""
Space Defender Game Launcher
This script handles the game launch and provides instructions
"""

import os
import sys
import subprocess

def check_pygame():
    """Check if pygame is installed"""
    try:
        import pygame
        print("✅ Pygame is installed")
        return True
    except ImportError:
        print("❌ Pygame not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
            print("✅ Pygame installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install pygame")
            return False

def run_game():
    """Run the Space Defender game"""
    print("🚀 Starting Space Defender...")
    print("=" * 50)
    print("GAME CONTROLS:")
    print("  WASD or Arrow Keys - Move spaceship")
    print("  SPACE - Shoot")
    print("  P - Pause/Resume")
    print("  R - Restart (when game over)")
    print("  ESC - Quit game")
    print("=" * 50)
    print()
    
    try:
        # Set environment variables for headless mode if needed
        env = os.environ.copy()
        env['SDL_VIDEODRIVER'] = 'dummy'  # For headless mode if needed
        
        # Try to run the game
        subprocess.run([sys.executable, "space_defender.py"], env=env)
        
    except KeyboardInterrupt:
        print("\n👋 Game interrupted by user")
    except Exception as e:
        print(f"❌ Error running game: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have a display available")
        print("2. Try running: python3 space_defender.py")
        print("3. If you're in a remote environment, you might need X11 forwarding")

def main():
    print("🎮 Space Defender - Python Edition")
    print("A classic space shooter game!")
    print()
    
    if not check_pygame():
        print("Please install pygame manually: pip install pygame")
        return
    
    print("Press Enter to start the game...")
    input()
    
    run_game()

if __name__ == "__main__":
    main()