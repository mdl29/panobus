$(document).ready(function() {
	$("#preloader").hide();
    $('#fullpage').fullpage({
		anchors: ['pres', 'doc', 'map', 'parten'],
		sectionsColor: ['#FF0000', '#800080', '#1E90FF', '#FFFF00'],
		menu: "#menu",
		css3: true
	});
});
