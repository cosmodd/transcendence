import { Vec3, Vec2 } from './utils/class_vec.js';
import GameType from './utils/game_type.js';
import Game from './objects/class_game.js';
import Collision from './collisions/collision.js'
import { ResizeCanvas } from './events/resize.js';
import Timer from './utils/timer.js'
import { DebugDraw, DebugSetup } from './utils/debug.js';
import * as k from './utils/constants_objects.js'

let gl = null;
let gl_canvas = null;

let game;

async function Init(game_type) {
    gl_canvas = document.getElementById("glcanvas");
    gl = gl_canvas.getContext("webgl");

    ResizeCanvas();

    game = new Game(game_type, [1.0, gl_canvas.width / gl_canvas.height]);
    await game.SetupPlayer(new Vec3(13 / 255, 110 / 255, 253 / 255), new Vec2(-0.9, 0.));
    await game.SetupOpponent(new Vec3(220 / 255, 53 / 255, 69 / 255), new Vec2(0.9, 0.));
    await game.SetupBall(new Vec3(1., 1., 1.));

    // await DebugSetup();

    GameLoop();
}

function GameLoop() {
    gl.viewport(0, 0, gl_canvas.width, gl_canvas.height);
    gl.clearColor(0., 0., 0., 0.0);
    gl.clear(gl.COLOR_BUFFER_BIT);

    // Delta time
    game.ComputeDeltatime();

    // Send input to server
    if (game.game_type === GameType.Online)
        game.player.SendInputToServer();

    // Game ended ?
    if (game.game_type == GameType.Local)
        if (game.ScoreLimitReached())
            game.EndGame();

    // Get data from server or interpolate with known keys
    game.UpdatePositions();

    // Collisions
    Collision.PaddleWall(game.player);
    Collision.PaddleWall(game.opponent);
    if (game.game_type === GameType.Local) {
        Collision.BallPaddle(game.ball, game.player);
        Collision.BallPaddle(game.ball, game.opponent);
        Collision.BallWall(game, game.ball);
        if (Collision.BallJustLandedInTheNet && game.TimerEnded() && game.ScoreIsNotEven())
            game.EndGame();
    }

    // Update uniforms - position in shader
    game.UpdateUniforms();

    // Update score - online only
	if (game.game_type == GameType.Online)
        game.UpdateScore();

    // Draw
    game.Draw();

    // DebugDraw(game.player._uEntityPosition);

    requestAnimationFrame(GameLoop);
}

export default Init;