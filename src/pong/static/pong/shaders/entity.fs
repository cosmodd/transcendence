#ifdef GL_ES
	precision highp float;
#endif

varying vec3 vColor;

void main() {
	gl_FragColor = vec4(vColor, 1.0);
	//gl_FragCoord
}
