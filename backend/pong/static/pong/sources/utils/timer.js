import { time_node } from "../ui/overlay.js";

let Timer = {}
Timer.is_expired = false;
let remaining_time = 0;

Timer.Start = function(duration)
{
	remaining_time = duration;

	let interval = setInterval(UpdateTimer, 1000);
}

Timer.ChangeRemainingTime = function(new_remaining_time)
{
	remaining_time = new_remaining_time;
}

function UpdateTimer()
{
	if (remaining_time > 0) {
		remaining_time--;
		DisplayTimer();
	}
	else {
		Timer.is_expired = true;
	}

}

function DisplayTimer()
{
	var minutes = Math.floor(remaining_time / 60);
	var secondes = remaining_time % 60;
	time_node.nodeValue = ('0' + minutes).slice(-2) + ':' + ('0' + secondes).slice(-2);
}


export default Timer;