from setuptools import setup, find_packages

VERSION = '1.2.0' 
DESCRIPTION = 'Tools for collecting behavioural measures of iconicity'


# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="icotools", 
        version=VERSION,
        author="Bonnie McLean",
        author_email="<59.b.mclean@gmail.com>",
        description=DESCRIPTION,
        long_description=open('pypiREADME.txt').read(),
        packages=find_packages(),
        url='https://pypi.org/project/icotools/',
        license="LICENSE",
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'iconicity'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
        include_package_data=True,
        package_data={'':['templates/*.html','templates/*.php','features/*.tsv']},
)

