export function ResizeCanvas() {
	let canvas = document.getElementById('glcanvas');
	let parent = canvas.parentElement;

	const parentWidth = parent.clientWidth - 20;
	const parentHeight = parent.clientHeight - 20;

	if (parentWidth > parentHeight * 1.25) {
		canvas.width = parentHeight * 1.25;
		canvas.height = parentHeight;
	} else {
		canvas.width = parentWidth;
		canvas.height = parentWidth / 1.25;
	}
}


window.addEventListener('resize', (event) => {
	ResizeCanvas();
});