import { DoIntersect, PaddleInterceptionYGap } from "./collision_utils.js";
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
    let intersect_type = "none";

    if (ball.direction.x <= 0.) {
        // Paddle right side
        does_intersect = DoIntersect(
        new Vec2(last_ball_pos.x - ball.radius, last_ball_pos.y * ball.scaling_factor[1]),
        new Vec2(ball.boundingbox_left, ball._uEntityPosition.y),
        new Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom),
        new Vec2(paddle.boundingbox_right, paddle.boundingbox_top));
        if (does_intersect)
            intersect_type = "longitudinal";
        // Paddle top
        if (does_intersect === false) {
            does_intersect = DoIntersect(
                new Vec2(last_ball_pos.x, last_ball_pos.y * ball.scaling_factor[1]),
                new Vec2(ball._uEntityPosition.x, ball._uEntityPosition.y),
                new Vec2(paddle.boundingbox_right, paddle.boundingbox_top),
                new Vec2(paddle.boundingbox_left, paddle.boundingbox_top));
        if (does_intersect)
            intersect_type = "transversal";
        }
        // Paddle bottom
        if (does_intersect === false) {
            does_intersect = DoIntersect(
                new Vec2(last_ball_pos.x, last_ball_pos.y * ball.scaling_factor[1]),
                new Vec2(ball._uEntityPosition.x, ball._uEntityPosition.y),
                new Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom),
                new Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom));
        if (does_intersect)
            intersect_type = "transversal";
        }
    }

    if (ball.direction.x >= 0.) {
            // Paddle left side
            does_intersect = DoIntersect(
            new Vec2(last_ball_pos.x + ball.radius, last_ball_pos.y * ball.scaling_factor[1]),
            new Vec2(ball.boundingbox_right, ball._uEntityPosition.y),
            new Vec2(paddle.boundingbox_left, paddle.boundingbox_top),
            new Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom));
            if (does_intersect)
                intersect_type = "longitudinal";
    }

    if (does_intersect) {
        // BALL NEW PLACEMENT
        if (intersect_type == "longitudinal") {
            let intersect = PaddleInterceptionYGap(ball, paddle, last_ball_pos); 
            let local_gap = intersect.y - paddle._uEntityPosition.y; // local gap
            console.log(local_gap);
            if (ball.direction.x < 0.)
                ball._uEntityPosition.x = intersect.x + ball.radius;
            else
                ball._uEntityPosition.x = intersect.x - ball.radius;
            ball._uEntityPosition.y = intersect.y;
            ball.direction.x = -ball.direction.x;
        }
        else if (intersect_type == "transversal") {
            // NEED TO DO
            // if (ball.direction.y < 0.)
            //     ball._uEntityPosition.y = intersect.y + ball.radius;
            // else
            //     ball._uEntityPosition.y = intersect.y - ball.radius;
            // ball._uEntityPosition.x = intersect.x
            // ball.direction.x = -ball.direction.x;
        }
        ball.acceleration += k.BallAccelerationStep;
        // BALL NEW Y 
        // let y_dir_diff = max(1.0, y_gap / paddle.height_half);
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