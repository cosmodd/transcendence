import { Vec3 } from '../utils/class_vec.js';
import Vertex from './class_vertex.js';
import Shader from './class_shader.js';

class Mesh {
	constructor(vertices, indices, enable_random_color = false, shader_infos, current_scale) {
		this.gl = document.getElementById('glcanvas').getContext('webgl');
		this.VBO = null;
		this.EBO = null;
		this.vertices = vertices || [new Vertex()];
		this.indices = indices || [];
		this.attached_shader = new Shader();
		this.enable_random_color = enable_random_color;
		this.shader_infos = shader_infos;
		this.scaling_factor = current_scale;
	}

	async Setup() {
		if (this.enable_random_color)
			this._SetupColors();
		this._SetupBuffers();
		await this._SetupShaders();
		this._SetupUniforms()
	}

	_SetupColors() {
		for (let i = 0; i < this.vertices.length; i++) {
			this.vertices[i].color = new Vec3(
				Math.random(),
				Math.random(),
				Math.random()
			);
		}
	}

	_SetupBuffers() {
		this.VBO = this.gl.createBuffer();
		this.EBO = this.gl.createBuffer();
		this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.VBO);
		this.gl.bindBuffer(this.gl.ELEMENT_ARRAY_BUFFER, this.EBO);

		// Send data
		const vertices_data = [];
		for (let i = 0; i < this.vertices.length; i++) {
			vertices_data.push(...this.vertices[i].ToArray());
		}
		this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(vertices_data), this.gl.STATIC_DRAW);
		this.gl.bufferData(this.gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(this.indices), this.gl.STATIC_DRAW);

		this.gl.bindBuffer(this.gl.ARRAY_BUFFER, null);
		this.gl.bindBuffer(this.gl.ELEMENT_ARRAY_BUFFER, null);
	}

	async _SetupShaders() {
		await this.attached_shader.BuildProgram(this.shader_infos);
	}

	_SetupUniforms() {
		// Rendering data shared with the scaler
		this.gl.useProgram(this.attached_shader.program);
		let uScalingFactor = this.gl.getUniformLocation(this.attached_shader.program, "uScalingFactor");
		this.gl.uniform2fv(uScalingFactor, this.scaling_factor);
	}

	Draw() {
		this.gl.useProgram(this.attached_shader.program);

		this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.VBO);
		this.gl.bindBuffer(this.gl.ELEMENT_ARRAY_BUFFER, this.EBO);

		// Linking - replaces vao
		this.gl.enableVertexAttribArray(0);
		this.gl.vertexAttribPointer(0, 2, this.gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 0);
		this.gl.enableVertexAttribArray(1);
		this.gl.vertexAttribPointer(1, 3, this.gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 2 * Float32Array.BYTES_PER_ELEMENT);

		this.gl.drawElements(this.gl.TRIANGLES, this.indices.length, this.gl.UNSIGNED_SHORT, 0);

		this.gl.bindBuffer(this.gl.ARRAY_BUFFER, null);
		this.gl.bindBuffer(this.gl.ELEMENT_ARRAY_BUFFER, null);
	}
}

export default Mesh;
