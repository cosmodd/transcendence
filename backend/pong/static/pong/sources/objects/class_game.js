import { Vec2 } from "../utils/class_vec.js";
import * as k from "../utils/constants_objects.js";
import * as D from "../utils/defines.js"
import { score_node } from '../ui/overlay.js';
import Paddle from "./class_paddle.js";
import Ball from "./class_ball.js"
import DataOrigin from "../utils/data_origin.js";
import GameType from "../utils/game_type.js";
import ServerAPI from "../websocket/server_api.js";

class Game {
	constructor(game_type = GameType.Local, current_scale)
	{
		this.game_type = game_type;
		this.player = null;
		this.opponent = null;
		this.ball = null;
		this.current_scale = current_scale;
		this.score = [0, 0]
		this.delta_time;
		this.current_time;
		this.previous_time = 0.0;

		if (this.game_type === GameType.Online)
			ServerAPI.InitConnection();
	}

	async SetupPlayer(color = null, position = new Vec2(0.0, 0.0))
	{
		let data_origin = this.game_type === GameType.Online ? DataOrigin.WebSocket : DataOrigin.Client;
		this.player = new Paddle(k.PaddleWidth, k.PaddleHeight, color, position, this.current_scale, data_origin, D.PLAYER);
		await this.player.Setup();
	}

	async SetupOpponent(color = null, position = new Vec2(0.0, 0.0))
	{
		let data_origin = this.game_type === GameType.Online ? DataOrigin.WebSocket : DataOrigin.Client;
		this.opponent = new Paddle(k.PaddleWidth, k.PaddleHeight, color, position, this.current_scale, data_origin, D.OPPONENT);
		await this.opponent.Setup();
	}

	async SetupBall(color = null)
	{
		let data_origin = this.game_type === GameType.Online ? DataOrigin.WebSocket : DataOrigin.Client;
		this.ball = new Ball(k.BallRadius, k.BallResolution, color, this.current_scale, data_origin);
		await this.ball.Setup()

	    if (this.game_type === GameType.Local)
			this.ball.Reset(new Vec2(-1., 0.));
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
		this.player.UpdatePosition(this.delta_time);
		this.opponent.UpdatePosition(this.delta_time);
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

	async UpdateScore()
	{
		if (this.game_type == GameType.Online) {
			if (ServerAPI.NewScoreStateAvailable()) {
				let score_state = await ServerAPI.GetScoreState();
				this.score[0] = score_state.score[ServerAPI.DATA_PLAYER_PLAYER1];
				this.score[1] = score_state.score[ServerAPI.DATA_PLAYER_PLAYER2];
			}
		}
		// else ?
	}
}

export default Game;