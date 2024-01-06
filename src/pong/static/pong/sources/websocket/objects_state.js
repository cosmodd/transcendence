import ServerAPI from './server_api.js';
import { Vec2 } from '../utils/class_vec.js';

export function NewPaddleState(initial_pos)
{
	return {
	  promise: Promise.resolve(),
	  position: initial_pos.Clone(),
	  key: "None",
	  new_data_available: true
	};
}

export function NewBallState()
{
	return {
	  promise: Promise.resolve(),
	  position: new Vec2(0., 0.),
	  acceleration: 0.,
	  direction: new Vec2(0., 0.),
	  new_data_available: true
	};
}
