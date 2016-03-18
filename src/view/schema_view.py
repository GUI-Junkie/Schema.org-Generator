"""
View of the |Model View Controller| |external_link|

Contains the class for the

- SchemaView
"""

from model.schema import PROPERTY_TYPES
from urllib.parse import unquote_plus

HIERARCHY_FILE = 'view/hierarchy.html'


class SchemaView:
    """
    SchemaView class handles all output creating valid HTML
    """
    def get_index(self, hierarchy):
        """
        Class method: Gets the html for the full hierarchy
                Calls the recursive private function _traverse_hierarchy

        :param hierarchy: The list of lists that's the full hierarchy
        :return: index.html
        """
        txt = ''
        txt = self._traverse_hierarchy(txt, hierarchy)

        with open(HIERARCHY_FILE) as f:
            html = f.read()
        return html.format(title='Hierarchy', buttons='', form=txt, output='')

    def _traverse_hierarchy(self, txt, list_hierarchy):
        """
        method: Lists all Hierarchy elements
                Recursive
        :param txt:
        :param list_hierarchy:
        :return:txt (same txt)
        """
        # list_hierarchy contains pairs of elements and lists of children ['Thing', []]
        if len(list_hierarchy):
            txt += '<ul>\n'
            x = 0
            while x < len(list_hierarchy):
                txt += '<li>\n'
                txt += '<a href="/{0}">{0}</a>\n'.format(list_hierarchy[x])
                # Recursive call
                txt = self._traverse_hierarchy(txt, list_hierarchy[x + 1])
                x += 2
                txt += '</li>\n'
            txt += '</ul>\n'
        return txt

    @staticmethod
    def ajax_properties(schema, web_hierarchy):
        """
        Class method: creates a section of HTML with the properties of the ``schema``

        :param schema: SchemaClass
        :param web_hierarchy: the id of the hierarchy
        :return: html <li></li>
        """
        txt = ''
        properties = sorted(schema.properties)
        if len(properties):
            txt += '<ul>\n'
            x = 0
            while x < len(properties):
                txt += '<li>\n'
                txt += '<a href="http://schema.org/{0}" target="_blank">{0} ' \
                       '<img src="external_link.png" alt="" /></a>\n'.format(properties[x])
                types = schema.properties[properties[x]]
                txt += '<ul>\n'
                for a_type in types[1]:
                    txt += '<li>\n'
                    # If the type is a basic type, let the user fill it out
                    name = '{0}_{1}_{2}'.format(web_hierarchy, properties[x], a_type)
                    if a_type in PROPERTY_TYPES:
                        txt += '<a href="http://schema.org/{0}" target="_blank">{0} ' \
                               '<img src="external_link.png" alt="" /></a>\n'.format(a_type)

                        # TODO For bonus points, the input could be checked according to the specific types
                        # Not going down that road
                        txt += '<input type="text" name="{0}" />\n'.format(name)
                    else:  # Div placeholder for AJAX property
                        txt += '<a href="javascript:ShowNextSchema(\'{0}\', \'{1}\')">{0}</a>\n'.format(a_type, name)
                        txt += '<div id="{0}"></div>'.format(name)
                    txt += '</li>\n'
                txt += '</ul>\n'
                x += 1
                txt += '</li>\n'
            txt += '</ul>\n'
        return txt

    def show_schema_properties(self, schema):
        """
        Class method: Creates top level output for a schema

        :param schema: SchemaClass
        :rtype: str - html
        """
        txt = '<input type="hidden" name="path" value="{0}" />'.format(schema.name)
        txt += self.ajax_properties(schema, schema.name)
        txt += '<input type="submit" value="Show Schema" />'

        with open('view/schema_header.html') as f:
            schema_txt = f.read()
        schema_txt += schema.get_schema_body()

        with open(HIERARCHY_FILE) as f:
            html = f.read()
        return html.format(title=schema.name, buttons="schema", form=txt, output=schema_txt)

    def generate_schema_output(self, schema_name, ctx):
        """
        Generate the valid Schema. This can be validated on Google Developers
        |Structured Data Testing Tool| |external_link|

        The properties with data get placed in their respective divs

        :param ctx: Context with the Query_string arguments
        :type schema_name: str
        """
        txt = '<textarea style="width:90%;height:50em">\n'
        txt += '<div itemscope itemtype="http://schema.org/{0}">\n'.format(schema_name)
        current_div_levels = [schema_name]
        current_lvl = 1

        # Sorted to group all levels correctly
        keys = sorted(ctx.get_keys())
        for p in keys:
            key_divs = p.split('_')  # 'TieAction_additionalType_URL'

            # Skip the QUERY_STRING items that are not part of the schema
            if schema_name != key_divs[0]:
                continue

            # schema, subschema, property, type
            # 0,      1,         -2,       -1
            key_lvl = len(key_divs) - 1
            current_lvl = len(current_div_levels)

            # Sanity check
            # If this key is shorter than the previous, close levels
            if current_lvl * 2 > key_lvl:
                txt += self._close_tabs(current_lvl, int(key_lvl / 2))
                current_div_levels = current_div_levels[:int(key_lvl / 2)]
                current_lvl = len(current_div_levels)

            # For all current levels, check if the current key is at the same level
            # if not, add one level to the current one
            for i in range(0, current_lvl):
                j = 2 * i
                if current_div_levels[i] != key_divs[j]:
                    # Close previous divs
                    txt += self._close_tabs(current_lvl, i)
                    current_div_levels = current_div_levels[:i]
                    current_lvl = len(current_div_levels)

                    # Open next div
                    current_div_levels.append(key_divs[j])
                    txt += '\t' * current_lvl
                    txt += '<div itemprop={0} itemscope itemtype="http://schema.org/{1}">\n'.format(key_divs[j - 1],
                                                                                                    key_divs[j])
                    current_lvl += 1

            # If this key has more levels than the current level
            # add more levels
            while key_lvl > current_lvl * 2:
                # Open next div
                j = current_lvl * 2
                current_div_levels.append(key_divs[j])
                txt += '\t' * current_lvl
                txt += '<div itemprop={0} itemscope itemtype="http://schema.org/{1}">\n'.format(key_divs[j - 1],
                                                                                                key_divs[j])
                current_lvl += 1

            # Add the key / value
            # Sanitize output
            txt += '\t' * current_lvl
            txt += '<span itemprop="{0}">{1}</span>\n'.format(key_divs[-2],
                                                              unquote_plus(ctx.get(p)).replace('</textarea', ''))

        # After the last key, close all divs
        txt += self._close_tabs(current_lvl)
        txt += '</textarea>'

        txt_output = '<p>'
        txt_output += 'You can check the generated Schema <a href="https://developers.google.com/structured-data/' \
                      'testing-tool/" target="_blank">here</a>.'
        txt_output += '</p>'

        with open(HIERARCHY_FILE) as f:
            html = f.read()
        return html.format(title='Generated Schema', buttons='', form=txt, output=txt_output)

    @staticmethod
    def get_saved_output():
        """
        Class method for UX experience. Shows the schema has effectively been stored in LocalStorage

        :return: str
        """
        with open(HIERARCHY_FILE) as f:
            html = f.read()

        txt_output = '<p>'
        txt_output += 'The Schema has been saved in Local Storage'
        txt_output += '</p>'

        return html.format(title='Saved', buttons='', form='', output=txt_output)

    @staticmethod
    def _close_tabs(lvl, i_low_level=0):
        """
        Adds the number of closing divs required.

        :param lvl: int
        :param i_low_level: int (optional)
        :return: txt: str
        """
        txt = ''
        while lvl > i_low_level:
            lvl -= 1
            txt += '\t' * lvl
            txt += '</div>\n'
        return txt
