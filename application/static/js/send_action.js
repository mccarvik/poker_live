
function send_action() {
    /*
    * This function will continuously loop waiting for messages from the server
    * The http call will connect and disconnect from the server each time a msg is received
    * The ajax will block waiting for the success function to run
    * Client will have to know when its his turn by seeing if turn = his id #
    * This is when the loop will break as no msg could be received now and when an
    * action is taken it will restart the loop
    */
    var act = 'ch';
    var bet = '0';
    console.log('Enter action function');
    var breaker = false;
    var turn = 1;
    while (true) {
        var template_returned = false;
        $.ajax({
            type: 'GET',
            url: '/action',
            data: {
                action: act,
                bet: bet },
        }).done(function(data) {
            console.log('Finished');
            if (data['turn'] === turn) {
                    breaker=true;
            }
            template_returned = true;
        });
        console.log('call');
        if (!template_returned || breaker) {
            break;
        }
    }
}