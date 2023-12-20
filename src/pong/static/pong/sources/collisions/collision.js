import Ball from "../objects/class_ball.js";
import Paddle from "../objects/class_paddle.js";
import { doIntersect } from "./collision_utils.js";

// Namespace equivalent
let Collision = {};

let lastBallPos = null;
Collision.BallPaddle = function(Ball, Paddle) {
    Ball.computeBoundingBox();
    Paddle.computeBoundingBox();

    if (lastBallPos == null)
    {
        lastBallPos = Ball._uEntityPosition.clone();
        return ;
    }

    let doesIntersect = false;
    if (Ball.direction.y < 0.) // Ball y negatif
    {
        // bottom current Ball
        doesIntersect = doIntersect(
        new Vec2(lastBallPos.x + Ball.radius, (lastBallPos.y + Ball.radius) * Ball.scalingFactor[1]),
        new Vec2(Ball.boundingBoxLeft, Ball.boundingBoxBottom),
        new Vec2(Paddle.boundingBoxRight, Paddle.boundingBoxBottom),
        new Vec2(Paddle.boundingBoxLeft, Paddle.boundingBoxTop));
        // top current Ball
        doesIntersect = doIntersect(
        new Vec2(lastBallPos.x + Ball.radius, (lastBallPos.y + Ball.radius) * Ball.scalingFactor[1]),
        new Vec2(Ball.boundingBoxLeft, Ball.boundingBoxTop),
        new Vec2(Paddle.boundingBoxRight, Paddle.boundingBoxBottom),
        new Vec2(Paddle.boundingBoxLeft, Paddle.boundingBoxTop));
    }
    else // Balle y positif
    { 
        // top current Ball
        doesIntersect = doIntersect(
        new Vec2(lastBallPos.x + Ball.radius, (lastBallPos.y - Ball.radius) * Ball.scalingFactor[1]),
        new Vec2(Ball.boundingBoxLeft, Ball.boundingBoxTop),
        new Vec2(Paddle.boundingBoxLeft, Paddle.boundingBoxBottom),
        new Vec2(Paddle.boundingBoxRight, Paddle.boundingBoxTop));
        // bottom current Ball
        doesIntersect = doIntersect(
        new Vec2(lastBallPos.x + Ball.radius, (lastBallPos.y - Ball.radius) * Ball.scalingFactor[1]),
        new Vec2(Ball.boundingBoxLeft, Ball.boundingBoxBottom),
        new Vec2(Paddle.boundingBoxLeft, Paddle.boundingBoxBottom),
        new Vec2(Paddle.boundingBoxRight, Paddle.boundingBoxTop));
    }
    if (doesIntersect)
    {
        Ball.direction.x = -Ball.direction.x;
        Ball._uEntityPosition.x = Paddle.boundingBoxRight + Ball.radius;
        Ball.acceleration += 1;
        if (upKeyPressed)
            Ball.direction.y = 1.;
        if (downKeyPressed)
            Ball.direction.y = -1.;
        lastBallPos = null;
    }
    else
    {
        lastBallPos = Ball._uEntityPosition.clone();
    }
}

Collision.BallWall = function(Ball) {
    Ball.computeBoundingBox();

    if (Ball.boundingBoxLeft <= -1) {
        Ball.direction.x = Math.abs(Ball.direction.x);
        Ball.reset();
        score[1] += 1;
    }
    else if (Ball.boundingBoxRight >= 1.) {
        Ball.direction.x = -Math.abs(Ball.direction.x);
    }
    else if (Ball.boundingBoxTop >= 1.) {
        Ball.direction.y = -Math.abs(Ball.direction.y);
    }
    else if (Ball.boundingBoxBottom <= -1.) {
        Ball.direction.y = Math.abs(Ball.direction.y);
    }
}

Collision.PaddleWall = function(Paddle) {
    Paddle.computeBoundingBox();

    if (Paddle.boundingBoxTop > 1.)
        Paddle._uEntityPosition.y -= Paddle.boundingBoxTop - 1.;
    else if (Paddle.boundingBoxBottom < -1.)
        Paddle._uEntityPosition.y += -(Paddle.boundingBoxBottom + 1.);
}

export default Collision;