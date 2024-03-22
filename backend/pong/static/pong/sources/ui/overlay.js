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

export let ready_element = document.getElementById('ready')
let ready_node = document.createTextNode('Ready ?')
ready_element.appendChild(ready_node)
ready_element.addEventListener('click', () => {
	ready_element.classList.toggle("btn-success");
	ready_element.classList.toggle("btn-warning");
	ServerAPI.SendReadyState()
});