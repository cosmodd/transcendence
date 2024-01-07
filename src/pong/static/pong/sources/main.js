import { Vec3, Vec2 } from './utils/class_vec.js';
import Ball from './objects/class_ball.js';
import Paddle from './objects/class_paddle.js'
import { score_node } from './ui/overlay.js';
import { up_key_pressed, down_key_pressed } from './events/key_listener.js';
import Collision from "./collisions/collision.js"
import DataOrigin from './utils/data_origin.js';
import { kBallRadius, kBallResolution, kPaddleHeight, kPaddleWidth } from './objects/constants_objects.js';

let gl = null;
let gl_canvas = null;

let current_scale = [1.0, 1.0];

// Time
let current_time;
let delta_time;
let previous_time = 0.0;

// Entities
let ball;
let player;
let opponent;

// Game related
let score = [];

window.addEventListener("load", Init, false);

async function Init() {
    gl_canvas = document.getElementById("glcanvas");
    gl = gl_canvas.getContext("webgl");

    current_scale = [1.0, gl_canvas.width / gl_canvas.height];

    player = new Paddle(kPaddleWidth, kPaddleHeight, new Vec3(0., 0., 255.), new Vec2(-0.9, 0.), current_scale);
    await player.Setup();
    opponent = new Paddle(kPaddleWidth, kPaddleHeight, new Vec3(255., 0., 0.), new Vec2(0.9, 0.), current_scale);
    await opponent.Setup();
    ball = new Ball(kBallRadius, kBallResolution, new Vec3(1., 1., 1.), current_scale);
    await ball.Setup()

    score = [0, 0];

    DrawLoop();
}

function DrawLoop() {
    gl.viewport(0, 0, gl_canvas.width, gl_canvas.height);
    gl.clearColor(0., 0., 0., 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT);

    // Delta time
    current_time = performance.now();
    delta_time = (current_time - previous_time) / 1000.0;
    previous_time = current_time;

    // Send input to server
    player.SendInputToServer();

    // Get data from server or interpolate
    player.UpdatePosition(DataOrigin.Client, delta_time);
    opponent.UpdatePosition(DataOrigin.WebSocket, delta_time);
    ball.UpdatePosition(delta_time);

    // Collisions check - for interpolation only
    Collision.PaddleWall(player);
    Collision.PaddleWall(opponent);
    // Collision.BallPaddle(ball, player);
    // Collision.BallPaddle(ball, opponent);
    // Collision.BallWall(ball);

    // Update uniforms (position in shader)
    player.UpdateUniform();
    opponent.UpdateUniform();
    ball.UpdateUniform();

    // Draw
    player.Draw();
    opponent.Draw();
    ball.Draw();

    score_node.nodeValue = score[0] + " | " + score[1];

    requestAnimationFrame(DrawLoop);
}

export default gl;