$( document ).ready( function(){
	function parseResp( resp ) {
		
	}
	function distanceMatrix( longitude, latitude ) {
		var queryString = longitude.toString() + ',' + latitude.toString(),
			dest = 'Oceanside+Pier+CA+92054',
			xhr = new XMLHttpRequest(),
			resp;
			xhr.open( 'GET', 'http://maps.googleapis.com/maps/api/distancematrix/json?origins=' + queryString + '&destinations=' + dest + '&mode=bicycling&language=en-EN&sensor=false', true );
			xhr.onreadystatechange = function() {
				if ( xhr.readyState === 4 ) {
					resp = JSON.parse( xhr.responseText );
					
				}
			};
			xhr.send();
	}
	function showPosition( position ) {
		distanceMatrix( position.coords.longitude, position.coords.latitude );
	}
	navigator.geolocation.getCurrentPosition(showPosition);
});