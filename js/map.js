$( document ).ready( function(){
	function parseResp( resp ) {
		var estTime = document.createElement( 'p' );
		estTime.innerHTML = '<b>It will take you approximately ' + resp.rows[ 0 ].elements[ 0 ].duration.text + ' to drive to Oceanside Pier View South</b>';
		estTime.setAttribute( 'class', 'estTime' );
		$( estTime ).hide();
		$( '.timeButton' ).before( $( estTime ) );
		$( estTime ).fadeIn( 500 );
	}
	function distanceMatrix( longitude, latitude ) {
		var queryString = latitude.toString() + ',' + longitude.toString(),
			dest = 'Oceanside+Pier+CA+92054',
			xhr = new XMLHttpRequest(),
			resp;
			xhr.open( 'GET', 'api?origins=' + queryString, true );
			xhr.onreadystatechange = function() {
				if ( xhr.readyState === 4 ) {
					resp = JSON.parse( xhr.responseText );
					parseResp( resp );
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