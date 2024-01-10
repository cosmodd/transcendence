import ServerAPI from "../websocket/server_api.js";

export function PrintInfo(event)
{
	switch (event[ServerAPI.DATA_INFO_TYPE]) {
		case ServerAPI.DATA_INFO_TYPE_MESSAGE:
			PrintInfoMessage(event);
			break;
		case ServerAPI.DATA_INFO_TYPE_ERROR:
			PrintInfoError(event);
			break;
		default:
			break;
	}
}

function PrintInfoMessage(event) 
{
	console.log(event);

	// Supprimer tous les éléments de classe "info" existants
	document.querySelectorAll('.info').forEach(element => {
		element.remove();
	});

	let newInfoElement = document.createElement('div');
	newInfoElement.textContent = event[ServerAPI.DATA_INFO_TYPE_MESSAGE];
	newInfoElement.classList.add('info', 'info_message');
	document.body.appendChild(newInfoElement);

	newInfoElement.addEventListener('animationend', function() {
		newInfoElement.remove();
	});
}

function PrintInfoError(event) 
{
	console.log(event);

	// Supprimer tous les éléments de classe "info" existants
	document.querySelectorAll('.info').forEach(element => {
		element.remove();
	});

	let newInfoElement = document.createElement('div');
	newInfoElement.textContent = event[ServerAPI.DATA_INFO_TYPE_ERROR];
	newInfoElement.classList.add('info', 'info_error');
	document.body.appendChild(newInfoElement);

	newInfoElement.addEventListener('animationend', function() {
		newInfoElement.remove();
	});
}

export function PrintError(error) 
{
	console.log(error);

	// Supprimer tous les éléments de classe "info" existants
	document.querySelectorAll('.info').forEach(element => {
		element.remove();
	});

	let newInfoElement = document.createElement('div');
	newInfoElement.textContent = error;
	newInfoElement.classList.add('info', 'info_error');
	document.body.appendChild(newInfoElement);

	newInfoElement.addEventListener('animationend', function() {
		newInfoElement.remove();
	});
}
