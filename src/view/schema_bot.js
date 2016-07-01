function onLoad()
{
    setTimeout(function(){CheckResult();}, 1000);
}

function CheckResult()
{
    // Get the next level with AJAX (but only once)
    var div = document.getElementById("result");

    // This code gets executed only once per level
    var params = "check=true";

    var http;
    if(window.XMLHttpRequest) // code for IE7+, Firefox, Chrome, Opera, Safari
        http=new XMLHttpRequest();
    else    // code for IE6, IE5
        http=new ActiveXObject("Microsoft.XMLHTTP");

    // Prepare the request
    http.open("POST", "/schema_bot", true);

    // Prepare the proper header information to send along with the request
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    http.setRequestHeader("Content-length", params.length);
    http.setRequestHeader("Connection", "close");

    // Prepare function for asynchronous reception
    http.onreadystatechange=function()
    {
        if (http.readyState==4 && http.status==200)
        {
            if(http.responseText === "Busy")
            {
                div.innerHTML+="."
                setTimeout(function(){CheckResult();}, 5000);
            }
            else
                div.innerHTML=http.responseText;
        }
    }

    // Send the request
    http.send(params);
}
