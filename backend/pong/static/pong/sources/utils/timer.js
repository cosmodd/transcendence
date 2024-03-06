import { time_node } from "../ui/overlay.js";

let Timer = {}
Timer.is_expired = false;
Timer.intervalID = null
Timer.remaining_time = 0;

Timer.Start = function()
{
	if (Timer.intervalID !== null)
		return ;
	if (arguments.length == 1 && typeof arguments[0] === 'number')
		Timer.remaining_time = arguments[0];
	Timer.intervalID = setInterval(UpdateTimer, 1000);
}

Timer.Pause = function()
{
	Timer.intervalID = clearInterval(Timer.intervalID);
	Timer.intervalID = null;
}

Timer.ChangeRemainingTime = function(new_remaining_time)
{
	Timer.remaining_time = new_remaining_time;
}

Timer.DisplayTimer = function()
{
	var minutes = Math.floor(Timer.remaining_time / 60);
	var secondes = Timer.remaining_time % 60;
	time_node.nodeValue = ('0' + minutes).slice(-2) + ':' + ('0' + secondes).slice(-2);
}

function UpdateTimer()
{
	if (Timer.remaining_time > 0) {
		Timer.remaining_time--;
		Timer.DisplayTimer();
	}
	else {
		Timer.is_expired = true;
	}
}

export default Timer;