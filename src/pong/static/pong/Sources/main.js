import { Vec3, Vec2 } from './Vector.js';
import Ball from './Ball.js';
import Paddle from './Paddle.js'
import { scoreNode } from './UI/overlay.js';
import { upKeyPressed, downKeyPressed } from './Event.js';
import Collision from "./Collision/Collision.js"
import DataOrigin from './DataOrigin.js';

let gl = null;
let glCanvas = null;

let currentScale = [1.0, 1.0];

// Time
let currentTime;
let deltaTime;
let previousTime = 0.0;

// Entities
let ball;
let player;
let opponent;

// Game related
let score = [];

window.addEventListener("load", init, false);

async function init() {
    glCanvas = document.getElementById("glcanvas");
    gl = glCanvas.getContext("webgl");

    currentScale = [1.0, glCanvas.width / glCanvas.height];

    player = new Paddle(0.05, 0.2, new Vec3(0., 0., 255.), new Vec2(-0.9, 0.), currentScale);
    await player.setup();
    // ball = new Ball(0.02, 4, new Vec3(1., 1., 1.));
    // await ball.setup()
    opponent = new Paddle(0.05, 0.2, new Vec3(255., 0., 0.), new Vec2(0.9, 0.), currentScale);
    await opponent.setup();

    score = [0, 0];

    drawLoop();
}

function drawLoop() {
    gl.viewport(0, 0, glCanvas.width, glCanvas.height);
    gl.clearColor(0., 0., 0., 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT);

    // Delta time
    currentTime = performance.now();
    deltaTime = (currentTime - previousTime) / 1000.0;
    previousTime = currentTime;

    // Positions, events, etc
    // ball.updatePosition(deltaTime);
    player.updatePosition(DataOrigin.Client, deltaTime);
    opponent.updatePosition(DataOrigin.WebSocket, deltaTime);

    // Collisions
    Collision.PaddleWall(player);

    // Update uniforms (position in shader)
    // ball.updateUniform();
    player.updateUniform();
    opponent.updateUniform();

    // Draw
    player.draw();
    opponent.draw();
    // ball.draw();

    scoreNode.nodeValue = score[0] + " | " + score[1];

    requestAnimationFrame(drawLoop);
}

export default gl;