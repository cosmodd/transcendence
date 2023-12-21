import Mesh from './class_mesh.js'
import { Vec2 } from '../utils/class_vec.js';
import Vertex from './class_vertex.js';
import { up_key_pressed, down_key_pressed } from '../events/key_listener.js';
import DataOrigin from '../utils/data_origin.js';
import ServerAPI from '../websocket/server_api.js';
import { kPaddleHeight, kPaddleSpeed, kPaddleWidth } from './constants_objects.js';

class Paddle extends Mesh {
	constructor(width = kPaddleWidth, height = kPaddleHeight, color = null, position = new Vec2(0., 0.), current_scale)
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
	}

	UpdateInput(delta_time) {
		if (up_key_pressed) {
			if (this.last_key != "KeyUp")
				ServerAPI.SendDataKey("KeyUp");
			this.last_key = "KeyUp";
		}
		else if (down_key_pressed) {
			if (this.last_key != "KeyDown")
				ServerAPI.SendDataKey("KeyDown");
			this.last_key = "KeyDown";
		}
		else {
			if (this.last_key != "None")
				ServerAPI.SendDataKey("None");
			this.last_key = "None";
		}
	}

	async UpdatePosition(data_origin, delta_time)
	{
		switch (data_origin) {
			case DataOrigin.Client:
				if (ServerAPI.self_new_data) {
					this._uEntityPosition = await ServerAPI.GetPositionPlayer();
					this.last_key = await ServerAPI.GetKeyPlayer();
					ServerAPI.self_new_data = false;
				}
				else { // Interpolate
					if (this.last_key == "None")
						return ;
					let move = this.speed * delta_time;
					if (this.last_key == "KeyDown")
						move *= -1.0;
					this._uEntityPosition.y += move;
				}

				break;
			case DataOrigin.WebSocket:
				if (ServerAPI.opp_new_data) {
					this._uEntityPosition = await ServerAPI.GetPositionOpponent();
					this.last_key = await ServerAPI.GetKeyOpponent();
					ServerAPI.opp_new_data = false;
				}
				else { // Interpolate
					if (this.last_key == "None")
						return ;
					let move = this.speed * delta_time;
					if (this.last_key == "KeyDown")
						move *= -1.0;
					this._uEntityPosition.y += move;
				}
				break ;
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