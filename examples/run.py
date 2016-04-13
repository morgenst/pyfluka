import argparse
import sys

from pyfluka.base.AnalysisBase import AnalysisBase


# noinspection PyUnusedLocal
def main(argv):
    parser = argparse.ArgumentParser(description='Example analysis')
    parser.add_argument('--input', '-i', type=str, required=True, help='input file')
    parser.add_argument('--output_dir', '-o', type=str, help='ouput directory')
    parser.add_argument('--config', '-c', type=str, required=True, help='configuration file')

    args = parser.parse_args()
    analysis = AnalysisBase(args.input, args.config)
    analysis.run()
    
if __name__ == '__main__':
    main(sys.argv[1:])
