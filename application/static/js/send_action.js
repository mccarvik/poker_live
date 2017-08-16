
function send_action() {
    console.log('Found Function');
    $.ajax({
        type: 'GET',
        url: '/action',
        data: {
            action: "get_data" },
        success: function()
        {
            console.log('Finished');
        },
    });
}