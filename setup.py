from distutils.core import setup
import sys, os

try:
	import py2exe
except ImportError as e:
	print('IMPORT ERROR: please, install py2exe.\npip install py2exe\n')
	sys.exit(1)
	
sys.argv.append('py2exe')

setup(
	windows=['app.py'],
	name='Restaurant manager',
	options = {         
	'py2exe' : {
        'dist_dir': 'bin',
        'skip_archive': True,
        }
    }
)
