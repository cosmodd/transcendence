import { DoIntersect } from "./collision_utils.js";
import * as k from "../utils/constants_objects.js";
import * as D from "../utils/defines.js"
import { Vec2 } from '../utils/class_vec.js'
import KeyListener from '../events/key_listener.js';

// Namespace equivalent
let Collision = {};

let last_ball_pos_needs_update = 0
let last_ball_pos = null;
Collision.BallPaddle = function(ball, paddle)
{
    last_ball_pos_needs_update += 1;
    ball.ComputeBoundingbox();
    paddle.ComputeBoundingbox();

    if (last_ball_pos == null) {
        last_ball_pos = ball._uEntityPosition.Clone();
        return ;
    }

    let does_intersect = false;

    if (ball.direction.x < 0.) {
        if (ball.direction.y < 0.) { // ball y negatif
            // bottom current ball
            does_intersect = DoIntersect(
            new Vec2(last_ball_pos.x + ball.radius, (last_ball_pos.y + ball.radius) * ball.scaling_factor[1]),
            new Vec2(ball.boundingbox_left, ball.boundingbox_bottom),
            new Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom),
            new Vec2(paddle.boundingbox_left, paddle.boundingbox_top));
            if (does_intersect === false) {
                // top current ball
                does_intersect = DoIntersect(
                new Vec2(last_ball_pos.x + ball.radius, (last_ball_pos.y + ball.radius) * ball.scaling_factor[1]),
                new Vec2(ball.boundingbox_left, ball.boundingbox_top),
                new Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom),
                new Vec2(paddle.boundingbox_left, paddle.boundingbox_top));
            }
        }
        else {// Balle y positif
            // top current ball
            does_intersect = DoIntersect(
            new Vec2(last_ball_pos.x + ball.radius, (last_ball_pos.y - ball.radius) * ball.scaling_factor[1]),
            new Vec2(ball.boundingbox_left, ball.boundingbox_top),
            new Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom),
            new Vec2(paddle.boundingbox_right, paddle.boundingbox_top));
            // bottom current ball
            if (does_intersect === false) {
                does_intersect = DoIntersect(
                new Vec2(last_ball_pos.x + ball.radius, (last_ball_pos.y - ball.radius) * ball.scaling_factor[1]),
                new Vec2(ball.boundingbox_left, ball.boundingbox_bottom),
                new Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom),
                new Vec2(paddle.boundingbox_right, paddle.boundingbox_top));
            }
        }
    }

    if (ball.direction.x >= 0.) {
        if (ball.direction.y < 0.) { // ball y negatif
            // bottom current ball
            does_intersect = DoIntersect(
            new Vec2(last_ball_pos.x - ball.radius, (last_ball_pos.y + ball.radius) * ball.scaling_factor[1]),
            new Vec2(ball.boundingbox_right, ball.boundingbox_bottom),
            new Vec2(paddle.boundingbox_right, paddle.boundingbox_top),
            new Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom));
            if (does_intersect === false) {
                // top current ball
                does_intersect = DoIntersect(
                new Vec2(last_ball_pos.x - ball.radius, (last_ball_pos.y + ball.radius) * ball.scaling_factor[1]),
                new Vec2(ball.boundingbox_right, ball.boundingbox_top),
                new Vec2(paddle.boundingbox_right, paddle.boundingbox_top),
                new Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom));
            }
        }
        else {// Balle y positif
            // top current ball
            does_intersect = DoIntersect(
            new Vec2(last_ball_pos.x - ball.radius, (last_ball_pos.y - ball.radius) * ball.scaling_factor[1]),
            new Vec2(ball.boundingbox_right, ball.boundingbox_top),
            new Vec2(paddle.boundingbox_left, paddle.boundingbox_top),
            new Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom));
            if (does_intersect === false) {
                // bottom current ball
                does_intersect = DoIntersect(
                new Vec2(last_ball_pos.x - ball.radius, (last_ball_pos.y - ball.radius) * ball.scaling_factor[1]),
                new Vec2(ball.boundingbox_right, ball.boundingbox_bottom),
                new Vec2(paddle.boundingbox_left, paddle.boundingbox_top),
                new Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom));
            }
        }
    }

    if (does_intersect) {
        if (ball.direction.x < 0.)
            ball._uEntityPosition.x = paddle.boundingbox_right + ball.radius;
        else
            ball._uEntityPosition.x = paddle.boundingbox_left - ball.radius;
        ball.direction.x = -ball.direction.x;
        ball.acceleration += k.BallAccelerationStep;
        if (KeyListener.LastKeyPressed() === D.KEY_UP)
            ball.direction.y = 1.;
        if (KeyListener.LastKeyPressed() === D.KEY_DOWN)
            ball.direction.y = -1.;
        last_ball_pos = null;
    }
    else {
        if ((last_ball_pos_needs_update % 2) == 0) // Second iteration
            last_ball_pos = ball._uEntityPosition.Clone();
    }
}

Collision.BallWall = function(game, ball) {
    ball.ComputeBoundingbox();

    if (ball.boundingbox_left <= -1) {
        ball.direction.x = Math.abs(ball.direction.x);
        ball.Reset();
        game.score[1] += 1;
    }
    else if (ball.boundingbox_right >= 1.) {
        ball.direction.x = -Math.abs(ball.direction.x);
        ball.Reset();
        game.score[0] += 1;
    }
    else if (ball.boundingbox_top >= 1.) {
        ball.direction.y = -Math.abs(ball.direction.y);
    }
    else if (ball.boundingbox_bottom <= -1.) {
        ball.direction.y = Math.abs(ball.direction.y);
    }
}

Collision.PaddleWall = function(paddle) {
    paddle.ComputeBoundingbox();

    if (paddle.boundingbox_top > 1.)
        paddle._uEntityPosition.y -= paddle.boundingbox_top - 1.;
    else if (paddle.boundingbox_bottom < -1.)
        paddle._uEntityPosition.y += -(paddle.boundingbox_bottom + 1.);
}

export default Collision;