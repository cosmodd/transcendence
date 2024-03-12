export function ResizeCanvas()
{
	let canvas = document.getElementById('glcanvas');

	canvas.height = canvas.clientHeight;
	canvas.width = canvas.height * 1.25;
}


window.addEventListener('resize', (event) => { 
	ResizeCanvas();
});