$(document).ready(function() {
    if($('#id_distraction-duration')){
        var input = $( "#id_distraction-duration" );
        if(input.value <= 60){
           input.value = 1
        }
        var slider = $( "<div id='slider'></div>" ).insertAfter( input ).slider({
            min: 60,
            max: 7200,
            range: "min",
            value: input.value + 1,
            slide: function( event, ui ) {
                input.value = ui.value - 1;
            }
        });
        $( "#id_distraction-duration" ).change(function() {
            slider.slider( "value", this.selectedIndex + 1 );
        });
    }
});
