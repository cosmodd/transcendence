import * as D from "../utils/defines.js"

let KeyListener = {}

KeyListener.up_key_pressed = false;
KeyListener.down_key_pressed = false;
KeyListener.left_key_pressed = false;
KeyListener.right_key_pressed = false;

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowUp') {
        KeyListener.up_key_pressed = true;
    } else if (event.key === 'ArrowDown') {
        KeyListener.down_key_pressed = true;
    } else if (event.key === 'ArrowLeft') {
        KeyListener.left_key_pressed = true;
    } else if (event.key === 'ArrowRight') {
        KeyListener.right_key_pressed = true;
    }
});

document.addEventListener('keyup', (event) => {
    if (event.key === 'ArrowUp') {
        KeyListener.up_key_pressed = false;
    } else if (event.key === 'ArrowDown') {
        KeyListener.down_key_pressed = false;
    } else if (event.key === 'ArrowLeft') {
        KeyListener.left_key_pressed = false;
    } else if (event.key === 'ArrowRight') {
        KeyListener.right_key_pressed = false;
    }
});

KeyListener.LastKeyPressed = function()
{
    if (KeyListener.up_key_pressed)
        return D.KEY_UP;
    else if (KeyListener.down_key_pressed)
        return D.KEY_DOWN;
    return D.KEY_NONE;
}

export default KeyListener;