
function outputText(text) {
	const outpDiv = document.querySelector("#nearby-stops .results")
	outpDiv.innerHTML = text;
}
function renderStops(response) {
	var count = (response.match(/station-item/g) || []).length;
	console.log(`Got ${count} nearby stops`)
	outputText(response)
}
function positionCallback(position) {
	const coords = {
		latitude: position.coords.latitude,
		longitude: position.coords.longitude
	};
	// TODO check good data
	console.log("Measured coords:", coords);

	fetch(`/get_stops_nearby?lat=${coords['latitude']}&lon=${coords['longitude']}`, {
		method: "GET",
	})
	.then(response => response.text())
	.then(response => renderStops(response))
	.catch(err => console.error("Error sending coords:", err));
};

function getStopsNearby() {
	if ("geolocation" in navigator) {
		navigator.geolocation.getCurrentPosition(
			positionCallback,
			function (error) {
				outputText("Error getting location <i>(zkontrolujte povolení GPS)</i><br>" + error);
			}
		);
	} else {
		outputText("Geolocation not supported");
	}
}

addEventListener("DOMContentLoaded", (event) => {
	getStopsNearby();
});
