from distutils.core import setup, Extension

module = Extension('APNGLib',

					libraries = ['stdc++', 'm', 'png', 'z'],
                    sources = ['APNGLib/APNGLib.cpp'])

setup (name = 'APNGLib',
	   packages = ['APNGLib'],
       version = '1.0',
       description = 'APNGLib a few tools for working with APNG files',
	   author = 'Tim Collins',
	   author_email = 'tscollins321@aim.com',
	   url = 'https://github.com/slicer4ever/APNGLib',
	   download_url = 'https://github.com/slicer4ever/APNGLib/archive/1.0.tar.gz',
	   keywords = ['APNG'],
	   classifiers = [],
       ext_modules = [module])
