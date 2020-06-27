import os
import unittest

from pybabel_utils.spreadsheets import PoFilesToSpreadsheet
from tests import TEST_DATA_PATH


class TestPoFilesToSpreadsheet(unittest.TestCase):

    def setUp(self):
        super(TestPoFilesToSpreadsheet, self).setUp()
        self.test_out_file_name = 'wb.xlsx'
        self.test_out_file_path = os.path.join(TEST_DATA_PATH, self.test_out_file_name)

    def tearDown(self):
        super(TestPoFilesToSpreadsheet, self).tearDown()
        try:
            os.remove(self.test_out_file_path)
        except:
            pass

    def test_run(self):
        wb = PoFilesToSpreadsheet.run(TEST_DATA_PATH, self.test_out_file_name)

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


if __name__ == '__main__':
    unittest.main()
