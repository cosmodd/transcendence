from class_game import *
from classes_objects import *
from class_vec2 import Vec2

def PaddleWall(player: Paddle):
    player.ComputeBoundingbox()

    if (player.boundingbox_top > 1.):
        player.position.y -= player.boundingbox_top - 1.
    elif (player.boundingbox_bottom < -1.):
        player.position.y += -(player.boundingbox_bottom + 1.)

def BallWall(ball: Ball):
    ball.ComputeBoundingbox()

    if (ball.boundingbox_left <= -1.):
        ball.direction.x = abs(ball.direction.x);
        ball.Reset()
        ball.collided = True
        # score[1] += 1;
    elif (ball.boundingbox_right >= 1.):
        ball.direction.x = -abs(ball.direction.x)
        ball.Reset()
        ball.collided = True
    elif (ball.boundingbox_top >= 1.):
        ball.direction.y = -abs(ball.direction.y)
        ball.collided = True
    elif (ball.boundingbox_bottom <= -1.):
        ball.direction.x = abs(ball.direction.y)
        ball.collided = True

# Collision.BallPaddle = function(Ball, Paddle) {
#     Ball.ComputeBoundingbox();
#     Paddle.ComputeBoundingbox();

#     if (last_ball_pos == null)
#     {
#         last_ball_pos = Ball._uEntityPosition.Clone();
#         return ;
#     }

#     let does_intersect = false;
#     if (Ball.direction.y < 0.) // Ball y negatif
#     {
#         // bottom current Ball
#         does_intersect = DoIntersect(
#         new Vec2(last_ball_pos.x + Ball.radius, (last_ball_pos.y + Ball.radius) * Ball.scaling_factor[1]),
#         new Vec2(Ball.boundingbox_left, Ball.boundingbox_bottom),
#         new Vec2(Paddle.boundingbox_right, Paddle.boundingbox_bottom),
#         new Vec2(Paddle.boundingbox_left, Paddle.boundingbox_top));
#         // top current Ball
#         does_intersect = DoIntersect(
#         new Vec2(last_ball_pos.x + Ball.radius, (last_ball_pos.y + Ball.radius) * Ball.scaling_factor[1]),
#         new Vec2(Ball.boundingbox_left, Ball.boundingbox_top),
#         new Vec2(Paddle.boundingbox_right, Paddle.boundingbox_bottom),
#         new Vec2(Paddle.boundingbox_left, Paddle.boundingbox_top));
#     }
#     else // Balle y positif
#     { 
#         // top current Ball
#         does_intersect = DoIntersect(
#         new Vec2(last_ball_pos.x + Ball.radius, (last_ball_pos.y - Ball.radius) * Ball.scaling_factor[1]),
#         new Vec2(Ball.boundingbox_left, Ball.boundingbox_top),
#         new Vec2(Paddle.boundingbox_left, Paddle.boundingbox_bottom),
#         new Vec2(Paddle.boundingbox_right, Paddle.boundingbox_top));
#         // bottom current Ball
#         does_intersect = DoIntersect(
#         new Vec2(last_ball_pos.x + Ball.radius, (last_ball_pos.y - Ball.radius) * Ball.scaling_factor[1]),
#         new Vec2(Ball.boundingbox_left, Ball.boundingbox_bottom),
#         new Vec2(Paddle.boundingbox_left, Paddle.boundingbox_bottom),
#         new Vec2(Paddle.boundingbox_right, Paddle.boundingbox_top));
#     }
#     if (does_intersect)
#     {
#         Ball.direction.x = -Ball.direction.x;
#         Ball._uEntityPosition.x = Paddle.boundingbox_right + Ball.radius;
#         Ball.acceleration += kBallAccelerationStep;
#         if (up_key_pressed)
#             Ball.direction.y = 1.;
#         if (down_key_pressed)
#             Ball.direction.y = -1.;
#         last_ball_pos = null;
#     }
#     else
#     {
#         last_ball_pos = Ball._uEntityPosition.Clone();
#     }
# }