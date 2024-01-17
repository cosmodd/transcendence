import { Vec2 } from "../utils/class_vec.js";
import * as k from "./constants_objects.js";
import { score_node } from '../ui/overlay.js';
import Paddle from "./class_paddle.js";
import Ball from "./class_ball.js"
import DataOrigin from "../utils/data_origin.js";
import ServerAPI from "../websocket/server_api.js";

class Game {
	constructor(current_scale)
	{
		this.player = null;
		this.opponent = null;
		this.ball = null;
		this.current_scale = current_scale;
		this.score = [0, 0]
		this.delta_time;
		this.current_time;
		this.previous_time = 0.0;
	}

	async SetupPlayer(color = null, position = new Vec2(0.0, 0.0))
	{
		this.player = new Paddle(k.kPaddleWidth, k.kPaddleHeight, color, position, this.current_scale);
		await this.player.Setup();
	}

	async SetupOpponent(color = null, position = new Vec2(0.0, 0.0))
	{
		this.opponent = new Paddle(k.kPaddleWidth, k.kPaddleHeight, color, position, this.current_scale);
		await this.opponent.Setup();
	}

	async SetupBall(color = null)
	{
		this.ball = new Ball(k.kBallRadius, k.kBallResolution, color, this.current_scale);
		await this.ball.Setup()
	}

	ComputeDeltatime()
	{
		this.current_time = performance.now();
		this.delta_time = (this.current_time - this.previous_time) / 1000.0;
		this.previous_time = this.current_time;
	}

	UpdatePositions()
	{
		// Get data from server or interpolate
		this.player.UpdatePosition(DataOrigin.Client, this.delta_time);
		this.opponent.UpdatePosition(DataOrigin.WebSocket, this.delta_time);
		this.ball.UpdatePosition(this.delta_time);
	}

	UpdateUniforms()
	{
		this.player.UpdateUniform();
		this.opponent.UpdateUniform();
		this.ball.UpdateUniform();
	}

	Draw()
	{
		this.player.Draw();
		this.opponent.Draw();
		this.ball.Draw();
    	score_node.nodeValue = this.score[0] + " | " + this.score[1];
	}

	async UpdateScore(data_origin)
	{
		if (data_origin == DataOrigin.WebSocket) {
			if (ServerAPI.NewScoreStateAvailable()) {
				let score_state = await ServerAPI.GetScoreState();
				this.score[0] = score_state.score[ServerAPI.DATA_PLAYER_PLAYER1];
				this.score[1] = score_state.score[ServerAPI.DATA_PLAYER_PLAYER2];
			}
		}
	}
}

export default Game;