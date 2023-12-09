import { Vec3 } from './Vector.js';
import Vertex from './Vertex.js';
import Shader from './Shader.js';

class Mesh {
	constructor(vertices, indices, randomColor = false, shaderInfo) {
		this.gl = document.getElementById('glcanvas').getContext('webgl');
		this.VBO = null;
		this.EBO = null;
		this.vertices = vertices || [new Vertex()];
		this.indices = indices || [];
		this.attachedShader = new Shader();
		this.randomColor = randomColor;
		this.shaderInfo = shaderInfo;
	}

	async setup() {
		if (this.randomColor)
			this._setupColors();
		this._setupBuffers();
		await this._setupShaders();
	}

	_setupColors() {
		for (let i = 0; i < this.vertices.length; i++) {
			this.vertices[i].color = new Vec3(
				Math.random(),
				Math.random(),
				Math.random()
			);
		}
	}

	_setupBuffers() {
		this.VBO = this.gl.createBuffer();
		this.EBO = this.gl.createBuffer();
		this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.VBO);
		this.gl.bindBuffer(this.gl.ELEMENT_ARRAY_BUFFER, this.EBO);

		// Send data
		const verticesData = [];
		for (let i = 0; i < this.vertices.length; i++) {
			verticesData.push(...this.vertices[i].toArray());
		}
		this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(verticesData), this.gl.STATIC_DRAW);
		this.gl.bufferData(this.gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(this.indices), this.gl.STATIC_DRAW);

		this.gl.bindBuffer(this.gl.ARRAY_BUFFER, null);
		this.gl.bindBuffer(this.gl.ELEMENT_ARRAY_BUFFER, null);
	}

	async _setupShaders() {
		await this.attachedShader.buildProgram(this.shaderInfo);
	}

	draw() {
		this.gl.useProgram(this.attachedShader.program);

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
