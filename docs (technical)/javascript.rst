Javascript
==========

Located in the ``view`` subdirectory for development, the ``schema.js`` file should be located at the root of the |Web Server| together with all other static files.

.. code-block:: javascript

    function onLoad(arg)

This function shows the different buttons depending on the situation.

* index.html (arg is empty)
    - the ``Recover Data`` button is shown if the LocalStorage has data
    - the ``Clear Data`` button is shown together with the ``Recover Data`` button
* all other pages (arg is "schema")
    - the ``Save Schema`` button is shown only if LocalStorage is available
    - the ``Generate Schema`` button is shown
    - the ``Recover Data`` button is shown if the LocalStorage has data
    - the ``Clear Data`` button is shown together with the ``Recover Data`` button

.. code-block:: javascript

    function ShowNextSchema(schema, id)

This function will get the next level on the hierarchy through an AJAX call, only once. If the level has already been obtained, it will toggle the display setting between ``None`` and ``Block``

* schema - the next element in the hierarchy
* id - the div where the content is to be shown

.. code-block:: javascript

    function GenerateSchema()

This function only executes the ``submit()`` action of the form, sending all the fields to the |Application Server| through the POST action. A syntactically correct schema.org schema will be returned.

.. code-block:: javascript

    function SaveSchema()

This function can only be called if LocalStorage is available. It will clear the old content of the LocalStorage and then will save all data on screen for later recovery. Then, it will show a confirmation the schema has been saved.

** TODO: The confirmation message might be improved using AJAX instead

.. code-block:: javascript

    function RecoverData()

This function will replace the ``innerHTML`` with the content stored in LocalStorage

.. code-block:: javascript

    function ClearData()

This function will delete the content stored in LocalStorage and hide the ``Recover Data`` and ``Clear Data`` buttons.

.. code-block:: javascript

    $(document).ready(function()

jQuery copied from schema.org. This will show the example tabs of the original schema.org example tabs.
