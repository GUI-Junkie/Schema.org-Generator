#!/usr/bin/python3

from unittest import TestCase, main
from model.schema import Hierarchy  # , SchemaClass, PropertyType
from controller import EZContext
from view.schema_view import SchemaView

TEST_DIR = '{0}tests/test_files/'.format(__file__[:__file__.index('tests')])


class TestHierarchy(TestCase):
    changed_files = False
    # changed_files = True

    @classmethod
    def setUpClass(cls):
        cls.hierarchy = Hierarchy()
        cls.view = SchemaView()

    @classmethod
    def tearDownClass(cls):
        cls.view = None
        cls.hierarchy = None

    def test_get_hierachy(self):
        test_file = '{0}hierarchy.html'.format(TEST_DIR)
        with open(test_file) as f:
            txt_html = f.read()

        txt = self.view.get_index(self.hierarchy.hierarchy)
        # If the output doesn't coincide, there may be another version of Schema.org
        if self.changed_files:
            with open(test_file, 'w') as f:
                f.write(txt)
        self.assertEqual(txt, txt_html, 'test_get_hierachy')

    def test_get_one_level(self):
        test_file = '{0}one_level.html'.format(TEST_DIR)
        with open(test_file) as f:
            txt_html = f.read()

        env = {'REQUEST_METHOD': 'GET', 'CONTENT_LENGTH': '0',
               'QUERY_STRING': 'TieAction_name_Text=this+name&id=TieAction_agent_Organization&'
                               'TieAction_additionalType_URL=http%3A%2F%2Fwww.www.www&next_element=Organization'}
        ctx = EZContext(env)
        txt = self.view.generate_schema_output('TieAction', ctx)

        # If the output doesn't coincide, there may be another version of Schema.org
        if self.changed_files:
            with open(test_file, 'w') as f:
                f.write(txt)
        self.assertEqual(txt, txt_html, 'test_get_one_level')

    def test_get_two_levels(self):
        test_file = '{0}two_level.html'.format(TEST_DIR)
        with open(test_file) as f:
            txt_html = f.read()

        env = {'REQUEST_METHOD': 'GET', 'CONTENT_LENGTH': '0',
               'QUERY_STRING': 'TieAction_name_Text=this+name&'
                               'id=TieAction_agent_Organization&'
                               'TieAction_additionalType_URL=http%3A%2F%2Fwww.www.www&next_element=Organization&'
                               'TieAction_agent_Organization_additionalType_URL=hahaha'}
        ctx = EZContext(env)
        txt = self.view.generate_schema_output('TieAction', ctx)

        # If the output doesn't coincide, there may be another version of Schema.org
        if self.changed_files:
            with open(test_file, 'w') as f:
                f.write(txt)
        self.assertEqual(txt, txt_html, 'test_get_two_level')

    def test_get_three_levels(self):
        test_file = '{0}three_level.html'.format(TEST_DIR)
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
        txt = self.view.generate_schema_output('TieAction', ctx)

        # If the output doesn't coincide, there may be another version of Schema.org
        if self.changed_files:
            with open(test_file, 'w') as f:
                f.write(txt)
        self.assertEqual(txt, txt_html, 'test_get_three_level')

    def test_get_mo_better_levels(self):
        test_file = '{0}mo_better_levels.html'.format(TEST_DIR)
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
        txt = self.view.generate_schema_output('TieAction', ctx)

        # If the output doesn't coincide, there may be another version of Schema.org
        if self.changed_files:
            with open(test_file, 'w') as f:
                f.write(txt)
        self.assertEqual(txt, txt_html, 'test_get_mo_better_levels')


if __name__ == "__main__":
    from datetime import datetime
    from os import chdir

    BASE_DIR = '{0}src/'.format(__file__[:__file__.index('tests')])
    chdir(BASE_DIR)
    # HIERARCHY_FILE = 'Hierarchy.pickle'
    #
    # if not path.exists(HIERARCHY_FILE):
    #     copy(BASE_DIR + HIERARCHY_FILE, '.')

    tStart = datetime.now()

    main()

    tFin = datetime.now()
    tDiff = tFin - tStart
    print("\nDuration:", ''.join([str(tDiff.seconds), ":", str(tDiff.microseconds)]))
