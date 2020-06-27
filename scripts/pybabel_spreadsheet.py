import argparse
import sys
import logging

from pybabel_utils.spreadsheets import PoFilesToSpreadsheet


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def parse_args():
    descr = 'This script converts translations from .po to .xlsx and vice versa'
    arg_parser = argparse.ArgumentParser(description=descr)
    subparsers = arg_parser.add_subparsers(dest='subcommand')

    parser_to_xlsx = subparsers.add_parser('to_xlsx')
    parser_to_xlsx.add_argument('-i', '--input_folder', type=str, help='Name of folder with po files')
    parser_to_xlsx.add_argument('-o', '--output_file', nargs='?', const=1, default='po_as_table.xlsx',
                                help='Name of the output file with format included')

    if len(sys.argv[1:]) == 0:
        arg_parser.print_help()
        arg_parser.exit()
    return arg_parser, arg_parser.parse_args()


if __name__ == '__main__':
    parser, run_args = parse_args()
    if run_args.subcommand == 'to_xlsx':
        PoFilesToSpreadsheet.run(run_args.input_folder, run_args.output_file)
    else:
        parser.print_help()
        parser.exit()
