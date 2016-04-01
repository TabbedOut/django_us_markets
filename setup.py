from setuptools import setup, find_packages


namespace = {}
exec(open('version.py').read(), namespace)


setup(
    name='django-us-markets',
    version=namespace['__version__'],
    description='Geographic data for US markets and postal codes.',
    long_description=open('README.md').read(),
    author='TabbedOut',
    author_email='dev@tabbedout.com',
    url='https://github.com/TabbedOut/django-us-markets',
    license='MIT License',
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests',
    install_requires=[],
    classifiers=[
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
    ],
)
