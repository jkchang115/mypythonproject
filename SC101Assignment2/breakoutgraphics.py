"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

# Constants
BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball

class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        self.window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=self.window_width, height=self.window_height, title=title)

        # Create a paddle
        self.paddle_height = paddle_height
        self.paddle_width = paddle_width
        self.paddle_offset = paddle_offset
        self.paddle = GRect(PADDLE_WIDTH, PADDLE_HEIGHT)
        self.paddle.filled = True
        self.window.add(self.paddle, x=(self.window_width - self.paddle_width) / 2, y=self.window_height - self.paddle_offset)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius * 2, ball_radius * 2)
        self.ball.filled = True
        self.window.add(self.ball, x=(self.window_width - ball_radius * 2) / 2, y=(self.window_height - ball_radius * 2) / 2)

        # Ball starting position
        self.start_x = (self.window_width - ball_radius * 2) / 2
        self.start_y = (self.window_height - ball_radius * 2) / 2

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        # Initialize brick counter
        self.brick_count = 0

        # Draw bricks
        self.brick_width = brick_width
        self.brick_height = brick_height
        for i in range(brick_rows):
            for j in range(brick_cols):
                self.brick = GRect(self.brick_width, self.brick_height)
                self.brick.filled = True
                if i < 2:
                    self.brick.fill_color = 'red'
                elif i < 4:
                    self.brick.fill_color = 'orange'
                elif i < 6:
                    self.brick.fill_color = 'yellow'
                elif i < 8:
                    self.brick.fill_color = 'green'
                else:
                    self.brick.fill_color = 'blue'
                self.window.add(self.brick, x=j * (brick_spacing + brick_width), y=brick_offset + i * (brick_spacing + brick_height))
                self.brick_count += 1

        # Initialize mouse listeners
        onmouseclicked(self.start_ball)
        onmousemoved(self.move_paddle)

        # Ball motion flag
        self.ball_in_motion = False

    def move_paddle(self, event):
        """
        Move the paddle horizontally based on the mouse x-coordinate.
        The paddle should not move beyond the window boundaries.
        """
        if (event.x > self.paddle_width / 2) and (event.x < self.window.width - self.paddle_width / 2):
            self.paddle.x = event.x - self.paddle_width / 2

    def start_ball(self, event):
        """
        Start the ball's motion when the user clicks the mouse.
        The ball should only start moving on the first click.
        """
        if not self.ball_in_motion:
            self.__dy = INITIAL_Y_SPEED
            self.__dx = random.uniform(1.0, MAX_X_SPEED)
            if random.random() > 0.5:
                self.__dx = -self.__dx
            self.ball_in_motion = True

    def get_dx(self):
        """Return the current x velocity of the ball."""
        return self.__dx

    def get_dy(self):
        """Return the current y velocity of the ball."""
        return self.__dy

    def reset_ball(self):
        """
        Reset the ball to the center of the window and stop its motion.
        This method is called when the ball goes out of bounds.
        """
        self.ball.x = self.start_x
        self.ball.y = self.start_y
        self.__dx = 0
        self.__dy = 0
        self.ball_in_motion = False

    def check_collisions(self):
        """
        Check for collisions between the ball and other objects (walls, paddle, bricks).
        Update the ball's velocity and remove bricks if a collision is detected.
        """
        # Check for collisions with walls
        if self.ball.x <= 0 or self.ball.x + BALL_RADIUS * 2 >= self.window_width:
            self.__dx = -self.__dx
        if self.ball.y <= 0:
            self.__dy = -self.__dy

        # Check for collisions with the paddle or bricks
        collider = self.get_colliding_object()
        if collider is self.paddle:
            if self.ball.y + BALL_RADIUS * 2 >= self.paddle.y and self.__dy > 0:
                self.__dy = -self.__dy
        elif collider is not None:
            self.window.remove(collider)
            self.brick_count -= 1
            self.__dy = -self.__dy

    def get_colliding_object(self):
        """
        Return the object that the ball collides with, if any.
        Check the four corners of the ball's bounding box for collisions.
        """
        corners = [
            (self.ball.x, self.ball.y),
            (self.ball.x + BALL_RADIUS * 2, self.ball.y),
            (self.ball.x, self.ball.y + BALL_RADIUS * 2),
            (self.ball.x + BALL_RADIUS * 2, self.ball.y + BALL_RADIUS * 2)
        ]

        collision_obj = None
        for corner in corners:
            obj = self.window.get_object_at(corner[0], corner[1])
            if obj is not None:
                collision_obj = obj
                break
        return collision_obj




