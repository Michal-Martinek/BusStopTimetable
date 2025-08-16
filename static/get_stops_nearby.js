
function outputText(text) {
	const outpDiv = document.querySelector("#nearby-stops .results")
	outpDiv.innerHTML = text;
}
function renderStops(response) {
	var count = (response.match(/station-item/g) || []).length;
	console.log(`Got ${count} nearby stops`)
	outputText(response)
}
function positionCallback(position, moreStops=false) {
	const coords = {
		latitude: position.coords.latitude,
		longitude: position.coords.longitude
	};
	// TODO check good data
	console.log("Measured coords:", coords);

	const currCount = document.querySelectorAll('#nearby-stops .results .station-item').length;
	const newCount = Math.max(currCount + 5 * moreStops, 7);
	let url = `/get_stops_nearby?lat=${coords['latitude']}&lon=${coords['longitude']}&count=${newCount}`;
	fetch(url, {
		method: "GET",
	})
	.then(response => response.text())
	.then(response => renderStops(response))
	.catch(err => console.error("Error sending coords:", err))
	.finally(() => document.getElementById('nearby-stops').classList.remove('fetching'));
};

function getStopsNearby(moreStops) {
	if ("geolocation" in navigator) {
		navigator.geolocation.getCurrentPosition(
			(loc) => positionCallback(loc, moreStops),
			function (error) {
				outputText("Error getting location <i>(zkontrolujte povolení GPS)</i><br>" + error);
			}
		);
	} else {
		outputText("Geolocation not supported");
	}
}
function refreshNearbyStops(moreStops=false) {
	let div = document.getElementById('nearby-stops')
	if (div.classList.contains('fetching')) return;
	div.classList.add('fetching');
	getStopsNearby(moreStops);
}

addEventListener("DOMContentLoaded", (event) => {
	refreshNearbyStops();
});
