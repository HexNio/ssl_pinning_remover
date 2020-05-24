import sys
import os
import subprocess
import magic
import shutil
from bs4 import BeautifulSoup

ANDROIDMANIFEST = 'AndroidManifest.xml'
NETWORK_SECURITY_CONFIG_PATH = '/res/xml/'
NEW_APK_PATH = '/dist/'
NETWORK_SECURITY_CONFIG = 'network_security_config.xml'

DEFAULT_NETWORK_CONFIG_CONTENT = '''<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config>
        <trust-anchors>
            <certificates src="system" />
            <certificates src="user" />
        </trust-anchors>
    </base-config>
</network-security-config>'''

PARENT_PATH = os.sep.join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-1])

TOOLS_PATH = PARENT_PATH + '/tools/'
FILES_PATH = PARENT_PATH + '/files/'
TEMP_PATH = PARENT_PATH + '/temp/'

is_verbose = False


def unpack_jar(input_path):

    if is_verbose:
            print('[+] Cleaning...')
    
    output_dir = input_path.rsplit('/',1)[1].rsplit('.', 1)[0]

    shutil.rmtree(TEMP_PATH, ignore_errors=True)

    if os.path.exists(input_path):
        if is_verbose:
            print('[+] Going to decode the APK...')

        try:
            subprocess.run(['apktool',
                            '-o', TEMP_PATH + output_dir, 
                            'd', '-f', input_path],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL).check_returncode()
            
        except subprocess.CalledProcessError:
            print('[-] Unable to decode this APK')


        if is_verbose:
            print('[+] Succesfully decompiled APK')
    else:
        print("[-] Invalid path")

    return TEMP_PATH + output_dir


def check_file_type(filename):
    return magic.from_file(filename)


def modify_manifest(output_folder):

    if is_verbose:
        print('[+] Modify AndroidManifest.xml...')

    fd = open(output_folder, 'r')
    xml_file = fd.read()
    fd.close()
    soup = BeautifulSoup(xml_file, 'xml')
    soup.prettify()

    if soup.select_one("application").get('android:networkSecurityConfig') == None:
        soup.find('application')['android:networkSecurityConfig'] = '@xml/network_security_config'
    else:
        soup.find('application')['android:networkSecurityConfig'] = '@xml/network_security_config'

    if soup.select_one("application").get('android:usesCleartextTraffic') == None:
        soup.find('application')['android:usesCleartextTraffic'] = 'true'
    else:
        soup.find('application')['android:usesCleartextTraffic'] = 'true'

    if soup.select_one("application").get('android:debuggable') == None:
        soup.find('application')['android:debuggable'] = 'true'
    else:
        soup.find('application')['android:debuggable'] = 'true'

    fd = open(output_folder, 'w')
    fd.write(str(soup))
    fd.close()

def modify_network_config(output_path):

    output_folder = output_path + NETWORK_SECURITY_CONFIG_PATH + NETWORK_SECURITY_CONFIG

    if is_verbose:
        print('[+] Looking for network_security_config.xml...')

    if os.path.isfile(output_folder):

        if is_verbose:
            print('[+] Found network_security_config.xml...')

        fd = open(output_folder, 'r')
        xml_file = fd.read()
        fd.close()
        soup = BeautifulSoup(xml_file, 'xml')
        soup.prettify()

        if is_verbose:
            print('[+] Modify network_security_config.xml...')

        if not soup.find("network-security-config").isSelfClosing:

            for domains in soup.findAll("domain-config"):
                domains['cleartextTrafficPermitted'] = 'true'

                if domains.select_one("domain") is not None:

                    for domain in domains.findAll("domain"):
                        
                        if domain['includeSubdomains'] == 'false' or domain['includeSubdomains'] is None:
                            domain['includeSubdomains'] = 'true'

                if soup.select_one("trustkit-config") is not None:

                    if soup.select_one("trustkit-config").get('enforcePinning') == None:
                        
                        domains.find('trustkit-config')['enforcePinning'] = 'false'
                    else:
                        domains.find('trustkit-config')['enforcePinning'] = 'false'

                    fd = open(output_folder, 'w')
                    fd.write(str(soup))
                    fd.close()

        else:
            if is_verbose:
                print('[+] network_security_config.xml found but it\'s has only a self closing tab...')

            fd = open(output_folder, 'w')
            fd.write(DEFAULT_NETWORK_CONFIG_CONTENT)
            fd.close()


    else:
        if is_verbose:
            print('[-] network_security_config.xml not found creating a new one...')

        if os.path.exists(output_path + NETWORK_SECURITY_CONFIG_PATH):

            fd = open(output_folder, 'w')
            fd.write(DEFAULT_NETWORK_CONFIG_CONTENT)
            fd.close()
        else:
            os.makedirs(output_path + NETWORK_SECURITY_CONFIG_PATH)
            open(NETWORK_SECURITY_CONFIG, 'a').close()
            fd = open(output_folder, 'w+')
            fd.write(DEFAULT_NETWORK_CONFIG_CONTENT)
            fd.close()

def rebuild_apk(output_folder):

    apk_name = output_folder.split("/")[-1] + '.new.apk'

    if is_verbose:
        print('[+] Starting rebuilding the APK...')

    try:
        subprocess.run(['apktool', 'b', output_folder, '-o', TEMP_PATH + apk_name],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL).check_returncode()
    except subprocess.CalledProcessError:
        print('[-] Unable to rebuild the APK')


def signing_apk(output_folder):

    apk_name = output_folder.split("/")[-1] + '.new.apk'
    
    if os.path.isfile(TEMP_PATH + apk_name):
        if is_verbose:
            print('[+] Signing the APK...')

        try:
            with subprocess.Popen(['jarsigner', '-sigalg', 'SHA1withRSA', 
                            '-digestalg', 'SHA1', '-keystore', TOOLS_PATH + 'new-release-key.keystore',
                            TEMP_PATH + apk_name, 'new_name'],
                            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) as p:
                p.stdin.write(bytes("123456789"+'\r\n','utf-8'))
                p.stdin.close()

        except subprocess.CalledProcessError:
            print('[-] Unable to sign the APK')
    else:
       print('[-] No APK to sign') 


def align_apk(output_folder):

    apk_name = output_folder.split("/")[-1] + '.new.apk'

    if os.path.isfile(TEMP_PATH + apk_name):
        if is_verbose:
            print('[+] Aligning the APK...')

        try:
            subprocess.run([TOOLS_PATH + 'zipalign', '-v', '4', 
                            TEMP_PATH + apk_name, output_folder.split("/")[-1] + '.unlocked.apk'],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL).check_returncode()
        except subprocess.CalledProcessError:
            print('[-] Unable to align the APK')
    else:
        print('[-] No APK to align')

def install_apk(output_folder):

    apk_name = (output_folder.split("/")[-1] + '.unlocked.apk').encode('utf-8')

    if os.path.isfile(apk_name):
        if is_verbose:
                print('[+] Upload and install the APK...')

        try:
            subprocess.run(['adb', 'install', apk_name],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL).check_returncode()
        except subprocess.CalledProcessError:
            print('[-] Unable to upload and install the APK')
