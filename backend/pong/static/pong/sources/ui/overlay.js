import ServerAPI from "../websocket/server_api.js";

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

ready_element.addEventListener('click', () => {
	if (ready_node.nodeValue === "Searching...")
		return ;

	ready_element.classList.remove("btn-warning");
	ready_element.classList.add("btn-success");
	ServerAPI.SendReadyState()
	ReadyButtonHide();
});

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