import Mesh from './Mesh.js'
import { Vec2 } from './Vector.js';
import Vertex from './Vertex.js';

class Ball extends Mesh {
	constructor (radius = 0.01, resolution = 4.0, color = null) {
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

		let numFaces = resolution * 4.;
		const vertices = [];
		vertices.push(new Vertex(new Vec2(0.0, 0.0), color)); // Origin
		let stepAngle = 360.0 / numFaces;
		for (let angle = 0.0; angle < 360.0 ; angle += stepAngle) {
			vertices.push(new Vertex(
				new Vec2(
					radius * Math.cos(angle * (Math.PI / 180.0)),
					radius * Math.sin(angle * (Math.PI / 180.0))
				),
				color
			));
		}

		const indices = [];
		for (let i = 0 ; i < numFaces ; i++) {
			indices.push(...[0, i+1, (i+1)%numFaces + 1]);
		}

		super(vertices, indices, (color == null), shaderInfo);

		this.radius = radius;
		this._uEntityPosition = new Vec2(0., 0.);
		this.speed = 0.5;
		this.acceleration = 0.;
		this.direction = new Vec2(-Math.random(), Math.random());
		// this.direction = new Vec2(-1., 0.);
		this.direction.normalize();	  
	}

	updatePosition(deltaTime) {
        const currentSpeed = this.speed + this.acceleration;

		//new position = position + (direction * speed)
        const deltaPosition = this.direction.clone().multiplyScalar(currentSpeed * deltaTime);
        this._uEntityPosition.add(deltaPosition);
	}

	reset() {
		this._uEntityPosition.x = 0.;
		this._uEntityPosition.y = 0.;
		this.direction = new Vec2(-Math.random(), Math.random());
		// this.direction = new Vec2(-1., 0.);
		this.acceleration = 0.;
	}

    updateUniform() {
        this.gl.useProgram(this.attachedShader.program);
        this.gl.uniform2f(
            this.gl.getUniformLocation(this.attachedShader.program, "uEntityPosition"),
            this._uEntityPosition.x,
            this._uEntityPosition.y
        );
		this.gl.useProgram(null);
    }

	computeBoundingBox(currentScale) {
		this.boundingBoxLeft = this._uEntityPosition.x - this.radius;
		this.boundingBoxRight = this._uEntityPosition.x + this.radius;
		this.boundingBoxTop = this._uEntityPosition.y + this.radius;
		this.boundingBoxBottom = this._uEntityPosition.y - this.radius;
		this.boundingBoxLeft *= currentScale[0];
		this.boundingBoxRight *= currentScale[0];
		this.boundingBoxTop *= currentScale[1];
		this.boundingBoxBottom *= currentScale[1];
	}
}

export default Ball;