#!/usr/bin/python3
from unittest import TestCase, main
# from unittest import skip
from urllib.error import URLError
from model.schema import Hierarchy, SchemaClass


# @skip("Skip TestHierarchy")
class TestHierarchy(TestCase):
    schema = None

    @classmethod
    def setUpClass(cls):
        cls.schema = Hierarchy()

    @classmethod
    def tearDownClass(cls):
        del cls.schema

    def test_get_parent_class_WearAction_from_Hierarchy(self):
        # print(self.schema.hierarchy)
        try:
            schema_class = self.schema.get_schema('WearAction')

            rs = schema_class.get_parent_class  # Get the parent
            test_list = [['Thing', 'Action', 'ConsumeAction', 'UseAction']]

            self.assertEqual(test_list, rs, 'Value: {0}'.format('test_get_parent_class_WearAction_from_Hierarchy'))
        except URLError as e:
            raise e

    def test_get_schema_class_from_Hierarchy(self):
        try:
            schema_class = self.schema.get_schema('Thing')

            self.assertEqual('Thing', schema_class.name, 'Value: {0}'.format('test_get_schema_class_from_Hierarchy'))
        except URLError as e:
            raise e

    def test_check_properties(self):
        try:
            schema_class = self.schema.get_schema('Thing')

            rs = sorted(schema_class.properties.keys())
            # print(rs)
            self.assertTrue('url' in rs, 'Value: {0}'.format('test_check_properties'))
        except URLError as e:
            raise e

    def test_get_properties(self):
        try:
            schema_class = self.schema.get_schema('Thing')

            rs = sorted(schema_class.properties.keys())

            self.assertEqual('additionalType', rs[0], 'Value: {0}'.format('test_get_properties'))
        except URLError as e:
            raise e


# @skip("Skip TestSchemaClass")
class TestSchemaClass(TestCase):
    def test_get_parent_class(self):
        try:
            schema_class = SchemaClass('Thing')
            schema_class.start(True)

            rs = schema_class.get_parent_class  # Get the parent

            self.assertEqual([], rs, 'Value: {0}'.format('test_get_parent_class'))
        except URLError as e:
            raise e

    def test_schema_properties_from_url(self):
        try:
            schema_class = SchemaClass('Thing')
            schema_class.start(True)

            rs = schema_class.properties.keys()

            self.assertTrue('url' in rs, 'Value: {0}'.format('test_schema_properties_from_url'))
        except URLError as e:
            raise e

    def test_get_parent_class_WearAction(self):
        try:
            schema_class = SchemaClass('WearAction')
            schema_class.start(True)

            rs = schema_class.get_parent_class  # Get the parent
            test_list = [['Thing', 'Action', 'ConsumeAction', 'UseAction']]

            self.assertEqual(test_list, rs, 'Value: {0}'.format('test_get_parent_class_WearAction'))
        except URLError as e:
            raise e

    def test_get_multiple_parent_class_VideoGame(self):
        try:
            schema_class = SchemaClass('VideoGame')
            schema_class.start(True)

            rs = sorted(schema_class.get_parent_class)  # Get the parent
            # print(s)
            test_list = [['Thing', 'CreativeWork', 'Game'], ['Thing', 'CreativeWork', 'SoftwareApplication']]
            self.assertEqual(rs, test_list, 'Value: {0}'.format('test_get_multiple_parent_class_VideoGame'))
        except URLError as e:
            raise e

    def test_get_schema_class(self):
        try:
            schema_class = SchemaClass('Thing')
            schema_class.start(True)

            self.assertEqual('Thing', schema_class.name, 'Value: {0}'.format('test_get_schema_class'))
        except URLError as e:
            raise e


# @skip("Skip TestPropertyTypes")
class TestPropertyTypes(TestCase):
    def testAddProperties(self):
        p = set()
        p.add('URL')
        p.add('Text')
        p.add('URL')
        p.add('Text')
        p.add('URL')
        p.add('Text')
        p.add('URL')
        p.add('Text')

        # print(p)
        self.assertEqual(p, {'Text', 'URL'}, 'testAddProperties')


if __name__ == "__main__":
    from datetime import datetime
    from os import chdir

    BASE_DIR = '{0}src/'.format(__file__[:__file__.index('tests')])
    chdir(BASE_DIR)

    tStart = datetime.now()

    main()

    tFin = datetime.now()
    tDiff = tFin - tStart
    print("\nDuration:", ''.join([str(tDiff.seconds), ":", str(tDiff.microseconds)]))
