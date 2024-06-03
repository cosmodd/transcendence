import ServerAPI from "../websocket/server_api.js";

export function PrintInfo(event)
{
	switch (event[ServerAPI.DATA_INFO_TYPE]) {
		case ServerAPI.DATA_INFO_TYPE_MESSAGE:
			PrintInfoMessage(event[ServerAPI.DATA_INFO_TYPE_MESSAGE]);
			break;
		case ServerAPI.DATA_INFO_TYPE_ERROR:
			PrintError(event[ServerAPI.DATA_INFO_TYPE_ERROR]);
			break;
		default:
			break;
	}
}

export function PrintInfoMessage(message) 
{
	console.log(message);

	document.querySelectorAll('.info').forEach(element => {
		element.remove();
	});

	let newInfoElement = document.createElement('div');
	newInfoElement.textContent = message;
	newInfoElement.classList.add(...('alert info border-none bg-primary m-3'.split(/\s/g)));
	document.body.appendChild(newInfoElement);

	newInfoElement.addEventListener('animationend', function() {
		newInfoElement.remove();
	});
}

export function PrintError(error) 
{
	console.log(error);

	document.querySelectorAll('.info').forEach(element => {
		element.remove();
	});

	let newInfoElement = document.createElement('div');
	newInfoElement.textContent = error;
	newInfoElement.classList.add(...('alert info border-none bg-danger m-3'.split(/\s/g)));
	document.body.appendChild(newInfoElement);

	newInfoElement.addEventListener('animationend', function() {
		newInfoElement.remove();
	});
}
