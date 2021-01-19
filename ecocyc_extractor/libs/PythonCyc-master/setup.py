# Copyright (c) 2014, SRI International
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ----------------------------------------------------------------------

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path, walk

def main():
	# additional files
	data_files = []
	for dirpath, dirnames, filenames in walk('examples'):
		tmp = []
		for filename in filenames:
			tmp.append(path.join(dirpath, filename))
		data_files.append((dirpath, tmp))
	#print(data_files)

	# Get the long description from the README file
	here = path.abspath(path.dirname(__file__))
	with open(path.join(here, 'README.md'), encoding='utf-8') as f:
		long_description = f.read()

	setup(
		name='PythonCyc',
		license='SRI International',
		version='2.0.2',
		description='A Python interface to Pathway Tools, 2019 update',
		long_description=long_description,
		#long_description_content_type='text/markdown',
		url='https://github.com/networkbiolab/PythonCyc',
		author='Rodrigo Santibáñez',
		author_email='glucksfall@users.noreply.github.com',

		python_requires='~=3.0',
		keywords=[],
		install_requires=[],

		# include files
		# MANIFEST.in, sdist
		include_package_data=True,
		# bdist_wheel (only for non-python files inside of the package)
		packages=find_packages(exclude=['contrib', 'docs', 'tests']),
		#package_data = {
			#'PythonCyc' : ['test/*.txt']
			#},
		data_files=data_files,

		project_urls={
			'Manual': 'https://pythoncyc-v20.readthedocs.io',
			'Bug Reports': 'https://github.com/networkbiolab/PythonCyc/issues',
			'Source': 'https://github.com/networkbiolab/PythonCyc',
		},
	)

if __name__ == '__main__':
    main()
