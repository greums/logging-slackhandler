import codecs
import io
import re
from os.path import abspath, dirname, join

from setuptools import find_packages, setup

MODULE_NAME = 'SlackLogger'
CWD = abspath(dirname(__file__))


def read(*names, **kwargs):
    with io.open(join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^VERSION = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


VERSION = find_version(join(CWD, MODULE_NAME), "version.py")

with codecs.open(join(CWD, 'README.rst'), encoding='utf-8') as reader:
    LONG_DESCRIPTION = reader.read()


setup(
    name='logging-slackhandler',
    version=VERSION,
    description='A logging handler for Slack',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/Greums/logging-slackhandler',
    download_url='https://github.com/Greums/logging-slackhandler/tarball/%s' % VERSION,
    author='Damien Le Bourdonnec',
    author_email='greumsworkshop@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='logging slack',
    platforms='any',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[],
    include_package_data=True,
    zip_safe=False
)
