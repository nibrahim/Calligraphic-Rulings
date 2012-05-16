from setuptools import setup

setup(
    name="calligraphic-rulings",
    version="0.2alpha",
    description='Script to generate ruling pages for western calligraphy',
    long_description=open('README.txt').read(),
    license='GPL',
    author='Noufal Ibrahim',
    author_email='noufal@nibrahim.net.in' ,
    url='https://github.com/nibrahim/Calligraphic-Rulings',
    platforms=['linux', 'osx', 'win32'],
    py_modules=['calligraphic_rulings'],
    install_requires = ['reportlab'],
    classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS :: MacOS X',
    'Topic :: Utilities',
    'Programming Language :: Python',
    ],
)
