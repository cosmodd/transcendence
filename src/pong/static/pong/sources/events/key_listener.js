let up_key_pressed = false;
let down_key_pressed = false;
let left_key_pressed = false;
let right_key_pressed = false;

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowUp') {
        up_key_pressed = true;
    } else if (event.key === 'ArrowDown') {
        down_key_pressed = true;
    } else if (event.key === 'ArrowLeft') {
        left_key_pressed = true;
    } else if (event.key === 'ArrowRight') {
        right_key_pressed = true;
    }

});

document.addEventListener('keyup', (event) => {
    if (event.key === 'ArrowUp') {
        up_key_pressed = false;
    } else if (event.key === 'ArrowDown') {
        down_key_pressed = false;
    } else if (event.key === 'ArrowLeft') {
        left_key_pressed = false;
    } else if (event.key === 'ArrowRight') {
        right_key_pressed = false;
    }
});

export { up_key_pressed, down_key_pressed, left_key_pressed, right_key_pressed};
