$(document).ready(function() {
	if (!(/Android|iPhone|iPad|iPod|BlackBerry|Windows Phone/i).test(navigator.userAgent || navigator.vendor || window.opera)) {
		$.getScript("/static/ln2xsite/plugins/youtube-player/src/jquery.mb.YTPlayer.min.js", function(){
	        $(".player").YTPlayer();
		});
	}
});
