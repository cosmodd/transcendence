import Mesh from './class_mesh.js'
import { Vec2 } from '../utils/class_vec.js';
import Vertex from './class_vertex.js';
import * as k from '../utils/constants_objects.js';
import ServerAPI from '../websocket/server_api.js';
import DataOrigin from '../utils/data_origin.js';

class Ball extends Mesh {
	constructor (radius = k.BallRadius, resolution = k.BallResolution, color = null, current_scale, data_origin)
	{
		const shader_infos = [
			{
				type: WebGL2RenderingContext.VERTEX_SHADER,
				file_path: k.EntityVertexShaderPath,
			},
			{
				type: WebGL2RenderingContext.FRAGMENT_SHADER,
				file_path: k.EntityFragmentShaderPath,
			},
		];

		let num_faces = resolution * 4.;
		const vertices = [];
		vertices.push(new Vertex(new Vec2(0.0, 0.0), color)); // Origin
		let step_angle = 360.0 / num_faces;
		for (let angle = 0.0; angle < 360.0 ; angle += step_angle) {
			vertices.push(new Vertex(
				new Vec2(
					radius * Math.cos(angle * (Math.PI / 180.0)),
					radius * Math.sin(angle * (Math.PI / 180.0))
				),
				color
			));
		}

		const indices = [];
		for (let i = 0 ; i < num_faces ; i++) {
			indices.push(...[0, i+1, (i+1)%num_faces + 1]);
		}

		super(vertices, indices, (color == null), shader_infos, current_scale);

		this.radius = radius;
		this._uEntityPosition = new Vec2(0, 0);
		this.speed = k.BallSpeed;
		this.acceleration = 0;
		this.direction = new Vec2(0, 0);
		this.data_origin = data_origin;
	}

	// Get new server position OR interpolate
	async UpdatePosition(delta_time)
	{
		try {
			if (this.data_origin === DataOrigin.WebSocket 
				&& await ServerAPI.NewBallStateAvailable()) {
					let ball_state = await ServerAPI.GetBallState();
					this._uEntityPosition = ball_state.position.Clone();
					this.direction = ball_state.direction.Clone();
					this.acceleration = ball_state.acceleration;
			}
			else {
				const current_speed = this.speed + this.acceleration;
				const delta_position = this.direction.Clone().MultiplyScalar(current_speed * delta_time);
				this._uEntityPosition.Add(delta_position);
			}
		} catch(e) {}
	}

	Reset(new_direction)
	{
		this.direction = new_direction
		this._uEntityPosition.y = 0.0;
		this._uEntityPosition.x = 0.0;
		this.acceleration = 0.;
	}

    UpdateUniform()
	{
		if (this.attached_shader.program == null)	  
			return ;

        this.gl.useProgram(this.attached_shader.program);
        this.gl.uniform2f(
            this.gl.getUniformLocation(this.attached_shader.program, "uEntityPosition"),
            this._uEntityPosition.x,
            this._uEntityPosition.y
        );
		this.gl.useProgram(null);
    }

	ComputeBoundingbox()
	{
		this.boundingbox_left = this._uEntityPosition.x - this.radius;
		this.boundingbox_right = this._uEntityPosition.x + this.radius;
		this.boundingbox_top = this._uEntityPosition.y + this.radius;
		this.boundingbox_bottom = this._uEntityPosition.y - this.radius;
		this.boundingbox_left *= this.scaling_factor[0];
		this.boundingbox_right *= this.scaling_factor[0];
		this.boundingbox_top *= this.scaling_factor[1];
		this.boundingbox_bottom *= this.scaling_factor[1];
	}
}

export default Ball;