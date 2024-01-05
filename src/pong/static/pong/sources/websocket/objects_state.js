import ServerAPI from './server_api.js';
import { Vec2 } from '../utils/class_vec.js';

export function NewPaddleState(initial_pos)
{
	return {
	  pos_promise: Promise.resolve(),
	  key_promise: Promise.resolve(),
	  pos: initial_pos.Clone(),
	  key: "None",
	  new_data_available: false
	};
}

export function NewBallState()
{
	return {
	  promise: Promise.resolve(),
	  position: new Vec2(0., 0.),
	  acceleration: 0.,
	  direction: new Vec2(0., 0.),
	  new_data_available: false
	};
}
