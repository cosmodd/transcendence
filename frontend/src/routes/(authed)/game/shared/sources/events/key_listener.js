import * as D from "../utils/defines.js"
import { Vec2 } from "../utils/class_vec.js";

let KeyListener = {}

KeyListener.up_key_pressed = false;
KeyListener.down_key_pressed = false;
KeyListener.w_key_pressed = false;
KeyListener.s_key_pressed = false;

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowUp') {
        KeyListener.up_key_pressed = true;
    } else if (event.key === 'ArrowDown') {
        KeyListener.down_key_pressed = true;
    } else if (event.key === 'w') {
        KeyListener.w_key_pressed = true;
    } else if (event.key === 's') {
        KeyListener.s_key_pressed = true;
    }
});

document.addEventListener('keyup', (event) => {
    if (event.key === 'ArrowUp') {
        KeyListener.up_key_pressed = false;
    } else if (event.key === 'ArrowDown') {
        KeyListener.down_key_pressed = false;
    } else if (event.key === 'w') {
        KeyListener.w_key_pressed = false;
    } else if (event.key === 's') {
        KeyListener.s_key_pressed = false;
    }
});

document.addEventListener('touchstart', (event) => {
    let y = event.touches[0].clientY;

    if (y <= window.innerHeight / 2)
        KeyListener.up_key_pressed = true;
    else
        KeyListener.down_key_pressed = true;
});

document.addEventListener('touchend', (event) => {
    KeyListener.up_key_pressed = false;
    KeyListener.down_key_pressed = false;
});

KeyListener.LastKeyPressed = function(caller)
{
    switch (caller) {
        case D.PLAYER:
            if (KeyListener.up_key_pressed)
                return D.KEY_UP;
            else if (KeyListener.down_key_pressed)
                return D.KEY_DOWN;
            break;
        case D.OPPONENT:
            if (KeyListener.w_key_pressed)
                return D.KEY_W;
            else if (KeyListener.s_key_pressed)
                return D.KEY_S;
            break;
    }
    return D.KEY_NONE;
}

export default KeyListener;