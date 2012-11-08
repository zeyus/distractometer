$(document).ready(function() {
    if($('#id_distraction-duration')){
        var input = $( "#id_distraction-duration" );
        if(parseInt(input.val()) <= 60){
           input.val(60)
        }
        var slider = $( "<div id='slider'></div>" ).insertAfter( input ).slider({
            min: 61,
            max: 7201,
            range: "min",
            value: parseInt(input.val())*60 + 1,
            slide: function( event, ui ) {
                input.val(parseInt((ui.value - 1)/60));
            }
        });
        slider.css('width', '50%').css('margin-left', '10px').css('margin-top','5px');
        $( "#id_distraction-duration" ).change(function() {
            slider.slider( "value", parseInt(this.val()) * 60 + 1 );
        });
    }
});
