"""
View of the |Model View Controller| |external_link|

Contains the class for the

- SchemaView
"""
# Refer to the Readme.txt file for © copyright information

from model.schema import PROPERTY_TYPES
from urllib.parse import unquote_plus

HIERARCHY_FILE = 'view/hierarchy.tpl'
TOP_LEVEL = 0
ALL_LEVELS = 1


# .buttons a {color:#4C3441;text-decoration:none;text-align:center;display:block;border-radius:12px;border:2px solid #4CAF50;padding-left:initial;}

def frequent_things(Thing):
    """

    :type Thing: String indicating the Thing
    """
    item = 'description'
    txt = '\t<div class="tr_even">\n'
    # txt += '<div class="tr_odd">\n'
    txt += '<div class="td">\n'
    txt += '<a href="{0}{1}" target="_blank">{1} ' \
           '<img src="/external_link.png" alt="external link" title="external link" />' \
           '</a>\n'.format('http://schema.org/', item)
    txt += '</div>\n'
    txt += '<div class="td">\n'
    txt += '<a href="http://schema.org/Text" target="_blank">Text ' \
           '<img src="/external_link.png" alt="external link" title="external link" /></a>\n'
    txt += '<input type="text" name="{0}_{1}_{2}" />\n'.format(Thing, item, 'Text')
    txt += '</div>\n'
    txt += '</div>\n'  # Close row

    item = 'image'
    txt += '<div class="tr_odd">\n'
    txt += '<div class="td">\n'
    txt += '<a href="{0}{1}" target="_blank">{1} ' \
           '<img src="/external_link.png" alt="external link" title="external link" />' \
           '</a>\n'.format('http://schema.org/', item)
    txt += '</div>\n'
    txt += '<div class="td">\n'
    txt += '<a href="http://schema.org/Text" target="_blank">Text ' \
           '<img src="/external_link.png" alt="external link" title="external link" /></a>\n'
    txt += '<input type="text" name="{0}_{1}_{2}" />\n'.format(Thing, item, 'ImageObject')
    txt += '</div>\n'
    txt += '</div>\n'  # Close row
    item = 'image - second property'
    txt += '<div class="tr_odd">\n'
    txt += '<div class="td">\n'
    txt += '&nbsp;'
    txt += '</div>\n'
    txt += '<div class="td">\n'
    txt += '<a href="javascript:ShowNextSchema(\'ImageObject\', \'{0}_image_ImageObject\', 10000);">ImageObject</a>\n'.format(Thing)
    txt += '<div class="td_property" id="{0}_image_ImageObject"></div>\n'.format(Thing)
    txt += '</div>\n'
    txt += '</div>\n'  # Close row

    item = 'name'
    txt += '\t<div class="tr_even">\n'
    # txt += '<div class="tr_odd">\n'
    txt += '<div class="td">\n'
    txt += '<a href="{0}{1}" target="_blank">{1} ' \
           '<img src="/external_link.png" alt="external link" title="external link" />' \
           '</a>\n'.format('http://schema.org/', item)
    txt += '</div>\n'
    txt += '<div class="td">\n'
    txt += '<a href="http://schema.org/Text" target="_blank">Text ' \
           '<img src="/external_link.png" alt="external link" title="external link" /></a>\n'
    txt += '<input type="text" name="{0}_{1}_{2}" />\n'.format(Thing, item, 'Text')
    txt += '</div>\n'
    txt += '</div>\n'  # Close row

    item = 'potentialAction'
    # txt += '\t<div class="tr_even">\n'
    txt += '<div class="tr_odd">\n'
    txt += '<div class="td">\n'
    txt += '<a href="{0}{1}" target="_blank">{1} ' \
           '<img src="/external_link.png" alt="external link" title="external link" />' \
           '</a>\n'.format('http://schema.org/', item)
    txt += '</div>\n'
    txt += '<div class="td">\n'
    txt += '<a href="http://schema.org/Text" target="_blank">Text ' \
           '<img src="/external_link.png" alt="external link" title="external link" /></a>\n'
    txt += '<input type="text" name="{0}_{1}_{2}" />\n'.format(Thing, item, 'Text')
    txt += '</div>\n'
    txt += '</div>\n'  # Close row

    item = 'url'
    txt += '\t<div class="tr_even">\n'
    # txt += '<div class="tr_odd">\n'
    txt += '<div class="td">\n'
    txt += '<a href="{0}{1}" target="_blank">{1} ' \
           '<img src="/external_link.png" alt="external link" title="external link" />' \
           '</a>\n'.format('http://schema.org/', item)
    txt += '</div>\n'
    txt += '<div class="td">\n'
    txt += '<a href="http://schema.org/URL" target="_blank">URL ' \
           '<img src="/external_link.png" alt="external link" title="external link" /></a>\n'
    txt += '<input type="text" name="{0}_{1}_{2}" />\n'.format(Thing, item, 'URL')
    txt += '</div>\n'
    txt += '</div>\n'  # Close row
    return txt


class SchemaView:
    def __init__(self, version, cloud=True):
        self.version = version
        self.cloud = cloud

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
        txt = '<input type="hidden" name="breadcrumb" id="breadcrumb" value="" />\n'
        txt += self._traverse_hierarchy(hierarchy, TOP_LEVEL)
        txt += '<h4>Full hierarchy</h4>\n'
        txt += self._traverse_hierarchy(hierarchy, ALL_LEVELS)

        with open(HIERARCHY_FILE) as f:
            html = f.read()
        return html.format(title='Hierarchy', buttons='', version=self.version, form=txt, output='')

    def _traverse_hierarchy(self, list_hierarchy, level):
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
                if list_hierarchy[x + 1]:
                    if level:
                        # txt += self._traverse_lvl(list_hierarchy[x + 1], breadcrumb, level)
                        txt += self._traverse_hierarchy(list_hierarchy[x + 1], level)
                    else:
                        txt += self._traverse_lvl(list_hierarchy[x + 1], breadcrumb)
                x += 2
                txt += '</li>\n'
            txt += '</ul>\n'
        return txt

    @staticmethod
    def _traverse_lvl(list_hierarchy, breadcrumb, level=TOP_LEVEL):
        """
        method: Lists all Hierarchy elements
                Recursive
        :param list_hierarchy:
        :return:txt (same txt)
        """
        txt = ''
        if TOP_LEVEL == level:
            # list_hierarchy contains pairs of elements and lists of children ['Thing', []]
            if not breadcrumb:
                breadcrumb = 'Thing'
            txt = '<h4>Sublevel:</h4>\n'

        num_elements = len(list_hierarchy)
        if num_elements:
            x = 0
            half = num_elements / 2

            while x < num_elements:
                if TOP_LEVEL == level:
                    txt += '<ul class="properties">\n'
                else:
                    txt += '<ul>\n'
                while x < half:
                    txt += '<li>\n'
                    # txt += '<a href="/{0}">{0}</a>\n'.format(list_hierarchy[x])
                    if TOP_LEVEL == level:
                        txt += '<a href="javascript:ShowNextLevel(\'{0}\', \'{1}\');">{0}</a>\n' \
                            .format(list_hierarchy[x], breadcrumb)
                    else:
                        txt += '<a href="{0}">{0}</a>\n'.format(list_hierarchy[x])
                    x += 2
                    txt += '</li>\n'
                txt += '</ul>\n'
                half = num_elements
        return txt

    @staticmethod
    def ajax_properties(schema, web_hierarchy, first_use, id=-1):
        """
        Class method: creates a section of HTML with the properties of the ``schema``

        :param id: The id of the select (id becomes id+1)
        :param first_use: If it's the first call, add the most frequent properties from Thing
        :param schema: SchemaClass
        :param web_hierarchy: the id of the hierarchy
        :return: html <li></li>
        """
        id += 1
        txt = '<div class="table">\n'
        if first_use:
            txt += frequent_things(schema.name)
        # txt += '\t<div class="tr_even">\n'
        txt += '\t<div class="tr_odd">\n'
        txt += '\t\tAdd property: <select id="select_' + str(id) + '" onchange="javascript:SelectionChange(' + str(id) + ');">\n'
        txt += '<option value="--">--</option>\n'

        properties = sorted(schema.properties)
        x = 0
        while x < len(properties):
            types = schema.properties[properties[x]]
            # {{types}} to insert the types later
            txt += '<option value="{0}{1};{2}_{3}_{4}||{{types}}">{1}</option>\n' \
                .format(types[0], properties[x], web_hierarchy, properties[x], 'Text')

            output_types = ''
            for a_type in types[1]:
                name = '{0}_{1}_{2}'.format(web_hierarchy, properties[x], a_type)
                if a_type not in PROPERTY_TYPES:
                    if output_types:
                        output_types += ','
                    output_types += '{0};{1}'.format(a_type, name)
            txt = txt.format_map({'types': output_types})
            x += 1
        txt += '\t\t</select>\n'
        txt += '\t</div>\n'
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
        try:
            with open('schemas/{0}_{1}.txt'.format(schema.name, breadcrumb)) as f:
                txt = f.read()
        except FileNotFoundError:
            txt = '<input type="hidden" name="path" value="{0}" />\n'.format(schema.name)
            txt += '<input type="hidden" name="type" id="type" value="" />\n'
            txt += '<input type="hidden" name="breadcrumb" id="breadcrumb" value="" />\n'

            txt += self._breadcrumbs(schema)

            txt += self._traverse_lvl(list_hierarchy, breadcrumb)
            txt += self._buttons()

            txt += '<h4>Properties: {0}</h4>\n'.format(schema.name)
            txt += self.ajax_properties(schema, schema.name, True)
            txt += '<br />\n'
            txt += self._buttons()
            if self.cloud:
                with open('schemas/{0}_{1}.txt'.format(schema.name, breadcrumb), 'w') as f:
                    f.write(txt)

        with open(HIERARCHY_FILE) as f:
            html = f.read()
        return html.format(title=schema.name, buttons="schema", version=self.version, form=txt, output='')

    @staticmethod
    def _buttons():
        txt = '<div class="buttons">\n'
        txt += '    <ul>\n'
        txt += '        <li>\n'
        txt += '            <span>Generate:</span>\n'
        txt += '            <a href="javascript:GenerateSchema(\'Microdata\');">Microdata</a>\n'
        txt += '            <a href="javascript:GenerateSchema(\'RDFa\');">RDFa</a>\n'
        txt += '            <a href="javascript:GenerateSchema(\'JSON\');">JSON-LD</a>\n'
        txt += '        </li>\n'
        txt += '    </ul>\n'
        txt += '</div>\n'
        # Maybe one day add Roles
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
                    txt += '<div itemprop="{0}" itemscope itemtype="{1}{2}">\n' \
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
            txt += '<span itemprop="{0}">{1}</span>\n' \
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
        return html.format(title='Generated Schema', buttons='', version=self.version, form=txt, output=txt_output)
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
            txt += '<span property="{0}">{1}</span>\n' \
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
        return html.format(title='Generated Schema', buttons='', version=self.version, form=txt, output=txt_output)
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
                    txt += ',\n'
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
        txt += self._close_brackets(current_lvl, 1)
        txt += '\n}\n'
        txt += '</script>\n'
        txt += '</textarea>'

        txt_output = '<p>'
        txt_output += 'You can check the generated Schema <a href="https://developers.google.com/structured-data/' \
                      'testing-tool/" target="_blank">here</a>.'
        txt_output += '</p>'

        with open(HIERARCHY_FILE) as f:
            html = f.read()
        return html.format(title='Generated Schema', buttons='', version=self.version, form=txt, output=txt_output)
        # FIN generate_json

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

    @staticmethod
    def _breadcrumbs(schema):
        # Add the Canonical URL
        txt = 'Canonical URL: <a href="http://schema.org/{0}" target="_blank">http://schema.org/{0} ' \
              '<img src="/external_link.png" alt="external link" title="external link" />' \
              '</a><br/><br/>\n'.format(schema.name)

        # Add all breadcrumbs with Schema.org syntax
        for parents in schema.get_parent_class:
            count = 0
            for parent in parents:
                count += 1
                if 1 == count:
                    txt += '<ol class="breadcrumb" itemscope itemtype="http://schema.org/BreadcrumbList">\n'
                else:
                    txt += '    <li> > </li>\n'

                txt += '    <li itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem">\n'
                txt += '        <a itemprop="item" href="/{0}"><span itemprop="name">{0}</span></a>\n'.format(parent)
                txt += '        <meta itemprop="position" content="{0}" />\n'.format(count)
                txt += '    </li>\n'

            txt += '</ol>\n'
        txt += '<br/>\n'
        return txt
