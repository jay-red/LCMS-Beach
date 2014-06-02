$( document ).ready( function() {
	$( 'iframe' ).load( function() {
		var $form = $( 'iframe' ).contents().find( '#ss-form' ),
			$submit = $( 'iframe' ).contents().find( '#ss-submit' ),
			xhr = new XMLHttpRequest(),
			fname = '';

		$submit.on( 'click', function( e ) {
			var $fname = $( 'iframe' ).contents().find( '#entry_2015244640' );
			fname = $fname.val();
			console.log( fname );
			if( fname !== '' ) {
				xhr.open( 'GET', 'rsvpForm?fname=' + fname, true );
				xhr.send();
			}
		});

		console.log( $fname = $( 'iframe' ).contents().find( 'h1' )[0].innerHTML );
	});
});