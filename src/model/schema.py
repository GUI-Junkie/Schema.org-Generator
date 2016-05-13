"""
Model of the |Model View Controller| |external_link|

Contains the classes for the

* Hierarchy

* Schemas
"""
from pickle import load
from threading import Thread
from time import sleep
from urllib.error import URLError
from urllib.request import urlopen

# Constants
HIERARCHY_FILE = 'Hierarchy.pickle'
PROPERTY_TYPES = {'Date', 'URL', 'Number', 'Integer', 'Text', 'Boolean', 'Time', 'DateTime'}
READ_BINARY = 'rb'
WRITE_BINARY = 'wb'
SCHEMA_ORG = 'http://schema.org/'
# SCHEMA_ORG = 'http://webschemas.org/'

class Hierarchy:
    """
    Class:  Hierarchy

    Goal:   Get the whole hierarchy of Schema.org

    * _schemas contains the actual schemas

    * _hierarchy contains a list of lists to maintain the same order as Schema.org

    * _property_types contains the input types

    * _version check to see whether a new version of Schema.org has been published
    """

    def __init__(self):
        FILE_NAME = 'model/schema.py'
        if __file__ != FILE_NAME:
            BASE_DIR = __file__[:__file__.index(FILE_NAME)]

        self._schemas = {}  # Dictionary for rapid access
        self._hierarchy = []  # Hierarchy, list of lists for ordering output
        self._property_types = PROPERTY_TYPES  # Set of basic properties that should be rendered as inputs
        self._version = 0.0  # Version of Schema.org

        try:
            # First load the existing HIERARCHY_FILE
            with open('{0}{1}'.format(BASE_DIR, HIERARCHY_FILE), READ_BINARY) as f:
                pickle_list = load(f)

            # HIERARCHY_FILE is created by schema_bot
            self._version = pickle_list[0]
            self._schemas = pickle_list[1]
            self._hierarchy = pickle_list[2]

        except FileNotFoundError:
            # HIERARCHY_FILE does not exist, shut down
            exit('HIERARCHY_FILE does not exist')

    def get_schema(self, thing):
        """
        Public function to obtain one schema

        :param thing: string, name of the schema to retrieve

        :return: schema
        """
        try:
            # Get the schema from the dictionary
            return self._schemas[thing]
        except KeyError:
            raise SchemaNotFoundError

    def get_hierarchy(self, breadcrumb):
        if 'Thing' == breadcrumb:
            return self._hierarchy[1], ''

        if '.' in breadcrumb:
            parents = breadcrumb.split('.')
        else:
            parents = '.'.join(self._schemas[breadcrumb].get_parent_class[0])
            parents = parents.split('.')
            parents.append(breadcrumb)

        hierarchy = self._hierarchy
        for x in range(0, len(parents)):
            # Walk the hierarchy until found
            hierarchy = hierarchy[hierarchy.index(parents[x]) + 1]

        return hierarchy, '.'.join(parents)

    @property
    def hierarchy(self):
        """
        Public function to obtain the hierarchy

        :return: hierarchy- list
        """
        return self._hierarchy


class SchemaClass:
    """
    Class:  SchemaClass

    Goal:   Get the properties and property types of a schema

    * _html (can) contain the html of the schema

    * parent contains a list of parents (complete with hierarchy)

    * properties contains the properties and property types

    * name

    * _callback optional callback function for thread-safety (used by the |Schema bot|)

    * is_alive indicator for the |Schema bot|
    """
    def __init__(self, thing, callback=None, url=SCHEMA_ORG):
        self._html = ''
        self.parent = None
        self.properties = {}
        self.name = thing
        self._callback = callback   # callback from the schema bot
        self.is_alive = False       # Indicator for the schema bot
        self.url = url

    def clean(self):
        """
        Class method used before dump to reduce the size of the pickle file
        """
        self._html = ''
        self._callback = None

    @property
    def get_parent_class(self):
        """
        Class method to get all parents of one schema used by |Schema bot| to create the hierarchy

        :return: list of lists
        """
        return self.parent

    def start(self, b_immediate=False):
        """
        Tries to get Schema from file

        Otherwise, tries to get it from Internet

        :param b_immediate: Optional, if ``True`` will force ``join()`` on the Thread
        """
        if self._html:
            return

        try:
            with open('Schemas/{0}.html'.format(self.name)) as f:
                self._html = f.read()

            # If this is an unknown Schema, analyze the _html
            if self.parent is None:
                self.generator_callback()
        except FileNotFoundError:
            # If this is a schema without .html file, create one
            s_gen = SchemaClassGenerator(self.name, self.generator_callback, self.url)

            self.is_alive = True    # Indicator for the schema bot
            s_gen.start()           # Start the thread
            if b_immediate:         # When called by get_schema_body, it's True
                s_gen.join()        # Join the thread immediately

    def generator_callback(self, s_gen=None):
        """
        Method called by the SchemaClassGenerator after finishing

        * is_alive becomes False
        * the html gets analyzed
        * if there is a callback, it's called (from |Schema bot|)

        :param s_gen: the SchemaClassGenerator or nothing
        """
        self.is_alive = False
        if s_gen is not None:
            self._html = s_gen.html

        # Obtain the parent from self._html
        self._get_parent_class()

        # Obtain the properties from self._html
        self._get_properties()

        # If it's a thread, try to callback
        if s_gen is None:
            return

        if self._callback is None:
            return

        # Keep on calling the callback until it's free
        while not self._callback(self.name):
            sleep(0.1)

    def get_schema_body(self):
        """
        Method called by |SchemaView.show_schema_properties|

        :return: html

        .. |SchemaView.show_schema_properties| raw:: html

            SchemaView.<a class="reference internal"
            href="view.html#view.schema_view.SchemaView.show_schema_properties">show_schema_properties</a>

        """
        if '' == self._html:
            self.start(True)
        return self._html

    def _get_properties(self):
        # <div id="mainContent" vocab="http://schema.org/" typeof="rdfs:Class" resource="http://schema.org/Thing">
        # if 'typeof="rdfs:Class"' not in self._html
        if None is self._html:
            return

        if 'id="mainContent"' not in self._html:
            return  # Incorrect - unlikely

        ind = 0
        # Obtain the properties
        while True:
            key = 'None'
            prop = 'None'
            types = []
            try:
                # <tr typeof="rdfs:Property" resource="http://schema.org/additionalType">
                ind += self._html[ind:].index('rdfs:Property')      # We're looking for the properties
                ind_end = ind + self._html[ind:].index('</tr>')     # We want to extract the property types as well
                ind += self._html[ind:].index('resource=')          # We want to extract the resource link
                ind += self._html[ind:].index('"') + 1              # resource="http://etc"
                # Now, we have the property
                prop = self._html[ind:ind + self._html[ind:].index('"')]

                # <code property="rdfs:label"><a href="/additionalType">additionalType</a></code>
                ind += self._html[ind:].index('rdfs:label')                 # Get the label
                ind += self._html[ind:].index('href=')                      # Skip the link
                ind += self._html[ind:].index('>') + 1                      # Start of the content >
                key = self._html[ind:ind + self._html[ind:].index('<')]     # End of the content <

                # Now we have the property, let's get the property type(s)
                # Unlike Highlander, there can be more than only one
                while ind < ind_end:
                    # <tr typeof="rdfs:Property" resource="http://schema.org/additionalType">
                    ind += self._html[ind:].index('property="rangeIncludes"')  # We're looking for the property_types
                    if ind < ind_end:
                        ind += self._html[ind:].index('">') + 2                 # property="rangeIncludes">URL</a>
                        # Now, we have the property type
                        property_type = self._html[ind:ind + self._html[ind:].index('<')]

                        types.append(property_type)

                # Just in case we overshoot
                ind = ind_end
                self.properties[key] = [prop, types]
            except ValueError:
                # Add last key
                self.properties[key] = [prop, types]
                # print(self.properties)
                return  # Escape While True loop

    def _get_parent_class(self):
        # Check if unknown Thing
        if self.name is None:
            return False

        if not isinstance(self._html, str):
            return False

        self.parent = []
        try:
            ind = 0
            while True:
                # All Schemas inherit from Thing
                ind += self._html[ind:].index('href="/Thing">Thing</a> &gt;')
                ind += self._html[ind:].index('&gt;')

                # There may be multiple parents :-/
                span = ind
                span += self._html[ind:].index('</span>')
                # <span class='breadcrumbs'>
                #   <a   href="/Thing">Thing</a> &gt;
                #   <a   href="/CreativeWork">CreativeWork</a> &gt;
                #   <a   href="/SoftwareApplication">SoftwareApplication</a> &gt;
                #   <a   href="/VideoGame">VideoGame</a>
                # </span>
                span = self._html[:span].rindex('&gt;')
                parent = ['Thing']
                while ind < span:
                    ind += self._html[ind:].index('href=')
                    ind += self._html[ind:].index('"') + 2  # href="/CreativeWork"
                    if ind < span:
                        parent.append(self._html[ind:ind + self._html[ind:].index('"')])

                # Add the parent [] to the instance variable self.parent
                self.parent.append(parent)
        except ValueError:
            return  # Escape While True loop


class SchemaClassGenerator(Thread):
    """
    Class:  SchemaClassGenerator

    Goal:   Get the markup of a schema thread-safe. This class can be started concurrently by the |Schema bot|

    * html from URL after ``decode("utf-8")``
    * name of the schema
    * callback from SchemaClass
    """
    def __init__(self, thing, generator_callback, url):
        super().__init__()
        self.html = None
        self.name = thing
        self._generator_callback = generator_callback
        self._url = url

    def run(self):
        """
        Start the thread

        Get the schema markup from the Internet

        Call the SchemaClass back when done
        """
        self._get_schema()
        self._generator_callback(self)

    def _get_schema(self):
        # Try to get the schema a number of times
        # If it fails, raise an error
        i_tries = 0
        url_error = None

        # Try to get the URL a number of times
        # Failure raises an error
        while i_tries < 9 and self.html is None:
            i_tries += 1
            try:
                if self._url != SCHEMA_ORG:
                    pass

                with urlopen('{0}{1}'.format(self._url, self.name)) as req:
                    self.html = req.read().decode("utf-8")

                # Strip the superfluous <html> from the text
                self.html = self._get_schema_body

                with open('Schemas/{0}.html'.format(self.name), 'w') as f:
                    f.write(self.html)
            except URLError as e:
                # Wait a millisecond before trying again
                print('Sleeping {0}'.format(self.name))
                sleep(0.1)
                url_error = e

        if '' == self.html:
            print('Error in SchemaClassGenerator.get_schema')
            raise url_error

    @property
    def _get_schema_body(self):
        # Only keep the mainContent div
        # Discard the rest
        ind = self.html.index('<div id="mainContent"')
        l_ind = self.html.rindex('</body>')
        return self.html[ind:l_ind]

class SchemaNotFoundError(Exception):
    pass
