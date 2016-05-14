$(document).ready(function() {
	//fullpage
    $('#fullpage').fullpage({
		anchors: ['Panobus','pres', 'news','doc', 'map', 'parten','contact'],
		sectionsColor: ['#191919','#352a75', '#423495', '#4f3eb6', '#6857c7','#8477d3','#000000'],
		menu: "#menu",
		css3: true,
		normalScrollElements:"#mapLeaflet",
		paddingTop:"6%",
		sectionSelector:"section",

		//Scrolling
        scrollingSpeed: 700,
        autoScrolling: true,
        fitToSectionDelay: 1000,
        scrollBar: false,
        easing: 'easeInOutCubic',
        easingcss3: 'ease',
        loopBottom: false,
        loopTop: false,
        loopHorizontal: true,
        continuousVertical: false,
        scrollOverflow: false,
        touchSensitivity: 15,
        normalScrollElementTouchThreshold: 15,

		//Design
        controlArrows: true,
        verticalCentered: true,
        resize : false,
        paddingTop: '64px',
        paddingBottom: '20px',
        responsiveWidth: '100px',
        responsiveHeight: '100px',
	});

        $("#preloader").hide();

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
