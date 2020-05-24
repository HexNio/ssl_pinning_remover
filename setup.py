import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssl-pinning-remover",
    version="1.0.0",
    author="HexNio",
    author_email="",
    description="An SSL Pinning Remover for Android Apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HexNio/ssl_pinning_remover",
    include_package_data=True,
    packages=setuptools.find_packages(),
    keywords=[
        "Android",
        "beautifulsoup4",
        "Bug Bounty",
        "SSL Pinning",
        "automation"
    ],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS :: MacOS X",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Education",
        "Operating System :: Android",
        "Topic :: Internet"
    ],
    install_requires=[
        'lxml',
        'python-magic',
        'beautifulsoup4'
    ],
    entry_points='''
        [console_scripts]
        ssl_pinning_remover=ssl_pinning_remover.ssl_pinning_remover:main
    ''',
    python_requires='>=3.6'
)