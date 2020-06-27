import os
import unittest

from pybabel_utils.spreadsheets import PoFilesToSpreadsheet, PoFilesFromSpreadsheet
from tests import TEST_DATA_PATH


class TestPoFilesToSpreadsheet(unittest.TestCase):

    def setUp(self):
        super(TestPoFilesToSpreadsheet, self).setUp()
        self.test_out_file_name = 'wb.xlsx'
        self.test_locales_dir_path = os.path.join(TEST_DATA_PATH, 'locales')
        self.test_out_file_path = os.path.join(TEST_DATA_PATH, 'locales', self.test_out_file_name)

    def tearDown(self):
        super(TestPoFilesToSpreadsheet, self).tearDown()
        try:
            os.remove(self.test_out_file_path)
        except:
            pass

    def test_run(self):
        wb = PoFilesToSpreadsheet.run(self.test_locales_dir_path, self.test_out_file_name)

        rows = list(wb.active.rows)
        self.assertEqual(6, len(rows))

        self.assertEqual('msgid', rows[0][0].value)
        self.assertEqual('en.po', rows[0][1].value)
        self.assertEqual('es.po', rows[0][2].value)
        self.assertEqual('de.po', rows[0][3].value)

        for r in rows[1:]:
            self.assertTrue(r[0].value.startswith('prj'))
            self.assertTrue(r[1].value.startswith('en:'))
            self.assertTrue(r[2].value.startswith('es:'))
            self.assertTrue(r[3].value.startswith('de:'))


class TestPoFilesFromSpreadsheet(unittest.TestCase):

    def setUp(self):
        super(TestPoFilesFromSpreadsheet, self).setUp()
        self.test_locales_dir_path = os.path.join(TEST_DATA_PATH, 'locales')
        self.test_input_spreadsheet_path = os.path.join(TEST_DATA_PATH, 'test_input_spreadsheet.xlsx')

    def test_run(self):
        catalogs = PoFilesFromSpreadsheet.run(self.test_input_spreadsheet_path, self.test_locales_dir_path, save=False)
        self.assertIsInstance(catalogs, list)
        self.assertEqual(3, len(catalogs))

        en_catalog = catalogs[0]
        self.assertEqual(6, len(en_catalog))

        es_catalog = catalogs[1]
        self.assertEqual(6, len(es_catalog))

        de_catalog = catalogs[2]
        self.assertEqual(6, len(de_catalog))


if __name__ == '__main__':
    unittest.main()
