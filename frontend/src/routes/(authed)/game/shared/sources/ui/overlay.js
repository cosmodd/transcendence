import { GameLoop } from "../main.js";
import ServerAPI from "../websocket/server_api.js";
import * as k from "../utils/constants_objects.js";
import Timer  from "../utils/timer.js";
import { Vec2 } from "../utils/class_vec.js";

// Score
let score_element1 = null;
export let score_node1 = document.createTextNode("0");
let score_element2 = null;
export let score_node2 = document.createTextNode("0");

// Time
let time_element = null;
export let time_node = document.createTextNode("00:00");

// Ready button
export let ready_element = null;
export let ready_node = document.createTextNode('Searching...');

// Usernames
let left_username_element = null;
let left_username_node = document.createTextNode("");
let right_username_element = null;
let right_username_node = document.createTextNode("");

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
	// Score
	score_element1 = document.getElementById("score1");
	score_element1.appendChild(score_node1);
	score_element2 = document.getElementById("score2");
	score_element2.appendChild(score_node2);

	// Time
	time_element = document.getElementById('time');
	time_element.appendChild(time_node);

	// Ready button
	ready_element = document.getElementById('ready');
	ready_element.appendChild(ready_node);

	// Usernames
	left_username_element = document.getElementById('left_username');
	if (left_username_element != null)
		left_username_element.appendChild(left_username_node);
	right_username_element = document.getElementById('right_username');
	if (right_username_element != null)
		right_username_element.appendChild(right_username_node);

	Timer.DisplayTimer();
	if (ready_node.nodeValue != 'Press when ready.\n') {
		ready_node.nodeValue = 'Searching...';
	}
}

export function OverlayShowSearching()
{
	ready_node.nodeValue = 'Searching...';
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

export function OverlayReadyButtonLocalListener(game)
{
	OverlayReadyButtonShow()
	ready_element.addEventListener('click', () => {
		ready_element.classList.remove("btn-warning");
		ready_element.classList.add("btn-success");
		OverlayReadyButtonHide();
		Timer.Start(k.GameDuration);
        game.ball.Reset(new Vec2(1.0, 0.));
		GameLoop();
	});
}


export function OverlayReadyButtonHide()
{
	document.getElementById('blurcul').classList.remove('blur-5');
	document.getElementById('ready').classList.add("opacity-0");
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

export function OverlayRefresh()
{
	score_element1 = document.getElementById("score1");
	score_element1.appendChild(score_node1);
	score_element2 = document.getElementById("score2");
	score_element2.appendChild(score_node2);

	// Time
	time_element = document.getElementById('time');
	time_element.appendChild(time_node);

	// Ready button
	ready_element = document.getElementById('ready');
	ready_element.appendChild(ready_node);

	// Usernames
	left_username_element = document.getElementById('left_username');
	if (left_username_element != null)
		left_username_element.appendChild(left_username_node);
	right_username_element = document.getElementById('right_username');
	if (right_username_element != null)
		right_username_element.appendChild(right_username_node);
}
