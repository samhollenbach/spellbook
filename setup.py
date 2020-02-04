from setuptools import setup, find_packages


def readme():
    try:
        return open('README.md').read()
    except Exception as err:  # noqa
        pass
    return ''


setup(
        name='spellbook',
        version='0.0.1',
        author="Sam Hollenbach",
        author_email="samhollenbach@gmail.com",
        description="A Collection of Python Spells",
        long_description=readme(),
        url='http://github.com/samhollenbach/spellbook',
        license='ALv2',
        packages=find_packages(exclude=['test']),
        install_requires=[

        ],
        test_suite='nose.collector',
        tests_require=[
            'nose',
            'mock',
            ],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Software Development :: Libraries',
            'Topic :: Utilities',
            ]
        )