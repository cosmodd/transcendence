export function ResizeCanvas()
{
	let canvas = document.getElementById('glcanvas');

	// canvas.height = canvas.clientHeight;
	// canvas.width = canvas.height * 1.25;
	canvas.width = canvas.clientWidth;
	canvas.height = canvas.width * 0.8;
	if (window.innerHeight <= canvas.height) {
		canvas.classList.remove('w-100');
		canvas.classList.add('h-100');
	}
	else {
		canvas.classList.add('w-100');
		canvas.classList.remove('h-100');
	}
}


window.addEventListener('resize', (event) => { 
	ResizeCanvas();
});