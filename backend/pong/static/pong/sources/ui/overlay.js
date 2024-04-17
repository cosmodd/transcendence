import { GameLoop } from "../main.js";
import ServerAPI from "../websocket/server_api.js";
import * as k from "../utils/constants_objects.js";
import Timer  from "../utils/timer.js";

// Score
let score_element1 = document.getElementById("score1");
export let score_node1 = document.createTextNode("0");
score_element1.appendChild(score_node1);
let score_element2 = document.getElementById("score2");
export let score_node2 = document.createTextNode("0");
score_element2.appendChild(score_node2);

// Time
let time_element = document.getElementById('time');
export let time_node = document.createTextNode("00:00");
time_element.appendChild(time_node);

// Ready button
export let ready_element = document.getElementById('ready');
let ready_node = document.createTextNode('Searching...');
ready_element.appendChild(ready_node);

// Usernames
let left_username_element = document.getElementById('left_username');
let left_username_node = document.createTextNode("");
if (left_username_element != null)
	left_username_element.appendChild(left_username_node);
let right_username_element = document.getElementById('right_username');
let right_username_node = document.createTextNode("");
if (right_username_element != null)
	right_username_element.appendChild(right_username_node);

export function OverlayChangeUsernames(opponent_username, side)
{
	if (side == ServerAPI.DATA_PLAYER_PLAYER1) {
		right_username_node.nodeValue = opponent_username;
		left_username_node.nodeValue = "You";
	}
	else {
		left_username_node.nodeValue = opponent_username;
		right_username_node.nodeValue = "You";
	}
}

export function OverlayInit()
{
	score_node1.nodeValue = 0;
	score_node2.nodeValue = 0;
	Timer.DisplayTimer();
	ready_node.nodeValue = 'Searching...'
}

export function OverlayReadyButtonOnlineListener()
{
	ready_element.addEventListener('click', () => {
		if (ready_node.nodeValue === "Searching...")
			return ;

		ready_element.classList.remove("btn-warning");
		ready_element.classList.add("btn-success");
		ServerAPI.SendReadyState()
		OverlayReadyButtonHide();
	});
	GameLoop();
}

export function OverlayReadyButtonLocalListener()
{
	OverlayReadyButtonShow()
	ready_element.addEventListener('click', () => {
		ready_element.classList.remove("btn-warning");
		ready_element.classList.add("btn-success");
		OverlayReadyButtonHide();
		Timer.Start(k.GameDuration);
		GameLoop();
	});
}

export function OverlayReadyButtonHide()
{
	document.getElementById('glcanvas').classList.remove('blur-5');
	time_element.classList.remove('blur-5');
	score_element1.classList.remove('blur-5');
	score_element2.classList.remove('blur-5');
	ready_element.classList.add("opacity-0");
}

export function OverlayReadyButtonShow(game_type = "", opponent_username = "")
{
	let new_nodevalue = "Press when ready.\n";

	if (game_type.length)
		new_nodevalue += `\n ${game_type} game against ${opponent_username}`
	ready_element.classList.remove("btn-primary");
	ready_element.classList.add("btn-warning");
	ready_node.nodeValue = new_nodevalue;
}