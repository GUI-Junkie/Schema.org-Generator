"""
View of the |Model View Controller| |external_link|

Contains the class for the

- SchemaView
"""
# Refer to the Readme.txt file for © copyright information

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
        txt = '<input type="hidden" name="breadcrumb" id="breadcrumb" value="" />'
        txt += self._traverse_hierarchy(hierarchy)

        with open(HIERARCHY_FILE) as f:
            html = f.read()
        return html.format(title='Hierarchy', buttons='', form=txt, output='')

    def _traverse_hierarchy(self, list_hierarchy):
        """
        method: Lists all Hierarchy elements
                Recursive
        :param list_hierarchy:
        :return:txt (same txt)
        """
        # list_hierarchy contains pairs of elements and lists of children ['Thing', []]
        txt = ''
        if len(list_hierarchy):
            txt += '<ul>\n'
            x = 0
            breadcrumb = list_hierarchy[0]
            while x < len(list_hierarchy):
                txt += '<li>\n'
                txt += '<a href="/{0}">{0}</a>\n'.format(list_hierarchy[x])
                # Recursive call
                # txt = self._traverse_hierarchy(list_hierarchy[x + 1])
                txt += self._traverse_lvl(list_hierarchy[x + 1], breadcrumb)
                x += 2
                txt += '</li>\n'
            txt += '</ul>\n'
        return txt

    @staticmethod
    def _traverse_lvl(list_hierarchy, breadcrumb):
        """
        method: Lists all Hierarchy elements
                Recursive
        :param list_hierarchy:
        :return:txt (same txt)
        """
        # list_hierarchy contains pairs of elements and lists of children ['Thing', []]
        if not breadcrumb:
            breadcrumb = 'Thing'
        breadcrumbs = breadcrumb.split('.')
        h4 = ''
        for crumb in breadcrumbs:
            if h4 != '':
                h4 += ' - '
            h4 += '<a href="/{0}">{0}</a>'.format(crumb)

        txt = '<h4>Sublevel: {0}</h4>'.format(h4)
        num_elements = len(list_hierarchy)
        if num_elements:
            x = 0
            half = num_elements / 2

            while x < num_elements:
                txt += '<ul class="properties">\n'
                while x < half:
                    txt += '<li>\n'
                    # txt += '<a href="/{0}">{0}</a>\n'.format(list_hierarchy[x])
                    txt += '<a href="javascript:ShowNextLevel(\'{0}\', \'{1}\');">{0}</a>\n'\
                        .format(list_hierarchy[x], breadcrumb)
                    x += 2
                    txt += '</li>\n'
                txt += '</ul>\n'
                half = num_elements
        return txt

    @staticmethod
    def ajax_properties(schema, web_hierarchy):
        """
        Class method: creates a section of HTML with the properties of the ``schema``

        :param schema: SchemaClass
        :param web_hierarchy: the id of the hierarchy
        :return: html <li></li>
        """
        txt = '<div class="table">\n'
        properties = sorted(schema.properties)
        if len(properties):
            x = 0
            while x < len(properties):
                if x % 2:
                    txt += '<div class="tr_odd">\n'
                else:
                    txt += '<div class="tr_even">\n'
                txt += '<div class="td">\n'
                txt += '<a href="{0}{1}" target="_blank">{1} ' \
                       '<img src="/external_link.png" alt="external link" title="external link" />' \
                       '</a>\n'.format(schema.url, properties[x])
                types = schema.properties[properties[x]]
                txt += '</div>\n'
                txt += '<div class="td">\n'
                txt += '<a href="http://schema.org/Text" target="_blank">Text ' \
                       '<img src="/external_link.png" alt="external link" title="external link" /></a>'
                txt += '<input type="text" name="{0}_{1}_{2}" />\n'.format(web_hierarchy, properties[x], 'Text')
                txt += '</div>\n'

                for a_type in types[1]:
                    # If the type is a basic type, let the user fill it out
                    name = '{0}_{1}_{2}'.format(web_hierarchy, properties[x], a_type)
                    if a_type not in PROPERTY_TYPES:
                        txt += '<div class="td">\n'
                        # Div placeholder for AJAX property
                        txt += '<a href="javascript:ShowNextSchema(\'{0}\', \'{1}\');">{0}</a>\n'.format(a_type, name)
                        txt += '<div class="td_property" id="{0}"></div>'.format(name)
                        txt += '</div>\n'
                x += 1
                txt += '</div>\n'
        txt += '</div>\n'
        return txt

    def show_schema_properties(self, schema, list_hierarchy, breadcrumb):
        """
        Class method: Creates top level output for a schema

        :param schema: SchemaClass
        :param list_hierarchy:
        :param breadcrumb:
        :rtype: str - html
        """
        txt = '<input type="hidden" name="path" value="{0}" />'.format(schema.name)
        txt += '<input type="hidden" name="type" id="type" value="" />'
        txt += '<input type="hidden" name="breadcrumb" id="breadcrumb" value="" />'

        txt += self._traverse_lvl(list_hierarchy, breadcrumb)
        txt += self._buttons(0)

        txt += '<h4>Properties: {0}</h4>'.format(schema.name)
        txt += self.ajax_properties(schema, schema.name)
        txt += '<br />'
        txt += self._buttons(1)

        with open('view/schema_header.html') as f:
            schema_txt = f.read()
        schema_txt += schema.get_schema_body()

        with open(HIERARCHY_FILE) as f:
            html = f.read()
        return html.format(title=schema.name, buttons="schema", form=txt, output=schema_txt)

    @staticmethod
    def _buttons(id):
        txt = '<div class="buttons">'
        txt += '    <ul>'
        txt += '        <li>'
        txt += '            <span>Generate:</span>'
        txt += '            <a href="javascript:GenerateSchema(\'Microdata\');">&nbsp;&nbsp;&nbsp;&nbsp;Microdata</a>'
        txt += '            <a href="javascript:GenerateSchema(\'RDFa\');">&nbsp;&nbsp;&nbsp;&nbsp;RDFa</a>'
        txt += '            <a href="javascript:GenerateSchema(\'JSON\');">&nbsp;&nbsp;&nbsp;&nbsp;JSON-LD</a>'
        txt += '        </li>'
        txt += '    </ul>'
        txt += '</div>'
        # txt += '<div class="buttons">'
        # txt += '    <ul>'
        # txt += '        <li>'
        # txt += '            <span>Add:</span>'
        # txt += '            <a href="javascript:AddRole({0});">&nbsp;&nbsp;&nbsp;&nbsp;Role to...</a>'.format(id)
        # txt += '        </li>'
        # txt += '    </ul>'
        # txt += '</div>'
        # txt += '<div id="role_{0}">'.format(id)
        # txt += '</div>'
        return txt

    def generate_microdata(self, schema, ctx):
        """
        Generate the valid Schema. This can be validated on Google Developers
        |Structured Data Testing Tool| |external_link|

        The properties with data get placed in their respective divs

        :param ctx: Context with the Query_string arguments
        :type schema: Schema
        """
        schema_name = schema.name
        txt = '<textarea>\n'
        txt += '<div itemscope itemtype="{0}{1}">\n'.format(schema.url, schema_name)
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
                    txt += '<div itemprop="{0}" itemscope itemtype="{1}{2}">\n'\
                        .format(key_divs[j - 1], schema.url, key_divs[j])
                    current_lvl += 1

            # If this key has more levels than the current level
            # add more levels
            while key_lvl > current_lvl * 2:
                # Open next div
                j = current_lvl * 2
                current_div_levels.append(key_divs[j])
                txt += '\t' * current_lvl
                txt += '<div itemprop="{0}" itemscope itemtype="{1}{2}">\n' \
                    .format(key_divs[j - 1], schema.url, key_divs[j])
                current_lvl += 1

            # Add the key / value
            # Sanitize output
            txt += '\t' * current_lvl
            txt += '<span itemprop="{0}">{1}</span>\n'\
                .format(key_divs[-2], unquote_plus(ctx.get(p)).replace('</textarea', ''))

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
        # Fin generate_microdata

    def generate_rdfa(self, schema, ctx):
        """
        Generate the valid Schema. This can be validated on Google Developers
        |Structured Data Testing Tool| |external_link|

        The properties with data get placed in their respective divs

        :param ctx: Context with the Query_string arguments
        :type schema: Schema
        """
        schema_name = schema.name
        txt = '<textarea>\n'
        txt += '<div vocab="{0}" typeof="{1}">\n'.format(schema.url, schema_name)
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
                    txt += '<div property="{0}" typeof="{1}">\n'.format(key_divs[j - 1], key_divs[j])
                    current_lvl += 1

            # If this key has more levels than the current level
            # add more levels
            while key_lvl > current_lvl * 2:
                # Open next div
                j = current_lvl * 2
                current_div_levels.append(key_divs[j])
                txt += '\t' * current_lvl
                txt += '<div property="{0}" typeof="{1}">\n'.format(key_divs[j - 1], key_divs[j])
                current_lvl += 1

            # Add the key / value
            # Sanitize output
            txt += '\t' * current_lvl
            txt += '<span property="{0}">{1}</span>\n'\
                .format(key_divs[-2], unquote_plus(ctx.get(p)).replace('</textarea', ''))

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
        # Fin generate_rdfa

    def generate_json(self, schema, ctx):
        """
        Generate the valid Schema. This can be validated on Google Developers
        |Structured Data Testing Tool| |external_link|

        The properties with data get placed in their respective brackets

        :param ctx: Context with the Query_string arguments
        :type schema: Schema
        """
        schema_name = schema.name
        txt = '<textarea>\n'
        txt += '<script type="application/ld+json">\n'
        txt += '{\n'
        # txt += '\t"@context": "{0}",\n'.format(schema.url)
        txt += '\t"@context": "http://schema.org/",\n'
        txt += '\t"@type": "{0}"'.format(schema_name)
        current_bracket_levels = [schema_name]
        current_lvl = 1

        # Sorted to group all levels correctly
        keys = sorted(ctx.get_keys())
        for p in keys:
            key_brackets = p.split('_')  # 'TieAction_additionalType_URL'

            # Skip the QUERY_STRING items that are not part of the schema
            if schema_name != key_brackets[0]:
                continue

            # schema, subschema, property, type
            # 0,      1,         -2,       -1
            key_lvl = len(key_brackets) - 1
            current_lvl = len(current_bracket_levels)

            # Sanity check
            # If this key is shorter than the previous, close levels
            if current_lvl * 2 > key_lvl:
                txt += self._close_brackets(current_lvl, int(key_lvl / 2))
                current_bracket_levels = current_bracket_levels[:int(key_lvl / 2)]
                current_lvl = len(current_bracket_levels)

            # For all current levels, check if the current key is at the same level
            # if not, add one level to the current one
            for i in range(0, current_lvl):
                j = 2 * i
                if current_bracket_levels[i] != key_brackets[j]:
                    # Close previous brackets
                    txt += self._close_brackets(current_lvl, i)
                    current_bracket_levels = current_bracket_levels[:i]
                    current_lvl = len(current_bracket_levels)

                    # Open next bracket
                    current_bracket_levels.append(key_brackets[j])
                    txt += '\t' * (current_lvl + 1)
                    txt += '"{0}": {{\n'.format(key_brackets[j - 1])
                    txt += '\t' * (current_lvl + 2)
                    txt += '"@type": "{0}"'.format(key_brackets[j])
                    current_lvl += 1

            # If this key has more levels than the current level
            # add more levels
            while key_lvl > current_lvl * 2:
                # Open next bracket
                j = current_lvl * 2
                current_bracket_levels.append(key_brackets[j])
                txt += ',\n'
                txt += '\t' * (current_lvl + 1)
                txt += '"{0}": {{\n'.format(key_brackets[j - 1])
                txt += '\t' * (current_lvl + 2)
                txt += '"@type": "{0}"'.format(key_brackets[j])
                current_lvl += 1

            # Add the key / value
            # Sanitize output
            txt += ',\n'
            txt += '\t' * (current_lvl + 1)
            txt += '"{0}":"{1}"'.format(key_brackets[-2], unquote_plus(ctx.get(p)).replace('</textarea', ''))

        # After the last key, close all brackets
        txt += self._close_brackets(current_lvl)
        txt += '\n}\n'
        txt += '</script>\n'
        txt += '</textarea>'

        txt_output = '<p>'
        txt_output += 'You can check the generated Schema <a href="https://developers.google.com/structured-data/' \
                      'testing-tool/" target="_blank">here</a>.'
        txt_output += '</p>'

        with open(HIERARCHY_FILE) as f:
            html = f.read()
        return html.format(title='Generated Schema', buttons='', form=txt, output=txt_output)
        # FIN generate_json

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
    def get_schema_bot_ajax(schema_bot):
        # Maybe the schema has not been started
        # This is not the place to start it
        if None is schema_bot:
            return 'Schema bot not started'

        # Check the status
        if schema_bot.is_alive():
            return 'Busy'

        # Finished, let's check for errors
        if schema_bot.error:
            return schema_bot.error

        if schema_bot.updated:
            # This is the good stuff
            # Update the hierarchy and go on your merry way
            return 'Finished - Updated to schema.org version {0}'.format(schema_bot.version)

        # False alarm, the version is unchanged
        return 'Finished - nothing there, still schema.org version {0}'.format(schema_bot.version)

    @staticmethod
    def get_schema_bot_html():
        with open('view/schema_bot.html') as f:
            return f.read()

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

    @staticmethod
    def _close_brackets(lvl, i_low_level=0):
        """
        Adds the number of closing divs required.

        :param lvl: int
        :param i_low_level: int (optional)
        :return: txt: str
        """
        txt = ''
        while lvl > i_low_level:
            txt += '\n'
            txt += '\t' * lvl
            txt += '}'
            lvl -= 1
        return txt
