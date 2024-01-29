class Shader {
	constructor() {
		this.program = null;
		this.gl = document.getElementById('glcanvas').getContext('webgl');
	}

	async _CompileShader(file_path, type) {
		const response = await fetch(file_path);
		if (!response.ok) {
			console.error(`Unable to fetch shader file: ${file_path}`);
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

	async BuildProgram(shader_infos) {
		if (!Array.isArray(shader_infos) || shader_infos.length !== 2) {
            throw new Error("L'ensemble de shaders doit être un tableau contenant exactement deux éléments.");
        }
        const valid_types = [WebGL2RenderingContext.VERTEX_SHADER, WebGL2RenderingContext.FRAGMENT_SHADER];
        for (const shader of shader_infos) {
            if (!shader || !shader.type || !valid_types.includes(shader.type) || !shader.file_path) {
                throw new Error("Chaque shader de l'ensemble doit avoir un type valide et un chemin de fichier spécifié.");
            }
        }

		this.program = this.gl.createProgram();

		await Promise.all(shader_infos.map(async (desc) => {
			const shader = await this._CompileShader(desc.file_path, desc.type);
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
