import { DoIntersect, PaddleInterceptionPoint } from "./collision_utils.js";
import * as k from "../utils/constants_objects.js";
import { Vec2 } from '../utils/class_vec.js'
import { SetDebug } from "../utils/debug.js";

// Namespace equivalent
let Collision = {};

Collision.BallJustLandedInTheNet = false;

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
        new Vec2(last_ball_pos.x + ball.radius, last_ball_pos.y),
        new Vec2(ball.boundingbox_left, ball._uEntityPosition.y),
        new Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom),
        new Vec2(paddle.boundingbox_right, paddle.boundingbox_top));
        if (does_intersect)
            intersect_type = "side";
        // Paddle top
        if (does_intersect === false) {
            does_intersect = DoIntersect(
                new Vec2(last_ball_pos.x, last_ball_pos.y),
                new Vec2(ball._uEntityPosition.x, ball._uEntityPosition.y),
                new Vec2(paddle.boundingbox_right, paddle.boundingbox_top),
                new Vec2(paddle.boundingbox_left, paddle.boundingbox_top));
            if (does_intersect)
                intersect_type = "top";
        }
        // Paddle bottom
        if (does_intersect === false) {
            does_intersect = DoIntersect(
                new Vec2(last_ball_pos.x, last_ball_pos.y),
                new Vec2(ball._uEntityPosition.x, ball._uEntityPosition.y),
                new Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom),
                new Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom));
            if (does_intersect)
                intersect_type = "bottom";
        }
    }

    else if (ball.direction.x > 0.) {
        // Paddle left side
        does_intersect = DoIntersect(
        new Vec2(last_ball_pos.x - ball.radius, last_ball_pos.y),
        new Vec2(ball.boundingbox_right, ball._uEntityPosition.y),
        new Vec2(paddle.boundingbox_left, paddle.boundingbox_top),
        new Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom));
        if (does_intersect)
            intersect_type = "side";
        // Paddle top
        if (does_intersect === false) {
            does_intersect = DoIntersect(
                new Vec2(last_ball_pos.x, last_ball_pos.y),
                new Vec2(ball._uEntityPosition.x, ball._uEntityPosition.y),
                new Vec2(paddle.boundingbox_right, paddle.boundingbox_top),
                new Vec2(paddle.boundingbox_left, paddle.boundingbox_top));
            if (does_intersect)
                intersect_type = "top";
        }
        // Paddle bottom
        if (does_intersect === false) {
            does_intersect = DoIntersect(
                new Vec2(last_ball_pos.x, last_ball_pos.y),
                new Vec2(ball._uEntityPosition.x, ball._uEntityPosition.y),
                new Vec2(paddle.boundingbox_right, paddle.boundingbox_bottom),
                new Vec2(paddle.boundingbox_left, paddle.boundingbox_bottom));
            if (does_intersect)
                intersect_type = "bottom";
        }
    }

    if (does_intersect) {
        if (intersect_type == "side") {
            let intersect = PaddleInterceptionPoint(ball, paddle, last_ball_pos); 
            let local_gap = intersect.y - paddle._uEntityPosition.y; // local gap
            ball._uEntityPosition.x = (ball.direction.x <= 0.0) ? paddle.boundingbox_right + ball.radius : paddle.boundingbox_left - ball.radius;
            // ball._uEntityPosition.y = intersect.y;
            ball.direction.x = -(ball.direction.x + Number.MIN_VALUE);
            ball.direction.y += local_gap / paddle.height_half;
            ball.direction.y = Math.min(1.0, ball.direction.y);
            ball.direction.y = Math.max(-1.0, ball.direction.y);

            // debug
            // console.log("SIDE");
            // SetDebug(intersect.y); 
        }
        else if (intersect_type === "top" || intersect_type == "bottom") {
            ball._uEntityPosition.y = (intersect_type === "top") ? paddle.boundingbox_top + ball.radius : paddle.boundingbox_bottom - ball.radius;
            ball.direction.x = -(ball.direction.x + Number.MIN_VALUE);
            ball.direction.y = -(ball.direction.y + Number.MIN_VALUE);

            //debug
            // console.log(intersect_type);
            // if (intersect_type === "top")
            //     SetDebug(paddle._uEntityPosition.y + paddle.height_half); 
            // else
            //     SetDebug(paddle._uEntityPosition.y - paddle.height_half); 
        }
        ball.acceleration += k.BallAccelerationStep;
        ball.direction.normalize();
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
        game.player.Reset();
        game.opponent.Reset();
        ball.Reset(new Vec2(-1.0, 0.));
        game.score[1] += 1;
        console.log("added score");
        this.BallJustLandedInTheNet = true;
    }
    else if (ball.boundingbox_right >= 1.) {
        game.player.Reset();
        game.opponent.Reset();
        ball.Reset(new Vec2(1.0, 0.));
        game.score[0] += 1;
        console.log("added score");
        this.BallJustLandedInTheNet = true;
    }
    else if (ball.boundingbox_top >= 1.) {
        ball.direction.y = -Math.abs(ball.direction.y);
        ball.acceleration += k.BallAccelerationStep;
        this.BallJustLandedInTheNet = false;
    }
    else if (ball.boundingbox_bottom <= -1.) {
        ball.direction.y = Math.abs(ball.direction.y);
        ball.acceleration += k.BallAccelerationStep;
        this.BallJustLandedInTheNet = false;
    }
}

Collision.PaddleWall = function(paddle) {
    if (paddle == null)
        return ;

    paddle.ComputeBoundingbox();

    if (paddle.boundingbox_top * paddle.scaling_factor[1] > 1.)
        paddle._uEntityPosition.y -= (paddle.boundingbox_top * paddle.scaling_factor[1]) - 1.;
    else if (paddle.boundingbox_bottom * paddle.scaling_factor[1] < -1.)
        paddle._uEntityPosition.y += -(paddle.boundingbox_bottom * paddle.scaling_factor[1] + 1.);
}

export default Collision;