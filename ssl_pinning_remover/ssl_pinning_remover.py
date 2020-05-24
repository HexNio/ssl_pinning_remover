import argparse
from bs4 import BeautifulSoup
import os

from .core import core


def unlock_apk(input_path, is_uploadable):
    
    if os.path.exists(input_path):

        #unpackapk
        output_folder = core.unpack_jar(input_path)

        #modify manifest
        core.modify_manifest(output_folder + '/' + core.ANDROIDMANIFEST)
        
        #checkif netsecurity exist and modify it
        core.modify_network_config(output_folder)

        #rebuildapk
        core.rebuild_apk(output_folder)

        #signapk
        core.signing_apk(output_folder)

        #zipalignapk
        core.align_apk(output_folder)

        #uploadapk
        if is_uploadable:
            core.install_apk(output_folder)

        print('[!] Process Terminated')

    else:
        print('[-] input path not found...')



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input',
                        help='Used to specify the .apk path',
                        default='',
                        type=str)
    parser.add_argument('-v', '--verbose',
                        default=False,
                        help='Use it if you want more logs during the process',
                        action='store_true')
    parser.add_argument('-u', '--upload',
                        default=False,
                        help='Use it if you upload the modified apk in your phone',
                        action='store_true')


    args = parser.parse_args()
    if args.input == '':
        parser.error('No action performed, set the --input path at least.')
    if args.verbose:
        core.is_verbose = True

    unlock_apk(args.input, args.upload)


if __name__ == '__main__':
    main()