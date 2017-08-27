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

function ShowNextSchema(schema, id, select_id)
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
    var params = "next_element=" + schema + "&id=" + id + "&select_id=" + select_id;

    var http = getRequest();

    // Prepare the request
    http.open("POST", schema, true);

    // Prepare the proper header information to send along with the request
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//    http.setRequestHeader("Content-length", params.length);
//    http.setRequestHeader("Connection", "close");

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
    // Don't continue if the browser does not support local storage
    if("undefined" == typeof(Storage))
        return;

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
    // Don't continue if the browser does not support local storage
    if("undefined" == typeof(Storage))
        return;

    // Don't continue if local storage is empty
    if(!localStorage.length)
        return;

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
    // Don't continue if the browser does not support local storage
    if("undefined" == typeof(Storage))
        return;

    // Clear local storage
    localStorage.clear();

    // Hide the buttons associated with local storage
    var li = document.getElementById("RecoveryButton");
    li.style.display = "None";

    li = document.getElementById("ClearButton");
    li.style.display = "None";
}

function SelectionChange(select_id)
{
    /*
    * From the selected element, create the layout for the selected property
    *   - Name (with link), text with field
    *   - additional properties, if there are any
    *   - Delete button
    *   - Div for AJAX level properties
    *
    * <div class="tr_even">
    *   <div class="td">
    *       <a href="http://schema.org/actionStatus" target="_blank">actionStatus <img src="/external_link.png" alt="external link" title="external link" /></a>
    *   </div>
    *   <div class="td">
    *       <a href="http://schema.org/Text" target="_blank">Text <img src="/external_link.png" alt="external link" title="external link" /></a>
    *       <input type="text" name="Action_actionStatus_Text" />
    *   </div>
    * </div>
    * <div class="tr_even">
    *   <div class="td">&nbsp;</div>
    *   <div class="td">
    *       <a href="javascript:ShowNextSchema('ActionStatusType', 'Action_actionStatus_ActionStatusType');">ActionStatusType</a>
    *       <div class="td_property" id="Action_actionStatus_ActionStatusType">
    *       </div>
    *   </div>
    * </div>
    */
    var select = document.getElementById("select_" + select_id);
    if("--" === select.value)
        return;

    var div = select.parentNode;
    var parent = div.parentNode;
    var new_div = document.createElement('div');

    if(div.className === "tr_odd")
    {
        div.className = "tr_even";
        new_div.className = "tr_odd";
    }
    else
    {
        div.className = "tr_odd";
        new_div.className = "tr_even";
    }
    parent.insertBefore(new_div, div);

    // URL;Div || types
    var ele = select.value.split("||");

    // Get the URL and Div
    var left = ele[0].split(";");
    var link = left[0];
    var id = left[1];

    var sub_div = document.createElement('div');
    sub_div.className = "td";

    var a = document.createElement('a');
    a.setAttribute("href", link);
    a.setAttribute("target","_blank");
    a.innerHTML = select.options[select.selectedIndex].text + " <img src=\"/external_link.png\" alt=\"external link\" title=\"external link\" />";

    // Add the link to the sub_div (column)
    sub_div.appendChild(a);

    // Add the subdiv to the new_div (row)
    new_div.appendChild(sub_div);

    // Make sure the select_id is unique
    while(document.getElementById(id + select_id))
        select_id += 1;

    // Add text
    var text = '<div class="td">';
    text += '   <a href="http://schema.org/Text" target="_blank">Text <img src="/external_link.png" alt="external link" title="external link" /></a>';
    text += '   <input type="text" name="' + id + select_id +'" id="' + id + select_id +'" />';
    text += '   <span class="delete_button"><a href="javascript:DeleteDiv(\'' + id + select_id + '\', ' + select_id + ');"> - </a></span>';
    text += '</div>';
    new_div.innerHTML += text;

    // If there are other properties, show them
    left = ele[1].split(",");
    for(var i = 0; i < left.length; i++)
    {
        link = left[i].split(";");
        if(link.length > 1)
        {
            // New row
            new_div = document.createElement('div');

            if(div.className === "tr_odd")
                new_div.className = "tr_even";
            else
                new_div.className = "tr_odd";
            parent.insertBefore(new_div, div);

            text = '<div class="td">&nbsp;</div>';
            text += '<div class="td">';
            text += '   <a href="javascript:ShowNextSchema(\''+ link[0] + '\', \'' + link[1] + '\', ' + select_id + ');">' + link[0] + '</a>';
            text += '   <div class="td_property" id="' + link[1] + '"></div>';
            text += '</div>';
            new_div.innerHTML += text;
        }
    }
}

function DeleteDiv(id, select_id)
{
    var div = document.getElementById(id);
    var parent = div.parentNode;
    div = parent.parentNode;
    var table = div.parentNode;
    var sibling = div.nextElementSibling;

    // Delete all siblings with the same tr_odd or tr_even pattern
    while(sibling.className === div.className)
    {
        table.removeChild(sibling);
        sibling = div.nextElementSibling;
    }
    // Delete the div
    table.removeChild(div);

    // Got to straighten out the odds and evens
    last = "tr_odd"
    for(var child=table.firstChild; child!==null; child=child.nextElementSibling)
    {
        // Ignore undefined children
        if(child.className)
        {
            // If the className is different, cool!
            if(child.className !== last)
                last = child.className;
            // If the className is the same check if it's 'empty'
            else if(child.innerHTML.indexOf("&nbsp;") === -1)
            {
                // Change the row color
                if(last === "tr_odd")
                    last = "tr_even";
                else
                    last = "tr_odd";
                child.className = last;
            }
        }
    }
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
