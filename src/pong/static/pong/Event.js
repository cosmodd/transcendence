let upKeyPressed = false;
let downKeyPressed = false;
let leftKeyPressed = false;
let rightKeyPressed = false;

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowUp') {
        upKeyPressed = true;
    } else if (event.key === 'ArrowDown') {
        downKeyPressed = true;
    } else if (event.key === 'ArrowLeft') {
        leftKeyPressed = true;
    } else if (event.key === 'ArrowRight') {
        rightKeyPressed = true;
    }

});

document.addEventListener('keyup', (event) => {
    if (event.key === 'ArrowUp') {
        upKeyPressed = false;
    } else if (event.key === 'ArrowDown') {
        downKeyPressed = false;
    } else if (event.key === 'ArrowLeft') {
        leftKeyPressed = false;
    } else if (event.key === 'ArrowRight') {
        rightKeyPressed = false;
    }
});

export { upKeyPressed, downKeyPressed, leftKeyPressed, rightKeyPressed};
