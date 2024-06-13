"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics1 import BreakoutGraphics

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3           # Number of attempts

def main():
    # Level configurations
    levels = [
        {'rows': 5, 'cols': 5, 'ball_speed': 3},
        {'rows': 7, 'cols': 7, 'ball_speed': 4},
        {'rows': 10, 'cols': 10, 'ball_speed': 5}
    ]

    level = 0
    lives = NUM_LIVES
    score = 0

    while level < len(levels):
        graphics = BreakoutGraphics(levels[level])
        graphics.update_score(score)
        while lives > 0 and graphics.brick_count > 0:
            if graphics.ball_in_motion:
                # Move the ball
                graphics.ball.move(graphics.get_dx(), graphics.get_dy())

                # Check for collisions
                score += graphics.check_collisions()

                # Update the score display
                graphics.update_score(score)

                # Check if the ball goes out of bounds
                if graphics.ball.y >= graphics.window.height:
                    lives -= 1
                    graphics.reset_ball()

            # Pause
            pause(FRAME_RATE)

        if graphics.brick_count == 0:
            level += 1
        else:
            break

    if level == len(levels):
        graphics.display_message("Winner!!")
    else:
        graphics.display_message("Game Over!")

if __name__ == '__main__':
    main()

