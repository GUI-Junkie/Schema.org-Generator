#!/usr/bin/python3
from pickle import dump
from os import remove, listdir
from urllib.error import HTTPError
from urllib.request import urlopen

from model.schema import SchemaClass

HIERARCHY_FILE = 'Hierarchy.pickle'
WRITE_BINARY = 'wb'

debug = 'Dentist'
# debug = 'ProfessionalService'


class Thing:
    """
    Small substitute class for the SchemaClass
    Info will be copied to the real class
    """
    def __init__(self, thing):
        self.name = thing       # The name of the schema
        self.parents = []       # This will contain all the direct parents
        self.real_parents = []  # This will contain all parents up to 'Thing'
        self.properties = []    # This will contain the properties (duh)
        self.url = ''

    def add_parent(self, parent):
        """
        Nothing here. Append parent
        :param parent:
        :return:
        """
        self.parents.append(parent)

    def add_property(self, prop):
        """
        Nothing here. Append property
        :param prop:
        :return:
        """
        if prop not in self.properties:
            self.properties.append(prop)


def parse_class(line):
    """
    Get the class name from the line. It's in the first column
    :param line:
    :return:
    """
    # <http://schema.org/DiscoverAction> <http://www.w3.org/2000/01/rdf-schema#subClassOf>
    #           <http://schema.org/FindAction> <http://schema.org/#v3.0> .
    ind = line.index('>')        # Get the end of the first column
    ind = line[:ind].rindex('/') + 1    # From here to the end
    return line[ind:ind + line[ind:].index('>')]


def parse_link(line):
    """
    Get the external link of the property
    :param line:
    :return:
    """
    # <http://schema.org/tongueWeight> <http://schema.org/rangeIncludes>
    #       <http://schema.org/QuantitativeValue> <http://auto.schema.org/#v3.0> .
    ind = line.index('<') + 1       # Get the beginning of the fourth column
    ind += line[ind:].index('<') + 1
    ind += line[ind:].index('<') + 1

    # rangeIncludes usually has four columns, but not if it's a #comment or a #label
    if not '#comment' in line and not '#label' in line:
        ind += line[ind:].index('<') + 1
    return line[ind:ind + line[ind:].index('#')]


def parse_sub_class(line, subclass='subClassOf'):
    """
    Get the data from the first and the third column, discarding the http link
    :param line:
    :param subclass:
    :return:
    """
    # Only treat the line if it contains the 'subclass'
    if subclass not in line:
        return None, None

    # Get the class name
    this_class = parse_class(line)

    # <http://schema.org/DiscoverAction> <http://www.w3.org/2000/01/rdf-schema#subClassOf>
    #           <http://schema.org/FindAction> <http://schema.org/#v3.0> .
    ind = line.index(subclass)      # We're interested in what comes after subclassof
    ind += line[ind:].index('>') + 1    # We're interested in what lies before the end
    ind += line[ind:].index('>')        # ... of the next column

    ind = line[:ind].rindex('/') + 1    # From here to the end
    # Get the data from the third column
    return this_class, line[ind:ind + line[ind:].index('>')]


def get_real_parents(name, hierarchy):
    """
    Recursive function to get all the parents of the thing (where thing is already a parent) confused?
    This function is called from a preparative function
    :param name:
    :param hierarchy:
    :return: thing.real_parents
    """
    # Return if thing is 'Thing'
    if 'Thing' == name:
        return [[]]

    # If thing already has real_parents, return them
    thing = hierarchy[name]
    if thing.real_parents:
        return thing.real_parents

    # At this point, we know we need to process all parents
    for parent in thing.parents:
        # Recursive call to get all the real_parents of the parent
        real_parents = get_real_parents(parent, hierarchy)

        # Now, we're guaranteed to have all the parents of the parent
        for real_parent in real_parents:
            # As lists are passed by reference, we need to make a copy
            copy = []
            if real_parent:
                # Add the real_parent
                copy += real_parent

            # Add the parent behind the real_parent
            copy.append(parent)

            # Now, we have one real_parent of this thing
            thing.real_parents.append(copy)

    # Now, we have all real_parents of this thing
    return thing.real_parents


def get_parents(hierarchy):
    """
    Get all the real_parents of all things in the hierarchy
    :param hierarchy:
    :return:
    """
    for name in hierarchy:
        get_real_parents(name, hierarchy)


def sort_nested(nested):
    # Sort tuples
    new_nested = []
    for i in range(len(nested)):
        if not i % 2:   # Odd members are text, even members are lists
            new_nested.append(nested[i])

    # Sort the text members
    new_nested = sorted(new_nested)

    ordered = []
    for i in range(len(new_nested)):
        ordered.append(new_nested[i])
        # Recursive call - next level to be sorted
        index = nested.index(new_nested[i]) + 1
        if not nested[index]:
            ordered.append([])
        else:
            ordered.append(sort_nested(nested[index]))

    return ordered


def create_nested_hierarchy(hierarchy):
    nested = ['Thing', []]
    # Create the nested list
    for thing in hierarchy.keys():
        # if thing == debug:
        #     print(thing)
        schema = hierarchy[thing]

        # Order by the longest parent first to prevent not reaching the insertion point or ValueError
        try:
            parents = sorted(schema.real_parents, key=len, reverse=True)
        except TypeError:
            continue

        if not parents:  # Thing has no parents
            continue

        # Every element has Thing at it's root, so it will be found
        # However, the parent we're looking for may be somewhere else, so keep looking
        for x in range(len(parents)):
            sub = nested
            for y in range(len(parents[x])):
                try:
                    # Walk the hierarchy until the insertion point
                    sub = sub[sub.index(parents[x][y]) + 1]
                except ValueError:
                    # If you can't find the parent, add it
                    sub.append(parents[x][y])
                    # if 'Thing' == parents[x][y]:
                    #     print(thing)
                    sub.append([])
                    sub = sub[sub.index(parents[x][y]) + 1]

            # When the insertion point has been reached, add the element
            if sub != nested:
                # Add the element to the hierarchy (if it doesn't exist)
                try:
                    sub = sub[sub.index(schema.name)]
                except ValueError:
                    sub.append(schema.name)
                    sub.append([])

    return sort_nested(nested)


def treat_file(schema_version):
    """
    Open the file, read all the data
        - Create the schemas with parents and properties
        - Create the nested hierarchy
    :return:
    """
    schemas = {}
    properties = {}
    with open('all-layers.nq') as f:
        for line in f:
            # If the line contains the schema, and parent
            thing, ancestor = parse_sub_class(line)
            if thing:
                if thing not in schemas:
                    # Add the schema
                    schemas[thing] = Thing(thing)

                # Now, we're sure the schema exist, add the parent
                schemas[thing].add_parent(ancestor)

            # If the line contains property - property type
            prop, prop_type = parse_sub_class(line, 'rangeIncludes')
            if prop:
                # Get the link
                try:
                    link = parse_link(line)
                except ValueError:
                    print(link)
                try:
                    # Check if the property already exists
                    prop_list = properties[prop]

                    # If it exists, add the type to the types
                    types = prop_list[1]
                    if prop_type not in types:
                        types.append(prop_type)
                except KeyError:
                    # If the property doesn't exist, add it
                    properties[prop] = [link, [prop_type]]

    # Delete the schemas we're not going to show
    unwanted = ['DataType', 'Float', 'Integer', 'URL']
    for name in unwanted:
        try:
            del schemas[name]
        except KeyError:
            print('Unwanted {0} not found'.format(name))

    # Add Thing. Thing has no parents, so it wouldn't be added
    schemas['Thing'] = Thing('Thing')

    # Perform some work to get all the parents. The file only contains the immediate parent
    # We want to have all the parents up to 'Thing'
    # This is needed to create the nested hierarchy and for breadcrumbs etc. later on
    get_parents(schemas)

    # ordered nested hierarchy
    # All the schemas ordered alphabetically and nested
    hierarchy = create_nested_hierarchy(schemas)

    # Go through the file another time
    # Check for orphaned classes
    # Get all the properties
    with open('all-layers.nq') as f:
        for line in f:
            # Sanity check -> see if there are things without subclass
            #   - ignore ['DataType', 'Time', 'Text','URL','Boolean','Float',
            #             'Integer','DataType','Date','DateTime','Number']
            if '#Class' in line:
                thing, something = parse_sub_class(line, '#Class')
                if thing:
                    try:
                        thing = schemas[thing]
                        link = parse_link(line)
                        thing.url = link
                    except KeyError:
                        if thing not in ['DataType', 'Time', 'Text', 'URL', 'Boolean', 'Float',
                                         'Integer', 'DataType', 'Date', 'DateTime', 'Number']:
                            print('Nonexistent: {0}'.format(thing))

            # Get all the properties
            if 'domainIncludes' in line:
                prop, thing = parse_sub_class(line, 'domainIncludes')
                try:
                    thing = schemas[thing]
                    thing.add_property(prop)
                except KeyError:
                    pass

    # Make the SchemaClass used by the program
    _schemas = {}
    for schema in schemas:
        # A new SchemaClass
        tmp = SchemaClass(schema)

        # Get the real parents
        tmp.parent = schemas[schema].real_parents

        # Get the url
        tmp.url = schemas[schema].url

        # Add all the known properties of the schema
        for prop in schemas[schema].properties:
            tmp.properties[prop] = properties[prop]

        # Add all the properties of all the parents
        added_properties = []
        for multiple_parents in tmp.parent:
            for parent in multiple_parents:
                # If the properties have already been added, skip
                if parent not in added_properties:
                    added_properties.append(parent)
                    for prop in schemas[parent].properties:
                        tmp.properties[prop] = properties[prop]

        # Add the schema to the dictionary
        _schemas[schema] = tmp

    # Create the dump file
    with open(HIERARCHY_FILE, WRITE_BINARY) as f:
        dump([schema_version, _schemas, hierarchy], f)


if __name__ == "__main__":
    download = False
    version = 3.3
    if download:
        try:
            with urlopen("https://github.com/schemaorg/schemaorg/blob/sdo-callisto/data/releases/"
                         "{0}/all-layers.nq?raw=true".format(version)) as f:
                txt = f.read()

            with open('all-layers.nq', 'w') as f:
                f.write(txt.decode())
        except HTTPError:
            exit("File not found")

    # Delete index.html
    try:
        remove('view/index.html')
    except FileNotFoundError:
        pass

    # Delete schemas/*.txt files
    for file in listdir("schemas/"):
        if '.txt' in file:
            remove("schemas/{0}".format(file))
        else:
            print('{0} is not a *.txt file in directory schemas'.format(file))

    # Let's do *everything*
    treat_file(version)
