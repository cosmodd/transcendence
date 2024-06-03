import Ball from "../objects/class_ball.js";
import DataOrigin from "./data_origin.js";
import { Vec3, Vec2 } from "./class_vec.js";

let debug_1;
export let debug_1_local_gap = 0;

export async function DebugSetup()
{
    debug_1 = new Ball(0.01, 4, new Vec3(0.0, 1.0, 0.0), [1.0, 1.25], DataOrigin.Client);
    await debug_1.Setup();
}

export function DebugDraw(paddle_position)
{
    // debug_1._uEntityPosition = new Vec2(-0.9 + 0.01, paddle_position.y + debug_1_local_gap);
    debug_1._uEntityPosition = new Vec2(-0.9, debug_1_local_gap);
    debug_1.UpdateUniform();
    debug_1.Draw();
}

export function SetDebug(foo)
{
	debug_1_local_gap = foo;
}


