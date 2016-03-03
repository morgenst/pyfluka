import argparse
import sys
import base.AnalysisBase

def main(argv):
    parser = argparse.ArgumentParser(description="Entry point to flair++ analysis")
    parser.add_argument('--input_files', '-if', required = True, nargs = '+', type=str, help="list of input files")
    parser.add_argument('--weights', '-w', nargs = '+', default=1., required = False, type=float, help = 'file weights; single value applied to all files or list of weights corresponding to input files')
    parser.add_argument('--config', '-c', required = True, type= str, help = 'config file specifing analysis')

    args = parser.parse_args()

    analysis = BaseC
if __name__ == '__main__':
    main(sys.args[1:])