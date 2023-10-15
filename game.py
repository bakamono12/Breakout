import random
import time
import turtle


class Breakout:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Breakout")
        self.screen.setup(width=800, height=600)
        self.screen.bgcolor("black")
        self.move_x = -10
        self.move_y = -10
        self.points = 0
        self.is_game_over = False

        # score #
        self.score_display = turtle.Turtle()
        self.score_display.speed(0)
        self.score_display.color("white")
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(0, 260)
        self.update_score()

        # paddle #
        self.paddle = turtle.Turtle()
        self.paddle.speed(0)
        self.paddle.shape("square")
        self.paddle.shapesize(stretch_wid=1, stretch_len=10)
        self.paddle.color("white")
        self.paddle.penup()
        self.paddle.goto(0, -280)

        # ball #
        self.ball = turtle.Turtle()
        self.ball.shape("circle")
        self.ball.color("purple")
        self.ball.penup()
        self.ball.goto(0, 0)

        # bricks #
        colors = ["violet", "indigo", "blue", "green", "yellow", "orange", "red"]
        self.bricks = []
        for i in range(7):
            for j in range(10):
                brick = turtle.Turtle()
                brick.shape("square")
                brick.speed(0)
                brick.shapesize(stretch_wid=0.8, stretch_len=4)  # 16 x 80 px
                brick.color(colors[i])
                brick.penup()
                brick.goto(-360 + 80 * j, 290 - 16 * i)
                self.bricks.append(brick)
        # print(self.bricks)

        # bind the keys to the paddle
        self.screen.listen()
        self.screen.onkey(self.move_paddle_left, "Left")
        self.screen.onkey(self.move_paddle_left, "a")
        self.screen.onkey(self.move_paddle_right, "Right")
        self.screen.onkey(self.move_paddle_right, "d")

    def move_paddle_left(self):
        if self.paddle.xcor() > -300:
            self.paddle.setx(self.paddle.xcor() - 20)

    def move_paddle_right(self):
        if self.paddle.xcor() < 300:
            self.paddle.setx(self.paddle.xcor() + 20)

    def move_ball(self):
        x = self.ball.xcor() + self.move_x
        y = self.ball.ycor() + self.move_y
        self.ball.goto(x, y)

    def bounce_ball_x(self):
        self.move_x *= -1

    def bounce_ball_y(self):
        self.move_y *= -1

    def update_score(self):
        self.score_display.clear()
        self.score_display.write(f"Score: {self.points}", align="center", font=("Courier", 24, "normal"))

    def game_over(self):
        self.is_game_over = True
        # self.score_display.clear()
        self.score_display.goto(0, 0)
        self.score_display.write("Game Over", align="center", font=("Courier", 36, "bold"))
        # destroy the bricks
        for brick in self.bricks:
            brick.goto(1000, 1000)


if __name__ == "__main__":
    breakout_game = Breakout()
    while True:
        time.sleep(0.05)
        breakout_game.move_ball()
        # detect collision with walls
        if breakout_game.ball.xcor() > 370 or breakout_game.ball.xcor() < -380:
            breakout_game.bounce_ball_x()
        elif breakout_game.ball.ycor() > 280:
            breakout_game.bounce_ball_y()
        # detect collision with paddle
        if breakout_game.ball.distance(breakout_game.paddle) < 100 and breakout_game.ball.ycor() < -240:
            breakout_game.bounce_ball_y()
        # print("dis", breakout_game.ball.distance(breakout_game.paddle), "x-cor", breakout_game.ball.xcor(), "y_cor",
        #       breakout_game.ball.ycor())
        # detect missing ball
        if breakout_game.ball.ycor() < -300:
            # end the game and display the score
            breakout_game.game_over()
            time.sleep(5)
            break

        # detect collision with bricks
        for brick in breakout_game.bricks:
            if breakout_game.ball.distance(brick) < 40 and breakout_game.ball.ycor() < 290:
                breakout_game.bounce_ball_y()
                brick.goto(1000, 1000)
                breakout_game.points += 1
                breakout_game.update_score()
                if breakout_game.points == len(breakout_game.bricks):
                    breakout_game.game_over()
