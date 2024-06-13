"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3           # Number of attempts

def main():
    graphics = BreakoutGraphics()
    lives = NUM_LIVES

    while lives > 0 and graphics.brick_count > 0:
        if graphics.ball_in_motion:
            # Move the ball
            graphics.ball.move(graphics.get_dx(), graphics.get_dy())

            # Check for collisions
            graphics.check_collisions()

            # Check if the ball goes out of bounds
            if graphics.ball.y >= graphics.window.height:
                lives -= 1
                graphics.reset_ball()

        # Pause
        pause(FRAME_RATE)



if __name__ == '__main__':
    main()
