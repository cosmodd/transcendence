import { GameLoop } from "../main.js";
import ServerAPI from "../websocket/server_api.js";
import * as k from "../utils/constants_objects.js";
import Timer  from "../utils/timer.js";

// Score
let score_element1 = document.getElementById("score1");
export let score_node1 = document.createTextNode("");
score_element1.appendChild(score_node1);
let score_element2 = document.getElementById("score2");
export let score_node2 = document.createTextNode("");
score_element2.appendChild(score_node2);

// Time
let time_element = document.getElementById('time')
export let time_node = document.createTextNode("00:00")
time_element.appendChild(time_node)

// Ready button
export let ready_element = document.getElementById('ready')
let ready_node = document.createTextNode('Searching...')
ready_element.appendChild(ready_node)

export function ReadyButtonOnlineListener()
{
	ready_element.addEventListener('click', () => {
		if (ready_node.nodeValue === "Searching...")
			return ;

		ready_element.classList.remove("btn-warning");
		ready_element.classList.add("btn-success");
		ServerAPI.SendReadyState()
		ReadyButtonHide();
	});
	GameLoop();
}

export function ReadyButtonLocalListener()
{
	ReadyButtonShow()
	ready_element.addEventListener('click', () => {
		ready_element.classList.remove("btn-warning");
		ready_element.classList.add("btn-success");
		ReadyButtonHide();
		Timer.Start(k.GameDuration);
		GameLoop();
	});
}

export function ReadyButtonHide()
{
	document.getElementById('glcanvas').classList.remove('blur-5');
	time_element.classList.remove('blur-5');
	score_element1.classList.remove('blur-5');
	score_element2.classList.remove('blur-5');
	ready_element.classList.add("opacity-0");
}

export function ReadyButtonShow()
{
	ready_node.nodeValue = "Press when ready.";
	ready_element.classList.remove("btn-primary");
	ready_element.classList.add("btn-warning");
}