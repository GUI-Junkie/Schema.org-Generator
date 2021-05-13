#!/usr/bin/python3
from unittest import TestCase, main
# from unittest import skip
from urllib.error import URLError

from model.schema import Hierarchy


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
        func = self._testMethodName
        # print(self.schema.hierarchy)
        try:
            schema_class = self.schema.get_schema('WearAction')

            rs = schema_class.get_parent_class  # Get the parent
            test_list = [['Thing', 'Action', 'ConsumeAction', 'UseAction']]

            self.assertEqual(test_list, rs, f'Value: {func}')
        except URLError as e:
            raise e

    def test_get_schema_class_from_Hierarchy(self):
        func = self._testMethodName
        try:
            schema_class = self.schema.get_schema('Thing')

            self.assertEqual('Thing', schema_class.name, f'Value: {func}')
        except URLError as e:
            raise e

    def test_check_properties(self):
        func = self._testMethodName
        try:
            schema_class = self.schema.get_schema('Thing')

            rs = sorted(schema_class.properties.keys())
            # print(rs)
            self.assertTrue('url' in rs, f'Value: {func}')
        except URLError as e:
            raise e

    def test_get_properties(self):
        func = self._testMethodName
        try:
            schema_class = self.schema.get_schema('Thing')

            rs = sorted(schema_class.properties.keys())

            self.assertEqual('additionalType', rs[0], f'Value: {func}')
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
    from os import chdir

    BASE_DIR = f'{__file__[:__file__.index("tests")]}src/'
    chdir(BASE_DIR)

    main()
