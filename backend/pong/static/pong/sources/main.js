import { Vec3, Vec2 } from './utils/class_vec.js';
import GameType from './utils/game_type.js';
import Game from './objects/class_game.js';
import Collision from './collisions/collision.js'

let gl = null;
let gl_canvas = null;

// Game related
let game;

window.addEventListener("load", Init, false);

async function Init() {
    gl_canvas = document.getElementById("glcanvas");
    gl = gl_canvas.getContext("webgl");

    game = new Game(GameType.Local, [1.0, gl_canvas.width / gl_canvas.height]);
    await game.SetupPlayer(new Vec3(0, 0, 1.), new Vec2(-0.9, 0.));
    await game.SetupOpponent(new Vec3(1., 0, 0), new Vec2(0.9, 0.));
    await game.SetupBall(new Vec3(1., 1., 1.));
    
    GameLoop();
}

function GameLoop() {
    gl.viewport(0, 0, gl_canvas.width, gl_canvas.height);
    gl.clearColor(0., 0., 0., 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT);

    // Delta time
    game.ComputeDeltatime();

    // Send input to server
    if (game.game_type === GameType.Online)
        game.player.SendInputToServer();

    // Get data from server or interpolate with known keys
    game.UpdatePositions();

    // Collisions - local only
    if (game.game_type === GameType.Local) {
        Collision.PaddleWall(game.player);
        Collision.PaddleWall(game.opponent);
        Collision.BallPaddle(game.ball, game.player);
        Collision.BallPaddle(game.ball, game.opponent);
        Collision.BallWall(game, game.ball);
    }

    // Update uniforms - position in shader
    game.UpdateUniforms();

    // Update score - online only
	if (game.game_type == GameType.Online)
        game.UpdateScore();

    // Draw
    game.Draw();

    requestAnimationFrame(GameLoop);
}

export default gl;