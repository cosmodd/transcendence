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

	// Créer un nouvel élément info
	let newInfoElement = document.createElement('div');
	newInfoElement.textContent = event[ServerAPI.DATA_INFO_TYPE_MESSAGE];

	// Ajouter la classe unique pour décaler le démarrage de l'animation
	newInfoElement.classList.add('info', 'info_message');

	// Ajouter l'élément au document
	document.body.appendChild(newInfoElement);

	// Supprimer l'élément après la fin de l'animation
	newInfoElement.addEventListener('animationend', function() {
		newInfoElement.remove();
	});
}

function PrintInfoError(event) 
{
	console.log(event);

	// Créer un nouvel élément info
	let newInfoElement = document.createElement('div');
	newInfoElement.textContent = event[ServerAPI.DATA_INFO_TYPE_ERROR];

	// Ajouter la classe unique pour décaler le démarrage de l'animation
	newInfoElement.classList.add('info', 'info_error');

	// Ajouter l'élément au document
	document.body.appendChild(newInfoElement);

	// Supprimer l'élément après la fin de l'animation
	newInfoElement.addEventListener('animationend', function() {
		newInfoElement.remove();
	});
}
