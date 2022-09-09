from setuptools import find_packages, setup

install_requires = ''
with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

setup(
    name='pyCSM',
    description="CSM Python Client",
    long_description="CSM RESTful API Python Client.",
    author="Dominic Blea",
    version='1.0.1',
    author_email="dblea00@ibm.com",
    maintainer="Dominic Blea",
    keywords=["IBM", "CSM Storage"],
    install_requires=install_requires,
    license="Apache License, Version 2.0",
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])
