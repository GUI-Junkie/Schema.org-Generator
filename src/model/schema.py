"""
Model of the |Model View Controller| |external_link|

Contains the classes for the

* Hierarchy

* Schemas
"""
from pickle import load

# Constants
HIERARCHY_FILE = 'Hierarchy.pickle'
PROPERTY_TYPES = {'Date', 'URL', 'Number', 'Integer', 'Text', 'Boolean', 'Time', 'DateTime'}
READ_BINARY = 'rb'
WRITE_BINARY = 'wb'
FILE_NAME = 'model/schema.py'
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
        base_dir = ''
        if __file__ != FILE_NAME:
            base_dir = __file__[:__file__.index(FILE_NAME)]

        self._version = 0.0  # Version of Schema.org
        self._schemas = {}  # Dictionary for rapid access
        self._hierarchy = []  # Hierarchy, list of lists for ordering output
        self._property_types = PROPERTY_TYPES  # Set of basic properties that should be rendered as inputs

        try:
            # First load the existing HIERARCHY_FILE
            with open('{0}{1}'.format(base_dir, HIERARCHY_FILE), READ_BINARY) as f:
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
            parents = self._schemas[breadcrumb].get_parent_class[0]
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
    """
    def __init__(self, thing):
        self._html = ''
        self.parent = None
        self.properties = {}
        self.name = thing
        self.url = SCHEMA_ORG

    @property
    def get_parent_class(self):
        """
        Class method to get all parents of one schema used by |Schema bot| to create the hierarchy

        :return: list of lists
        """
        return self.parent


class SchemaNotFoundError(Exception):
    pass
