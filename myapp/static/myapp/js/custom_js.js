console.log('js loaded')
$(function() {

    console.log( "ready!" );
     $('.date-own').datepicker({
              format: "yyyy",
            viewMode: "years",
            minViewMode: "years",
            orientation: "auto"

           });
});




