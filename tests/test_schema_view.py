#!/usr/bin/python3

from unittest import TestCase, main

from controller import EZContext
from model.schema import Hierarchy, SchemaClass  # , PropertyType
from view.schema_view import SchemaView

TEST_DIR = f'{__file__[:__file__.index("tests")]}tests/test_files/'
WRITE = 'w'


class TestHierarchy(TestCase):
    # changed_files = False
    # changed_files = True

    @classmethod
    def setUpClass(cls):
        cls.hierarchy = Hierarchy()
        cls.view = SchemaView(SCHEMA_VERSION)
        cls.tests = ['micro', 'rdfa', 'json']

    @classmethod
    def tearDownClass(cls):
        cls.view = None
        cls.hierarchy = None
        cls.tests = None

    def test_get_hierarchy(self):
        test_file = f'{TEST_DIR}hierarchy.html'
        txt_html = ''
        if not CHANGED_FILES:
            with open(test_file) as f:
                txt_html = f.read()

        txt = self.view.get_index(self.hierarchy.hierarchy)
        # If the output doesn't coincide, there may be another version of Schema.org
        if CHANGED_FILES:
            with open(test_file, WRITE) as f:
                f.write(txt)
        else:
            self.assertEqual(txt, txt_html, 'test_get_hierachy')

    def test_get_one_level(self):
        for test in self.tests:
            test_file = f'{TEST_DIR}one_level_{test}.html'
            txt_html = ''
            if not CHANGED_FILES:
                with open(test_file) as f:
                    txt_html = f.read()

            env = {'REQUEST_METHOD': 'GET', 'CONTENT_LENGTH': '0',
                   'QUERY_STRING': 'TieAction_name_Text=this+name&id=TieAction_agent_Organization&'
                                   'TieAction_additionalType_URL=http%3A%2F%2Fwww.www.www&next_element=Organization'}
            ctx = EZContext(env)
            schema = SchemaClass('TieAction')
            txt = self.select_test(test, schema, ctx)

            # If the output doesn't coincide, there may be another version of Schema.org
            if CHANGED_FILES:
                with open(test_file, WRITE) as f:
                    f.write(txt)
            else:
                self.assertEqual(txt, txt_html, 'test_get_one_level')

    def test_get_two_levels(self):
        for test in self.tests:
            test_file = f'{TEST_DIR}two_level_{test}.html'
            txt_html = ''
            if not CHANGED_FILES:
                with open(test_file) as f:
                    txt_html = f.read()

            env = {'REQUEST_METHOD': 'GET', 'CONTENT_LENGTH': '0',
                   'QUERY_STRING': 'TieAction_name_Text=this+name&'
                                   'id=TieAction_agent_Organization&'
                                   'TieAction_additionalType_URL=http%3A%2F%2Fwww.www.www&next_element=Organization&'
                                   'TieAction_agent_Organization_additionalType_URL=hahaha'}
            ctx = EZContext(env)
            schema = SchemaClass('TieAction')
            txt = self.select_test(test, schema, ctx)

            # If the output doesn't coincide, there may be another version of Schema.org
            if CHANGED_FILES:
                with open(test_file, WRITE) as f:
                    f.write(txt)
            else:
                self.assertEqual(txt, txt_html, 'test_get_two_level')

    def test_get_three_levels(self):
        for test in self.tests:
            test_file = f'{TEST_DIR}three_level_{test}.html'
            txt_html = ''
            if not CHANGED_FILES:
                with open(test_file) as f:
                    txt_html = f.read()

            env = {'REQUEST_METHOD': 'GET', 'CONTENT_LENGTH': '0',
                   'QUERY_STRING': 'TieAction_name_Text=this+name&'
                                   'id=TieAction_agent_Organization&'
                                   'TieAction_additionalType_URL=http%3A%2F%2Fwww.www.www&'
                                   'TieAction_agent_Organization_additionalType_URL=hahaha&'
                                   'TieAction_agent_Organization_address_PostalAddress_additionalType_URL=ad1&'
                                   'TieAction_agent_Organization_address_PostalAddress_addressCountry_Text=adcou&'
                                   'TieAction_agent_Organization_address_PostalAddress_addressLocality_Text=adloc&'
                                   'TieAction_agent_Organization_address_PostalAddress_addressRegion_Text=adreg'}

            ctx = EZContext(env)
            schema = SchemaClass('TieAction')
            txt = self.select_test(test, schema, ctx)

            # If the output doesn't coincide, there may be another version of Schema.org
            if CHANGED_FILES:
                with open(test_file, WRITE) as f:
                    f.write(txt)
            else:
                self.assertEqual(txt, txt_html, 'test_get_three_level')

    def test_get_mo_better_levels(self):
        for test in self.tests:
            test_file = f'{TEST_DIR}mo_better_levels_{test}.html'
            txt_html = ''
            if not CHANGED_FILES:
                with open(test_file) as f:
                    txt_html = f.read()

            env = {'REQUEST_METHOD': 'GET', 'CONTENT_LENGTH': '0',
                   'QUERY_STRING': 'TieAction_name_Text=this+name&'
                                   'id=TieAction_agent_Organization&'
                                   'TieAction_additionalType_URL=http%3A%2F%2Fwww.www.www&'
                                   'TieAction_agent_Organization_additionalType_URL=hahaha&'
                                   'TieAction_agent_Organization_address_PostalAddress_additionalType_URL=ad1&'
                                   'TieAction_agent_Organization_address_PostalAddress_addressCountry_Text=adcou&'
                                   'TieAction_agent_Organization_address_PostalAddress_addressLocality_Text=adloc&'
                                   'TieAction_agent_Organization_address_PostalAddress_addressRegion_Text=adreg&'
                                   'TieAction_image_ImageObject_accessibilityAPI_Text=accessAPI'}

            ctx = EZContext(env)
            schema = SchemaClass('TieAction')
            txt = self.select_test(test, schema, ctx)

            # If the output doesn't coincide, there may be another version of Schema.org
            if CHANGED_FILES:
                with open(test_file, WRITE) as f:
                    f.write(txt)
            else:
                self.assertEqual(txt, txt_html, 'test_get_mo_better_levels')

    def test_get_breadcrumbs(self):
        test_file = f'{TEST_DIR}test_get_breadcrumbs.html'
        txt_html = ''
        if not CHANGED_FILES:
            with open(test_file) as f:
                txt_html = f.read()

        schema = self.hierarchy.get_schema('Dentist')
        txt = self.view._breadcrumbs(schema)

        # If the output doesn't coincide, there may be another version of Schema.org
        if CHANGED_FILES:
            with open(test_file, WRITE) as f:
                f.write(txt)
        else:
            self.assertEqual(txt, txt_html, 'test_get_one_level')

    def select_test(self, test, schema, ctx):
        if 'micro' == test:
            return self.view.generate_microdata(schema, ctx)
        elif 'rdfa' == test:
            return self.view.generate_rdfa(schema, ctx)

        return self.view.generate_json(schema, ctx)


if __name__ == "__main__":
    SCHEMA_VERSION = 12
    # CHANGED_FILES = True
    CHANGED_FILES = False

    from os import chdir

    BASE_DIR = f'{__file__[:__file__.index("tests")]}src/'
    chdir(BASE_DIR)
    # HIERARCHY_FILE = 'Hierarchy.pickle'
    #
    # if not path.exists(HIERARCHY_FILE):
    #     copy(BASE_DIR + HIERARCHY_FILE, '.')

    main()
