function onLoad(arg)
{
    var li;

    // Onload doesn't have an argument when index.html
    // for schema's, it does
    if("schema" == arg)
    {
        // default style.display for all buttons is "None"
        li = document.getElementById("GenerateButton");
        li.style.display = "";

        // Don't show the Save button if the browser does not support local storage
        if("undefined" == typeof(Storage))
            return;
        li = document.getElementById("SaveButton");
        li.style.display = "";
    }

    // Don't continue if the browser does not support local storage
    if("undefined" == typeof(Storage))
        return;

    // If localStorage has information, show buttons
    if(localStorage.length)
    {
        li = document.getElementById("RecoveryButton");
        li.style.display = "";

        li = document.getElementById("ClearButton");
        li.style.display = "";
    }
}

function getRequest()
{
    if(window.XMLHttpRequest) // code for IE7+, Firefox, Chrome, Opera, Safari
        return new XMLHttpRequest();

    // code for IE6, IE5
    return new ActiveXObject("Microsoft.XMLHTTP");
}

function ShowNextSchema(schema, id)
{
    // Get the next level with AJAX (but only once)
    var div = document.getElementById(id);

    // If the level has already been obtained, show/hide
    if(div.innerHTML.length)
    {
        if(div.style.display == "block")
            div.style.display = "none";
        else
            div.style.display = "block";

        return;
    }

    // This code gets executed only once per level
    var params = "next_element=" + schema + "&id=" + id;

    var http = getRequest();

    // Prepare the request
    http.open("POST", schema, true);

    // Prepare the proper header information to send along with the request
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    http.setRequestHeader("Content-length", params.length);
    http.setRequestHeader("Connection", "close");

    // Prepare function for asynchronous reception
    http.onreadystatechange=function()
    {
        if (http.readyState==4 && http.status==200)
        {
            div.innerHTML=http.responseText;
            div.style.display = "block";
        }
    }

    // Send the request
    http.send(params);
}

function AddRole(id)
{
    // Get the next level with AJAX (but only once)
    var div = document.getElementById("role_" + id);

    // If the level has already been obtained, show/hide
    if(div.innerHTML.length)
    {
        if(div.style.display == "block")
            div.style.display = "none";
        else
            div.style.display = "block";

        return;
    }

    var http = getRequest();

    // Prepare the request
    http.open("POST", "AddRoles", true);

    // Prepare the proper header information to send along with the request
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    params = '';
    http.setRequestHeader("Content-length", params.length);
    http.setRequestHeader("Connection", "close");

    // Prepare function for asynchronous reception
    http.onreadystatechange=function()
    {
        if (http.readyState==4 && http.status==200)
        {
            div.innerHTML=http.responseText;
            div.style.display = "block";
        }
    }

    // Send the request
    http.send(params);
}

function AddRoleTo(id, property)
{
    // Get the next level with AJAX (but only once)
    var div = document.getElementById("role_" + id);
    div.style.display = "none";
}

function ShowNextLevel(schema, breadcrumb)
{
    var ele = document.getElementById("breadcrumb");
    ele.value = breadcrumb + '.' + schema;
    document.forms[0].action = '/' + schema;
    document.forms[0].submit();
}

function GenerateSchema(type)
{
    // Save the Schema before submitting it
    SaveSchema(false);

    // Set the type
    var ele = document.getElementById("type");
    ele.value = type;
    document.forms[0].submit();
}

function SaveSchema(clicked)
{
    // Clear local storage
    localStorage.clear();

    // This function can only be called if the browser supports local storage
    // Save the entire page, this doesn't store values
    localStorage.setItem("SaveSchema", document.documentElement.innerHTML);

    var form = document.forms[0];
    var i;

    // Save values, but only the form elements with information
    for(i=0; i<form.length; i++)
        if(form.elements[i].value.length && form.elements[i].name.length)
            localStorage.setItem(form.elements[i].name, form.elements[i].value);

    // Show a nice message after saving to local storage
    if(clicked)
    {
        form = document.getElementById('saved');
        form.style.display = ""
        setTimeout(function()
        {
            form = document.getElementById('saved');
            form.style.display = "None";
        }, 3000);
    }
}

function RecoverData()
{
    // This function can only be called if there is local storage
    // Restore the saved page without values
    document.documentElement.innerHTML = localStorage.getItem("SaveSchema");
    var i;
    // Restore all values of the saved form elements
    for(i=0; i<localStorage.length; i++)
        if(localStorage.key(i) !== "SaveSchema")
            document.getElementsByName(localStorage.key(i))[0].value = localStorage.getItem(localStorage.key(i));

    // Show the Clear Button
    var li = document.getElementById("ClearButton");
    li.style.display = "";
}

function ClearData()
{
    // Clear local storage
    localStorage.clear();

    // Hide the buttons associated with local storage
    var li = document.getElementById("RecoveryButton");
    li.style.display = "None";

    li = document.getElementById("ClearButton");
    li.style.display = "None";
}

// jQuery for Schema.org content 'Examples' for the tabs to work
// Copied from Schema.org
$(document).ready(function()
{
    setTimeout(function()
    {
        $(".atn:contains(itemscope), .atn:contains(itemtype), .atn:contains(itemprop), \
            .atn:contains(itemid), .atn:contains(time), .atn:contains(datetime), \
            .atn:contains(datetime), .tag:contains(time) ").addClass('new');
        $('.new + .pun + .atv').addClass('curl');
    }, 500);

    setTimeout(function()
    {
        $(".atn:contains(property), .atn:contains(typeof) ").addClass('new');
        $('.new + .pun + .atv').addClass('curl');
    }, 500);

    setTimeout(function()
    {
        $('.ds-selector-tabs .selectors a').click(function()
        {
            var $this = $(this);
            var $p = $this.parents('.ds-selector-tabs');
            $('.selected', $p).removeClass('selected');
            $this.addClass('selected');
            $('pre.' + $this.data('selects'), $p).addClass('selected');
        });
    }, 0);
});
