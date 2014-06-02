$( document ).ready( function(){
	function parseResp( resp ) {
		
	}
	function distanceMatrix( longitude, latitude ) {
		var queryString = latitude.toString() + ',' + longitude.toString(),
			dest = 'Oceanside+Pier+CA+92054',
			xhr = new XMLHttpRequest(),
			resp;
			xhr.open( 'GET', 'http://maps.googleapis.com/maps/api/distancematrix/json?origins=' + queryString + '&destinations=' + dest + '&mode=bicycling&language=en-EN&sensor=false&key=AIzaSyDv_8qcIEBZHqca71PH4pB5kAZKSFG0fP0', true );
			xhr.onreadystatechange = function() {
				if ( xhr.readyState === 4 ) {
					resp = JSON.parse( xhr.responseText );
					
				}
			};
			xhr.send();
	}
	function showPosition( position ) {
		$( '.timeButton' ).fadeOut( 500 );
		distanceMatrix( position.coords.longitude, position.coords.latitude );
	}
	$( '.timeButton' ).click( function(){
		navigator.geolocation.getCurrentPosition(showPosition);
	});
});