import { Vec3, Vec2 } from './Vector.js';
import Ball from './Ball.js';
import Paddle from './Paddle.js'
import { scoreNode } from './overlay.js';
import { doIntersect } from './collision.js';
import { upKeyPressed, downKeyPressed } from './Event.js';

let gl = null;
let glCanvas = null;

// Aspect ratio and coordinate system
let aspectRatio;
let currentScale = [1.0, 1.0];

// Time
let currentTime;
let deltaTime;
let previousTime = 0.0;

// Entities
let ball;
let player;

// Game related
let score = [];

// Rendering data shared with the scaler
let uScalingFactor;

window.addEventListener("load", init, false);

async function init() {
    glCanvas = document.getElementById("glcanvas");
    gl = glCanvas.getContext("webgl");

    aspectRatio = glCanvas.width / glCanvas.height;
    currentScale = [1.0, aspectRatio];

    player = new Paddle(0.05, 0.2, null, new Vec2(-0.9, 0.));
    await player.setup();
    ball = new Ball(0.02, 4, new Vec3(1., 1., 1.));
    await ball.setup()

    score = [0, 0];

    drawLoop();
}

function drawLoop() {
    gl.viewport(0, 0, glCanvas.width, glCanvas.height);
    // gl.clearColor(0.8, 0.9, 1.0, 1.0);
    gl.clearColor(0., 0., 0., 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT);

    // TO REMOVE - scaling factor
    gl.useProgram(ball.attachedShader.program);
    uScalingFactor = gl.getUniformLocation(ball.attachedShader.program, "uScalingFactor");
    gl.uniform2fv(uScalingFactor, currentScale);
    gl.useProgram(player.attachedShader.program);
    uScalingFactor = gl.getUniformLocation(player.attachedShader.program, "uScalingFactor");
    gl.uniform2fv(uScalingFactor, currentScale);

    // Delta time
    currentTime = performance.now();
    deltaTime = (currentTime - previousTime) / 1000.0;
    previousTime = currentTime;

    // Positions, events, etc
    ball.updatePosition(deltaTime);
    player.updatePosition(deltaTime, currentScale);

    // Collisions
    collisions();

    // Update uniforms (position in shader)
    ball.updateUniform();
    player.updateUniform();

    // Draw
    player.draw();
    ball.draw();

    scoreNode.nodeValue = score[0] + " | " + score[1];

    requestAnimationFrame(drawLoop);
}

function collisions() {
    ball.computeBoundingBox(currentScale);
    player.computeBoundingBox(currentScale);

    // Ball -> player
    playerBallCollision()
    // if local -> player2/ia ball collision

    // Ball -> wall
    if (ball.boundingBoxLeft <= -1) {
        ball.direction.x = Math.abs(ball.direction.x);
        ball.reset();
        score[1] += 1;
    }
    else if (ball.boundingBoxRight >= 1.) {
        ball.direction.x = -Math.abs(ball.direction.x);
    }
    else if (ball.boundingBoxTop >= 1.) {
        ball.direction.y = -Math.abs(ball.direction.y);
    }
    else if (ball.boundingBoxBottom <= -1.) {
        ball.direction.y = Math.abs(ball.direction.y);
    }

    // Player -> wall
    if (player.boundingBoxTop > 1.)
        player._uEntityPosition.y -= player.boundingBoxTop - 1.;
    else if (player.boundingBoxBottom < -1.)
        player._uEntityPosition.y += -(player.boundingBoxBottom + 1.);
}

let lastBallPos = null;
function playerBallCollision() {

    if (lastBallPos == null)
    {
        lastBallPos = ball._uEntityPosition.clone();
        return ;
    }

    let doesIntersect = false;
    if (ball.direction.y < 0.) // ball y negatif
    {
        // bottom current ball
        doesIntersect = doIntersect(
        new Vec2(lastBallPos.x + ball.radius, (lastBallPos.y + ball.radius) * currentScale[1]),
        new Vec2(ball.boundingBoxLeft, ball.boundingBoxBottom),
        new Vec2(player.boundingBoxRight, player.boundingBoxBottom),
        new Vec2(player.boundingBoxLeft, player.boundingBoxTop));
        // top current ball
        doesIntersect = doIntersect(
        new Vec2(lastBallPos.x + ball.radius, (lastBallPos.y + ball.radius) * currentScale[1]),
        new Vec2(ball.boundingBoxLeft, ball.boundingBoxTop),
        new Vec2(player.boundingBoxRight, player.boundingBoxBottom),
        new Vec2(player.boundingBoxLeft, player.boundingBoxTop));
    }
    else // balle y positif
    { 
        // top current ball
        doesIntersect = doIntersect(
        new Vec2(lastBallPos.x + ball.radius, (lastBallPos.y - ball.radius) * currentScale[1]),
        new Vec2(ball.boundingBoxLeft, ball.boundingBoxTop),
        new Vec2(player.boundingBoxLeft, player.boundingBoxBottom),
        new Vec2(player.boundingBoxRight, player.boundingBoxTop));
        // bottom current ball
        doesIntersect = doIntersect(
        new Vec2(lastBallPos.x + ball.radius, (lastBallPos.y - ball.radius) * currentScale[1]),
        new Vec2(ball.boundingBoxLeft, ball.boundingBoxBottom),
        new Vec2(player.boundingBoxLeft, player.boundingBoxBottom),
        new Vec2(player.boundingBoxRight, player.boundingBoxTop));
    }
    if (doesIntersect)
    {
        ball.direction.x = -ball.direction.x;
        ball._uEntityPosition.x = player.boundingBoxRight + ball.radius;
        ball.acceleration += 1;
        if (upKeyPressed)
            ball.direction.y = 1.;
        if (downKeyPressed)
            ball.direction.y = -1.;
        ball.computeBoundingBox(currentScale);
        lastBallPos = null;
    }
    else
    {
        lastBallPos = ball._uEntityPosition.clone();
    }
}

export default gl;