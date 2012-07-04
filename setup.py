#!/usr/bin/env python3

from distutils.core import setup

from zounds import __version__


setup(name = 'IPA Zounds',
      version = __version__,
      description = 'IPA Zounds sound change applier',
      long_description = '''The IPA Zounds application models language sound change by applying a given set of sound change rules to a given lexicon. It has a built-in model of the IPA, allowing users to write input words in IPA characters, and rules using those characters and/or the distinctive features of the model.''',
      author = 'Jamie Norrish',
      author_email = 'jamie@artefact.org.nz',
      url = 'http://zounds.artefact.org.nz/',
      classifiers = [
        'Environment :: Console',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Linguistic'],
      packages = ['zounds'],
      scripts = ['scripts/zounds'],
      )
