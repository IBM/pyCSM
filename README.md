# CSM Python Client
[![Build Status](https://travis.ibm.com/pyCSM/pyCSM.svg?token=S4B3H6Vzv2oQaoCcyYeT&branch=main)](https://github.ibm.com/pyCSM/pyCSM)
[![Documentation Status](https://readthedocs.org/projects/pycsm/badge/?version=latest)](https://pycsm.readthedocs.io/en/latest/?badge=latest)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/5999/badge)](https://bestpractices.coreinfrastructure.org/projects/5999)

This repository contains the IBM Python client for RESTful communication to an IBM Copy Services Manager server.  The Python client enables full management and monitoring of the replication and the components necessary for replication in a Copy Services Manager environment. 

The repository provides two options for implementations.  
- **Clients**      - The client classes are [session_client.py](pyCSM/clients/session_client.py), [hardware_client.py](pyCSM/clients/hardware_client.py), and [system_client.py](pyCSM/clients/system_client.py).  These classes are designed to automatically obtain and manage a token to CSM for communication.  A client class can be instantiated and then used to call the methods that perform the desired actions.   
- **Services**     - The service classes are located under [session_service](pyCSM/services/session_service), [hardware_service](pyCSM/services/hardware_service), and [system_service](pyCSM/services/system_service) and can be used if the caller wishes to manage the connection and token themselves.  These are the same classes that are called from the client classes. 


## Python Compatibility
The content in this collection supports Python 3.6 and higher 

## Installation 

Communication to the Copy Services Manager server uses the RESTful interface and thus does not require an installation of client code.  
Clone the repository, and then add it to your PYTHONPATH directory. The Python client is then ready for import and use.

The pyCSM library can also be installed using pip.  
```text
pip install pyCSM
```

## Command Documentation
All commands, their usage and their parameters are documented on [read the docs](https://pycsm.readthedocs.io/en/latest/).

## Usage examples
See documentation for examples on [read the docs](https://pycsm.readthedocs.io/en/latest/).

## The CSM RESTful API
Details on the CSM RESTful API used by this python library can be found in the [Knowledgecenter](https://www.ibm.com/docs/en/csm/6.3.2?topic=reference-csm-rest-api-documentation) for the product. 


## Contributing
To contribute to this library, please see [CONTRIBUTING.md](CONTRIBUTING.md) and submit a contributor license agreement for either an individual or corporation, to those listed as maintainers [here](MAINTAINERS.md).  

See [cla-individual.doc](cla-individual.doc) or [cla-corporate.doc](cla-corporate.doc) for templates of the contributor license agreement.

## License

All source files must include a Copyright and License header. 
```text
#
# (c) Copyright contributors to the pyCSM project
#
```

This project is licensed under the Apache License 2.0. 
Click here to obtain a copy of the [License](http://www.apache.org/licenses/LICENSE-2.0).  

It is a permissive license whose main conditions require preservation of 
copyright and license notices. Contributors provide an express grant of 
patent rights. Licensed works, modifications, and larger works may be 
distributed under different terms and without source code.  

The examples are provided for tutorial purposes only. A complete handling 
of error conditions has not been shown or attempted, and the programs have 
not been submitted to formal IBM testing. The programs are distributed on an 
'AS IS' basis without any warranties either expressed or implied.

If you would like to see the detailed LICENSE click [here](LICENSE).
