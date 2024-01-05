import { DoIntersect } from "./collision_utils.js";
import { kBallAccelerationStep } from "../objects/constants_objects.js";

// Namespace equivalent
let Collision = {};

let last_ball_pos = null;
Collision.BallPaddle = function(Ball, Paddle) {
    Ball.ComputeBoundingbox();
    Paddle.ComputeBoundingbox();

    if (last_ball_pos == null)
    {
        last_ball_pos = Ball._uEntityPosition.Clone();
        return ;
    }

    let does_intersect = false;
    if (Ball.direction.y < 0.) // Ball y negatif
    {
        // bottom current Ball
        does_intersect = DoIntersect(
        new Vec2(last_ball_pos.x + Ball.radius, (last_ball_pos.y + Ball.radius) * Ball.scaling_factor[1]),
        new Vec2(Ball.boundingbox_left, Ball.boundingbox_bottom),
        new Vec2(Paddle.boundingbox_right, Paddle.boundingbox_bottom),
        new Vec2(Paddle.boundingbox_left, Paddle.boundingbox_top));
        // top current Ball
        does_intersect = DoIntersect(
        new Vec2(last_ball_pos.x + Ball.radius, (last_ball_pos.y + Ball.radius) * Ball.scaling_factor[1]),
        new Vec2(Ball.boundingbox_left, Ball.boundingbox_top),
        new Vec2(Paddle.boundingbox_right, Paddle.boundingbox_bottom),
        new Vec2(Paddle.boundingbox_left, Paddle.boundingbox_top));
    }
    else // Balle y positif
    { 
        // top current Ball
        does_intersect = DoIntersect(
        new Vec2(last_ball_pos.x + Ball.radius, (last_ball_pos.y - Ball.radius) * Ball.scaling_factor[1]),
        new Vec2(Ball.boundingbox_left, Ball.boundingbox_top),
        new Vec2(Paddle.boundingbox_left, Paddle.boundingbox_bottom),
        new Vec2(Paddle.boundingbox_right, Paddle.boundingbox_top));
        // bottom current Ball
        does_intersect = DoIntersect(
        new Vec2(last_ball_pos.x + Ball.radius, (last_ball_pos.y - Ball.radius) * Ball.scaling_factor[1]),
        new Vec2(Ball.boundingbox_left, Ball.boundingbox_bottom),
        new Vec2(Paddle.boundingbox_left, Paddle.boundingbox_bottom),
        new Vec2(Paddle.boundingbox_right, Paddle.boundingbox_top));
    }
    if (does_intersect)
    {
        Ball.direction.x = -Ball.direction.x;
        Ball._uEntityPosition.x = Paddle.boundingbox_right + Ball.radius;
        Ball.acceleration += kBallAccelerationStep;
        if (up_key_pressed)
            Ball.direction.y = 1.;
        if (down_key_pressed)
            Ball.direction.y = -1.;
        last_ball_pos = null;
    }
    else
    {
        last_ball_pos = Ball._uEntityPosition.Clone();
    }
}

Collision.BallWall = function(Ball) {
    Ball.ComputeBoundingbox();

    if (Ball.boundingbox_left <= -1) {
        Ball.direction.x = Math.abs(Ball.direction.x);
        Ball.reset();
        score[1] += 1;
    }
    else if (Ball.boundingbox_right >= 1.) {
        Ball.direction.x = -Math.abs(Ball.direction.x);
        Ball.reset();
        score[0] += 1;
    }
    else if (Ball.boundingbox_top >= 1.) {
        Ball.direction.y = -Math.abs(Ball.direction.y);
    }
    else if (Ball.boundingbox_bottom <= -1.) {
        Ball.direction.y = Math.abs(Ball.direction.y);
    }
}

Collision.PaddleWall = function(Paddle) {
    Paddle.ComputeBoundingbox();

    if (Paddle.boundingbox_top > 1.)
        Paddle._uEntityPosition.y -= Paddle.boundingbox_top - 1.;
    else if (Paddle.boundingbox_bottom < -1.)
        Paddle._uEntityPosition.y += -(Paddle.boundingbox_bottom + 1.);
}

export default Collision;