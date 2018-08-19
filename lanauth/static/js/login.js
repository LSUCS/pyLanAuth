

function get_url_param(sParam, default_val=null)
{
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++)
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam)
        {
            return sParameterName[1];
        }
    }
    return default_val;
}​

/**
 *  Check the current auth state of the user
 */
function check() {

    // Status constants
    const STATUS_NO_AUTH = 0
    const STATUS_PENDING = 1
    const STATUS_AUTH    = 2

    $.get("/api/check",
        function(response) {
            var status_code = response.status;
            
            switch(status_code) {
                case STATUS_NO_AUTH:
                    $("#info, #login-form").show(500);
                    break;
                case STATUS_PENDING:
                    $('#login-form').hide(500);
                    $('#pending').show(500);
                    setTimeout(function() { check(); }, 5000);
                    break;
                default:
                    $("#login-form, #pending").hide(500);
                    $("#authenticated").show(500);
                    setTimeout(function() {
                        window.location = get_url_param("url", "http://lan.lsucs.org.uk/index.php?page=account");
                    }, 3000);
            }
        },
        'json');
}

/**
 *  Attempt to authenticate the form against the API
 */
function auth() {

    // Status constants
    const STATUS_PASS = 0
    const STATUS_FAIL = 1

    $.post(
        "/api/auth", {
            username: $("#username").val(),
            password: $("#password").val(),
            seat: $("#seat").val(),
            wifi_id: get_url_param("id")
            wifi_site: get_url_param("site")
        },
        function (response) {
            if (response.status == STATUS_PASS) {
                check();
                setTimeout(function() {
                    check();
                }, 3000);
            
            }
            else {
                if (response.error) {
                    $('#error-text').text(response.error)               
                    $('#error').show();                    
                }
            }
        },
        'json');
}

/* Initialise login page */
$(document).ready(function() {

    // Hide elements
    $('#login-form').hide();
    $('#pending').hide();
    $('#authenticated').hide();
    $('#error').hide();

    $("#login-form").submit(function(event) {
        event.preventDefault();
        console.log("LOGIN!");
        auth();
    });

    
    // Check the users authentication status
    check();
});
