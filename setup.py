import os

from setuptools import setup

PACKAGE_VERSION = '0.1'


def version():
    def version_file(mode='r'):
        return open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'version.txt'), mode)

    if os.getenv('TRAVIS'):
        with version_file('w') as verfile:
            verfile.write('{0}.{1}'.format(PACKAGE_VERSION, os.getenv('TRAVIS_BUILD_NUMBER')))
    with version_file() as verfile:
        data = verfile.readlines()
        return data[0].strip()

setup(
    name='fallball',
    version=version(),
    author='romanovskyj',
    author_email='eromanovskyj@odin.com',
    packages=['fallball'],
    test_suite="fallball.runtests",
    url='http://fallball.io',
    license='Apache License',
    description='Dummy file sharing service available by REST api.',
    long_description=open('README.md').read(),
)
