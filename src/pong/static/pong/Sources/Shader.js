class Shader {
	constructor() {
		this._projMat = null;
		this._viewMat = null;
		this._modelMat = null;
		this.program = null;
		this.gl = document.getElementById('glcanvas').getContext('webgl');
	}

	async _compileShader(filePath, type) {
		const response = await fetch(filePath);
		if (!response.ok) {
			console.error(`Unable to fetch shader file: ${filePath}`);
			return null;
		}

		const code = await response.text();
		const shader = this.gl.createShader(type);

		this.gl.shaderSource(shader, code);
		this.gl.compileShader(shader);

		if (!this.gl.getShaderParameter(shader, this.gl.COMPILE_STATUS)) {
			console.log(
				`Error compiling ${type === this.gl.VERTEX_SHADER ? "vertex" : "fragment"
				} shader:`,
			);
			console.log(this.gl.getShaderInfoLog(shader));
		}
		return shader;
	}

	async buildProgram(shaderInfo) {
		if (!Array.isArray(shaderInfo) || shaderInfo.length !== 2) {
            throw new Error("L'ensemble de shaders doit être un tableau contenant exactement deux éléments.");
        }
        const validTypes = [WebGL2RenderingContext.VERTEX_SHADER, WebGL2RenderingContext.FRAGMENT_SHADER];
        for (const shader of shaderInfo) {
            if (!shader || !shader.type || !validTypes.includes(shader.type) || !shader.filePath) {
                throw new Error("Chaque shader de l'ensemble doit avoir un type valide et un chemin de fichier spécifié.");
            }
        }

		this.program = this.gl.createProgram();

		await Promise.all(shaderInfo.map(async (desc) => {
			const shader = await this._compileShader(desc.filePath, desc.type);
			if (shader) {
				this.gl.attachShader(this.program, shader);
			}
		}));

		this.gl.linkProgram(this.program);

		if (!this.gl.getProgramParameter(this.program, this.gl.LINK_STATUS)) {
			console.log("Error linking shader program:");
			console.log(this.gl.getProgramInfoLog(this.program));
		}
	}
}

export default Shader;
