import Mesh from './class_mesh.js'
import { Vec2 } from '../utils/class_vec.js';
import Vertex from './class_vertex.js';
import { up_key_pressed, down_key_pressed } from '../events/key_listener.js';
import DataOrigin from '../utils/data_origin.js';
import ServerAPI from '../websocket/server_api.js';
import { kPaddleHeight, kPaddleSpeed, kPaddleWidth, PLAYER, OPPONENT } from './constants_objects.js';

class Paddle extends Mesh {
	constructor(width = kPaddleWidth, height = kPaddleHeight, color = null, position = new Vec2(0., 0.), current_scale, data_origin, iam)
	{
		const shader_infos = [
			{
				type: WebGL2RenderingContext.VERTEX_SHADER,
				file_path: kEntityVertexShaderPath,
			},
			{
				type: WebGL2RenderingContext.FRAGMENT_SHADER,
				file_path: kEntityFragmentShaderPath,
			},
		];

		const width_half = width / 2.;
		const height_half = height / 2.;
		const vertices = [
			new Vertex(new Vec2(-width_half, -height_half), color),
			new Vertex(new Vec2(width_half, -height_half), color),
			new Vertex(new Vec2(-width_half, height_half), color),
			new Vertex(new Vec2(width_half, height_half), color)
		];
		const indices = [0, 1, 2, 1, 2, 3];

		super(vertices, indices, (color == null), shader_infos, current_scale);

		this._uEntityPosition = position;
		this.speed = kPaddleSpeed;
		this.width = width;
		this.height = height;
		this.width_half = width_half;
		this.height_half = height_half;
		this.last_key = "None";
		this.data_origin = data_origin;
		this.iam = iam;
	}

	SendInputToServer() {
		let key_pressed = null;
		
		if (this.data_origin === DataOrigin.WebSocket) {
			if (this.iam === PLAYER) {
				if (up_key_pressed) {
					key_pressed = ServerAPI.DATA_INPUT_KEY_UP;
				} else if (down_key_pressed) {
					key_pressed = ServerAPI.DATA_INPUT_KEY_DOWN;
				} else {
					key_pressed = ServerAPI.DATA_INPUT_KEY_NONE;
				}
			
				if (key_pressed !== this.last_key) {
					ServerAPI.SendDataKey(key_pressed);
					this.last_key = key_pressed;
				}
			}
		}
	}

    // Get data from server or interpolate with known keys
	async UpdatePosition(delta_time)
	{
		let paddle_state = null;
		switch (this.data_origin) {
			case DataOrigin.Client:
				if (this.iam === PLAYER) {
					// Do something (update key from input)
				}
				else if (this.iam === OPPONENT) {
					// Do something (update key from IA API ?)
				}
				break;
			case DataOrigin.WebSocket:
				if (this.iam === PLAYER && await ServerAPI.NewPlayerStateAvailable())
					paddle_state = await ServerAPI.GetPlayerState();
				if (this.iam === OPPONENT && await ServerAPI.NewOpponentStateAvailable())
					paddle_state = await ServerAPI.GetOpponentState();
				break ;
		}

		if (paddle_state != null) {
			this._uEntityPosition = paddle_state.position.Clone();
			this.last_key = paddle_state.key;
		}
		else { // Interpolate and/or local
			if (this.last_key == "None")
				return ;
			let move = this.speed * delta_time;
			if (this.last_key == "KeyDown")
				move *= -1.0;
			this._uEntityPosition.y += move;
		}
	}

	UpdateUniform()
	{
		this.gl.useProgram(this.attached_shader.program);
		this.gl.uniform2f(
			this.gl.getUniformLocation(this.attached_shader.program, "uEntityPosition"),
			this._uEntityPosition.x,
			this._uEntityPosition.y)
		this.gl.useProgram(null);
	}

	ComputeBoundingbox()
	{
		this.boundingbox_left = this._uEntityPosition.x - this.width_half;
		this.boundingbox_right = this._uEntityPosition.x + this.width_half;
		this.boundingbox_top = this._uEntityPosition.y + this.height_half;
		this.boundingbox_bottom = this._uEntityPosition.y - this.height_half;
		this.boundingbox_left *= this.scaling_factor[0];
		this.boundingbox_right *= this.scaling_factor[0];
		this.boundingbox_top *= this.scaling_factor[1];
		this.boundingbox_bottom *= this.scaling_factor[1];
	}
}

export default Paddle;