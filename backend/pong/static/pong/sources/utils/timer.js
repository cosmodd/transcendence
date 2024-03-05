import { time_node } from "../ui/overlay.js";

let Timer = {}
Timer.is_expired = false;
let remaining_time = 0;
let intervalID = undefined

Timer.Start = function()
{
	if (arguments.length == 1 && typeof arguments[0] === 'number')
		remaining_time = arguments[0];
	intervalID = setInterval(UpdateTimer, 1000);
}

Timer.IsIntervalRunning = function()
{
	return (intervalID !== undefined)
}

Timer.Pause = function()
{
	intervalID = clearInterval(intervalID);
}

Timer.ChangeRemainingTime = function(new_remaining_time)
{
	remaining_time = new_remaining_time;
}

Timer.DisplayTimer = function()
{
	var minutes = Math.floor(remaining_time / 60);
	var secondes = remaining_time % 60;
	time_node.nodeValue = ('0' + minutes).slice(-2) + ':' + ('0' + secondes).slice(-2);
}

function UpdateTimer()
{
	if (remaining_time > 0) {
		remaining_time--;
		Timer.DisplayTimer();
	}
	else {
		Timer.is_expired = true;
	}
}

export default Timer;