$(document).ready(function() {

	$("#preloader").hide();
	
	//fullpage
    $('#fullpage').fullpage({
		anchors: ['pres', 'doc', 'map', 'parten', 'news'],
		sectionsColor: ['#FF0000', '#800080', '#1E90FF', '#FFFF00','#008000'],
		menu: "#menu",
		css3: true,
		normalScrollElements:"#mapLeaflet",
		paddingTop:"6%",
		sectionSelector:"section"
	});
	
	//leaflet
	var map = L.map('mapLeaflet').setView([48.3921,-4.4769], 13);
	
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
		attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);
	
	$.getJSON("js/pano.json", function(json) {
		for (i = 0; i < json.pano.length; i++) {
			L.marker(json.pano[i].pos)
				.addTo(map)
				.bindPopup("<h1>"+json.pano[i].where+"</h1><br>"+json.pano[i].desc);
		}
	});
	
});
