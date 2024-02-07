export function ResizeCanvas()
{
	let canvas = document.getElementById('glcanvas');

	canvas.width = Math.floor(Math.max(360, window.innerWidth / 2));
	canvas.height = Math.floor(canvas.width * 0.8);
    if (window.innerHeight - 50 < canvas.height) {
        canvas.height = window.innerHeight - 50;
        canvas.width = canvas.height * 1.25;
    }
}


window.addEventListener('resize', (event) => { 
	ResizeCanvas();
});