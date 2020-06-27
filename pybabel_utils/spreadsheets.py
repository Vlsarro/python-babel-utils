# -*- coding: utf-8 -*-

import os
import openpyxl

from babel.messages.pofile import read_po

from pybabel_utils import logger


def get_po_filenames(dir_path):
    filenames = []
    for f in os.listdir(dir_path):
        if f.endswith('.po'):
            filenames.append(os.path.join(dir_path, f))
    return filenames


class PoFilesToSpreadsheet(object):

    @classmethod
    def _init_po_workbook(cls, po_filenames):
        """Create workbook and fill header row"""
        workbook = openpyxl.Workbook()
        worksheet = workbook.active

        col = 1
        row = 1
        worksheet.cell(row, col, 'msgid')

        col += 1
        for name in po_filenames:
            worksheet.cell(row, col, name.split(os.sep)[-1])
            col += 1

        return workbook, worksheet

    @classmethod
    def _fill_po_worksheet(cls, po_filenames, worksheet, include_obsolete):
        col = 1
        row = 2

        for filename in po_filenames:
            with open(filename) as f:
                cat = read_po(f, ignore_obsolete=not include_obsolete)
                for msg in cat:
                    if msg.id != '':  # ignore header
                        if col == 1:
                            worksheet.cell(row, col, msg.id)
                            worksheet.cell(row, col + 1, msg.string)
                        else:
                            worksheet.cell(row, col + 1, msg.string)
                        row += 1
            col += 1
            row = 2

    @classmethod
    def run(cls, input_folder_name, output_filename, include_commented_messages=False):
        po_filenames = get_po_filenames(input_folder_name)
        if not po_filenames:
            raise ValueError('No files were added. Please, try again.')

        wb, ws = cls._init_po_workbook(po_filenames)
        try:
            cls._fill_po_worksheet(po_filenames, ws, include_commented_messages)
            wb.save(filename=output_filename)
        except Exception as e:
            logger.debug('Exception occurred while worksheet processing > {!r}'.format(e))

        return wb


class PoFilesFromSpreadsheet(object):
    pass
