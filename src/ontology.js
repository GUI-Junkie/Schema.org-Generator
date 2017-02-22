function OnLoad()
{
    var inp = document.getElementById("schema_name");
    inp.focus();
}

var lvl = 0;                                                // lvl
var count = 0;                                              // Count

function Add(param)
{
    if(param === "Property")
    {
        var div = document.getElementById("input" + lvl);       // Get the <div>
        AddChild(div, "Property Name:", count, true);
        count++;                                                // +1 on the counter
        AddChild(div, "Property Type:", count, false);
        count++;                                                // +1 on the counter
        AddChild(div, "Property Value:", count, false);
        count++;                                                // +1 on the counter

        // Add remove button
        var inp = document.createElement("button");             // Create a <button> element
        inp.setAttribute("onclick", "javascript:Delete('" + count + "');"); // Set the onclick attribute
        inp.setAttribute("id", "button_" + count);              // Set the id attribute
        var txt = document.createTextNode("-");                 // Create a text node
        inp.appendChild(txt);                                   // Append the text to <Button>
        div.appendChild(inp);                                   // Add the <input> to the <div>

        var br = document.createElement("br");                  // Create a <br> element
        div.appendChild(br);
    }
    else
    {
        lvl++;
        var div = document.getElementById("input");             // Get the <div>
        var sub = document.createElement("div");                // Create a <label> element
        sub.setAttribute("id", "input" + lvl);                  // Set the id attribute

        <!--<label for="schema_name">Schema Name:</label><input type="text" id="schema_name" value="Schema name"><br/><br/>-->
        var lbl = document.createElement("label");              // Create a <label> element
        var txt = document.createTextNode("Schema Name:");      // Create a text node
        lbl.setAttribute("for", "schema_name" + lvl);           // Set the for attribute
        lbl.appendChild(txt);                                   // Append the text to <label>
        sub.appendChild(lbl);                                   // Add the <label> to the <div>

        var inp = document.createElement("input");              // Create a <input> element
        inp.setAttribute("type", "text");                       // Set the type attribute
        inp.setAttribute("id", "schema_name" + lvl);            // Set the id attribute
        sub.appendChild(inp);                                   // Add the <input> to the <div>
        var br = document.createElement("br");                  // Create a <br> element
        sub.appendChild(br);

        div.appendChild(sub);
        inp.focus();
    }
}

function AddChild(div, text, count, focus)
{
    if(text === "Property Type:")
    {
        var lbl = document.createElement("input");              // Create a <label> element
        lbl.setAttribute("type", "hidden");                     // Set the type attribute
        lbl.setAttribute("id", "label_" + count);               // Set the id attribute
    }
    else
    {
        var lbl = document.createElement("label");              // Create a <label> element
        var txt = document.createTextNode(text);                // Create a text node
        lbl.setAttribute("for", "property_" + count);           // Set the for attribute
        lbl.setAttribute("id", "label_" + count);               // Set the id attribute
        lbl.appendChild(txt);                                   // Append the text to <label>
    }
    div.appendChild(lbl);                                       // Add the <label> to the <div>

    var inp = document.createElement("input");                  // Create a <input> element
    if(text === "Property Type:")
        inp.setAttribute("type", "hidden");                     // Set the type attribute
    else
        inp.setAttribute("type", "text");                       // Set the type attribute

    inp.setAttribute("id", "property_" + count);                // Set the id attribute
    if(text === "Property Type:")
        inp.setAttribute("value", "Text");                      // Set the value attribute
    div.appendChild(inp);                                       // Add the <input> to the <div>

    if(focus)
        inp.focus();
}

function Delete(count)
{
    var ele = document.getElementById("button_" + count);
    ele.parentNode.removeChild(ele.nextSibling);                // Remove <br>
    ele.parentNode.removeChild(ele);                            // Romove Button

    count--;
    DeleteChild(count);                                         // Remove all children
    count--;
    DeleteChild(count);
    count--;
    DeleteChild(count);
}

function DeleteChild(count)
{
    ele = document.getElementById("label_" + count);
    ele.parentNode.removeChild(ele);

    ele = document.getElementById("property_" + count);
    ele.parentNode.removeChild(ele);
}

function WalkDiv(div, count, name)
{
    var field = "";
    var form = document.forms[0];
    var ele = null;

    // Recursive
    for(var child=div.firstChild; child!==null; child=child.nextSibling)
    {
        if(child.hasChildNodes())
            WalkDiv(child, count, name);
        else if(child.id)
        {
            if("schema_name" === child.id.substring(0, 11))
            {
                if("schema_name" === child.id)
                {
                    name = child.value;
                    ele = document.getElementById("path");
                    ele.value = child.value;
                }
//                else
//                {
//                console.log(child.id + " - " + child.value);
//                }
            }
            else if("property_" === child.id.substring(0, 9))
            {
                if(0 == count)
                {
                    count++;
                    console.log("Name - " + child.value);
                    field = name + "_" + child.value;
                }
                else if(1 == count)
                {
                    count++;
                    console.log("Type - " + child.value);
                    field += "_" + child.value;
                }
                else if(2 == count)
                {
                    count = 0;
                    console.log("Value - " + child.value);
                    ele = document.createElement("input");  // Create an input node
                    ele.setAttribute("type", "hidden");     // Set the type attribute
                    ele.setAttribute("name", field);        // Set the name attribute
                    ele.setAttribute("value", child.value); // Set the name attribute
                    form.appendChild(ele);                  // Add the <input> to the <form>
                }
            }
            else
                console.log(child.id.substring(0, 9));
         //   console.log(child);
         }
    }
}

function Generate(type)
{
    var ele = document.getElementById("type");
    ele.value = type;

    var inp = document.getElementById("schema_name");
    ele = document.getElementById("path");
    ele.value = inp.value;
    ele.value = ele.value.trim();
    ele.value = ele.value.replace(" ", "_");

    var div = document.getElementById("input");       // Get the <div>
    var count = 0;
    for(var child=div.firstChild; child!==null; child=child.nextSibling)
    {
        if(child.hasChildNodes())
            WalkDiv(child, count, "");
    }

    document.forms[0].submit();
}
