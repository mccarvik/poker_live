
function send_action() {
    /*
    * This function will continuously loop waiting for messages from the server
    * The http call will connect and disconnect from the server each time a msg is received
    * Client will have to know when its his turn by seeing if turn = his id #
    * This is when the loop will break as no msg could be received now and when an
    * action is taken it will restart the loop
    */
    
    console.log('Enter action function');
    var breaker = false;
    var turn = 1;
    var j = 0;
    while (true) {
        $.ajax({
            type: 'GET',
            url: '/action',
            data: {
                action: "get_data" },
            success: function(data)
            {
                if (data['turn'] === turn) {
                    breaker=true;
                }
                console.log('Finished');
            },
        });
        if (breaker) {
            break;
        }
    }
}