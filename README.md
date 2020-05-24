<p align="center">
  <img width="600" height="220" src="https://github.com/HexNio/ssl_pinning_remover/blob/master/imgs/SSL_pinning_remover_logo.png?raw=true">
</p>

[![PyPI version shields.io](https://img.shields.io/pypi/v/ssl-pinning-remover.svg)](https://pypi.org/project/ssl-pinning-remover/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


## Brief history
All it started with two simple questions:

**How we can sniff ssl traffic in order to understand which services are invoked?**

and

**Is there a method to automate all the process from decompile a .apk to upload on your device?**

For the first questions i found a lot of guides that explain the procedure of modify the *AndroidManifest.xml* and the *network_security_config.xml* but there is not a single formula, there are different factors to understand in order to do it correctly.

For the second question is: Yes... but.

i found different types of project the on Github but they aren't completely automated in all those phases so here we are.

I read a lot of guides most of those requires to have a rooted device so i tried to create something to sniff the encrypted traffic unrooted devices in order to help all security researchers, this software is **UNSTABLE** for now a lot of "unlocked" apps will not work with this mod.

## How it works?
ssl_pinning_remover has all the following phases:
1. Unpack the .apk app with apktool
2. Check if the *AndroidManifest.xml* has the correct attributes and if *network_security_config.xml* exists with the correct tags
3. Repack the modified files in a new apk packet
4. Sign the new apk with a self signed certificate
5. Align the certified apk
6. it upload the new jar in the connected android device (Optional)

## Prerequisites
To use this script you need to install all those softwares in your environment:
* [Java JDK 8 or above](https://www.oracle.com/it/java/technologies/javase-downloads.html)
* [apktool](https://ibotpeaches.github.io/Apktool/)
* [Android Debug Bridge (adb)](https://developer.android.com/studio/releases/platform-tools)

On your device:
* [Enable USB Debugging](https://www.phonearena.com/news/How-to-enable-USB-debugging-on-Android_id53909)

## How to install

```
$ pip install -r requirements.txt
$ pip install ssl-pinning-remover
```

## How to use 
| Parameter  | Description | Mandatory |
| ------------- | ------------- |------------- |
| `-i --input`  | Used to specify the input .apk path | Yes |
| `-v --verbose`  | Used to increase the stdout verbosity  | No |
| `-u --upload`  | Used to specify if you want upload the "unlocked" apk in the connected device or not  | No |

### Example

Elaborate without uploading .apk:

`ssl_pinning_remover -i test.apk -v`

Elaborate and upload .apk:

`ssl_pinning_remover -i test.apk -v -u`

The output path is the path where you launch the script.
The modified apk will have the same name of the original apk but before the extension will be added ".unlocked.apk"

## ToDo List

- [ ] Continue implementing studying difference configuration cases

- [ ] Make the software working for most of the applications in the play store

- [ ] Add more options

- [ ] Code review


## Disclaimer

This project is for educational and research purposes only. Any actions and/or activities related to the material contained on this GitHub Repository is solely your responsibility. The misuse of the information in this GitHub Repository can result in criminal charges brought against the persons in question. The author will not be held responsible in the event any criminal charges be brought against any individuals misusing the information in this GitHub Repository to break the law.
