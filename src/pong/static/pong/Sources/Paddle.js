import Mesh from './Mesh.js'
import { Vec2, Vec3 } from './Vector.js';
import Vertex from './Vertex.js';
import { upKeyPressed, downKeyPressed, leftKeyPressed, rightKeyPressed } from './Event.js';
import DataOrigin from './DataOrigin.js';

class Paddle extends Mesh {
	constructor(width, height, color = null, position = new Vec2(0., 0.), currentScale) {
		const shaderInfo = [
			{
				type: WebGL2RenderingContext.VERTEX_SHADER,
				filePath: entityVertexShaderPath,
			},
			{
				type: WebGL2RenderingContext.FRAGMENT_SHADER,
				filePath: entityFragmentShaderPath,
			},
		];

		let widthHalf = width / 2.;
		let heightHalf = height / 2.;
		const vertices = [
			new Vertex(new Vec2(-widthHalf, -heightHalf), color),
			new Vertex(new Vec2(widthHalf, -heightHalf), color),
			new Vertex(new Vec2(-widthHalf, heightHalf), color),
			new Vertex(new Vec2(widthHalf, heightHalf), color)
		];

		const indices = [0, 1, 2, 1, 2, 3];

		super(vertices, indices, (color == null), shaderInfo, currentScale);

		this._uEntityPosition = position;
		this.speed = 2.0;
		this.width = width;
		this.height = height;
		this.widthHalf = width / 2.;
		this.heightHalf = height / 2.;
	}

	updatePosition(dataOrigin, deltaTime) {
		const move = this.speed * deltaTime;
		if (dataOrigin === DataOrigin.Client) {
			if (upKeyPressed) {
				this._uEntityPosition.y += move;
			}
			else if (downKeyPressed) {
				this._uEntityPosition.y -= move;
			}
		}
	}

	updateUniform() {
		this.gl.useProgram(this.attachedShader.program);
		this.gl.uniform2f(
			this.gl.getUniformLocation(this.attachedShader.program, "uEntityPosition"),
			this._uEntityPosition.x,
			this._uEntityPosition.y)
		this.gl.useProgram(null);
	}

	computeBoundingBox() {
		this.boundingBoxLeft = this._uEntityPosition.x - this.widthHalf;
		this.boundingBoxRight = this._uEntityPosition.x + this.widthHalf;
		this.boundingBoxTop = this._uEntityPosition.y + this.heightHalf;
		this.boundingBoxBottom = this._uEntityPosition.y - this.heightHalf;
		this.boundingBoxLeft *= this.scalingFactor[0];
		this.boundingBoxRight *= this.scalingFactor[0];
		this.boundingBoxTop *= this.scalingFactor[1];
		this.boundingBoxBottom *= this.scalingFactor[1];
	}
}

export default Paddle;