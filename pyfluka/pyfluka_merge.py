import sys
import argparse
import fnmatch
import os
import re
import shutil
import glob
import logging
import multiprocessing
from copy_reg import pickle
from types import MethodType

_logger = logging.getLogger('default')
_logger.addHandler(logging.StreamHandler())
_logger.setLevel(logging.CRITICAL)


def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)


def _unpickle_method(func_name, obj, cls):
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)


class InputParser:
    def __init__(self, path):
        self.path = path
        self.parsedInfo = {'resnuc': [], 'usrbin': []}

    def _get_bins(self):
        r = re.compile("([0-9]{2})$")
        self.bins = set([int(re.search(r, fN).group(1)) for fN in glob.glob(self.path + '/*fort*')])

    def _drop_bin(self, bin):
        try:
            self.bins.remove(bin)
            return True
        except:
            return False

    def __parse_scoring_cards(self):
        re_resnuc = re.compile("^RESNUC")
        re_usrbin = re.compile("^(USRBIN)\s+\d+.?\d?\s+\w+.*")
        try:
            input_file = glob.glob(self.path + '/*.inp')[0]
        except IndexError:
            _logger.critical("Unable to locate .inp file required for parsing scoring card information. Either provide "
                             "it in the input directory or specify card and bins explicitly.")
            sys.exit(1)
        for line in open(input_file).readlines():
            if len(self.bins) == 0:
                return
            if re.match(re_resnuc, line):
                index = abs(int(line.split()[2].rstrip('.')))
                add_bin = self._drop_bin(index)
                if add_bin:
                    self.parsedInfo['resnuc'].append(index)

            elif re.match(re_usrbin, line):
                index = abs(int(line.split()[3].rstrip('.')))
                add_bin = self._drop_bin(index)
                if add_bin:
                    self.parsedInfo['usrbin'].append(index)

    def parse(self):
        self._get_bins()
        self.__parse_scoring_cards()
        return self.parsedInfo


class Merger(object):
    def __init__(self, path, out_path):
        self.curdir = os.getcwd()
        self.path = path
        self.bins = []
        self.filelist = []
        self.cycle = []
        self.parse_dir()
        self.mergingCodeLookup = {'resnuc': 'usrsuw',
                                  'usrbin': 'usbsuw'}
        self.out_path = out_path
        self.__class__.check_fluka_loaded()
        self.check_out_path()

    @staticmethod
    def check_fluka_loaded():
        try:
            os.environ['FLUPRO']
        except KeyError:
            _logger.critical('FLUPRO environment not setup. Please export FLUPRO pointing to your FLUKA \
                             installation directory.')
            sys.exit(1)

    def check_out_path(self):
        if self.out_path is not None:
            self.out_path = os.path.abspath(self.out_path)
        if not os.path.exists(self.out_path):
            os.makedirs(self.out_path)
            
    def parse_dir(self):
        for file_name in os.listdir(self.path):
            if fnmatch.fnmatch(file_name, '*???_fort.??*'):
                self.geom = file_name[:-11]
                c = int(file_name[-11:-8])
                b = int(file_name[-2:])
                self.filelist.append(file_name)
                if b not in self.bins:
                    self.bins.append(b)
                    if c not in self.cycle:
                        self.cycle.append(c)

    def merge(self, cards):
        pickle(MethodType, _pickle_method, _unpickle_method)
        jobs = [(k,v) for k, values in cards.items() for v in values]
        pool = multiprocessing.Pool(processes=min(len(jobs), multiprocessing.cpu_count()))
        pool.map(self._merge_impl, jobs)

    def _merge_impl(self, *args):
        card = args[0][0]
        b = args[0][1]
        _logger.debug("Merge " + card + " for bin " + str(b))
        os.chdir(self.path)
        list_name = 'list_' + str(b) + '_' + card
        os.system('ls -1 *_fort.'+str(b)+'* > ' + list_name)
        os.system('echo "" >> ' + list_name)
        os.system('echo "' + self.geom + '_' + card + '_'+str(b)+'" >> ' + list_name)
        os.system('%s/flutil/%s < %s ' % (os.environ['FLUPRO'], self.mergingCodeLookup[card], list_name))
        if self.out_path is not None:
            self.move(card, b)
        if card == 'usrbin':
            self.convert_to_ascii(card, b)

    def move(self, card, index):
        for fName in glob.glob(r'%s/%s_%s_%s*' % (self.path,
                                                  self.geom,
                                                  card,
                                                  index)):
            shutil.move(fName, os.path.join(self.out_path, fName.split('/')[-1]))

    def convert_to_ascii(self, card, bin):
        os.chdir(self.out_path)
        tmp_file_name = 'asciiconversion_%s_%i.txt' % (card, bin)
        for file_name in glob.glob(r'%s/%s_%s_%s*' % (self.out_path,
                                                  self.geom,
                                                  card,
                                                  bin)):
            if file_name.endswith('.ascii'):
                continue
            file_name = os.path.split(file_name)[1]
            tmp_file = open(os.path.join(self.curdir, tmp_file_name), 'w+')
            print >> tmp_file, file_name
            print >> tmp_file, file_name + '.ascii'
            tmp_file.close()
            os.system('%s/flutil/usbrea < %s > /dev/null' % (os.environ['FLUPRO'], os.path.join(self.curdir, tmp_file_name)))
            os.remove(os.path.join(self.curdir, tmp_file_name))
        os.chdir(self.curdir)


def main(argv):
    parser = argparse.ArgumentParser(description='Script for merging fluka bin data')
    parser.add_argument('path', help='input path')
    parser.add_argument('--card', '-c', required=False, default=None, help='card')
    parser.add_argument('--bins', '-b', required=False, default=None, type=int, nargs='+', help='bins')
    parser.add_argument('--output', '-o', default=None, help='output directory')
    parser.add_argument('--debug', '-d', action='store_true', default=False, help='Switch on debug messages')
    args = parser.parse_args()
    if args.debug:
        _logger.setLevel(logging.DEBUG)
    path = os.path.abspath(args.path)
    if not args.card and not args.bins:
        parser = InputParser(path)
        scoring_cards = parser.parse()
    else:
        scoring_cards = {args.card : args.bins}
    merger = Merger(path, args.output)
    merger.merge(scoring_cards)


if __name__ == '__main__':
    main(sys.argv[1:])
