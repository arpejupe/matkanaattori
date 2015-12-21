$(function() {
    var calendars = $('#additional_calendars');
    var max_fields = 5; 
    var add_button = $('#add_calendar')
    var x = 1;
    $(add_button).click(function(e){
        e.preventDefault();
        if(x < max_fields){
            $(calendars).append('<input type="text" name="calendar_url" value=""/>');
            x++;
        }
    });
    
    // Insert date to footer
    var date = new Date();
    var year = date.getFullYear()  
    $("#date").append(year);
});
