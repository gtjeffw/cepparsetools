import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cepparsetools',
    version='0.0.2',
    author='Jeff Wilson',
    author_email='jeff@imtc.gatech.edu',
    description='CEP Data Parsing Tools',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/gtjeffw/cepparsetools',
    project_urls={
        "Bug Tracker": "https://github.com/gtjeffw/cepparsetools/issues"
    },
    license='MIT',
    packages=['cepparsetools'],
    install_requires=['lark'],
)