export const BallSpeed = 1.0;
export const BallAccelerationStep = 0.1;
export const BallRadius = 0.02;
export const BallResolution = 4.0;
export const ScoreLimit = 10

export const PaddleSpeed = 1.5;
export const PaddleWidth = 0.05;
export const PaddleHeight = 0.3;
export const GameDuration = 30;

export const EntityVertexShaderPath = `attribute vec2 aVertexPosition;
attribute vec3 aVertexColor;

uniform vec2 uScalingFactor;
uniform vec2 uEntityPosition;

varying vec3 vColor;

void main()
{
    vec2 position = (aVertexPosition + uEntityPosition) * uScalingFactor;
    gl_Position = vec4(position, 0.0, 1.0);

    vColor = aVertexColor;
}`;


export const EntityFragmentShaderPath = `
#ifdef GL_ES
	precision highp float;
#endif

varying vec3 vColor;

void main()
{
	gl_FragColor = vec4(vColor, 1.0);
}`;