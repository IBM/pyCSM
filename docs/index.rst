.. pyCSM documentation master file, created by
   sphinx-quickstart on Tue Mar 15 14:26:56 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyCSM's documentation!
=================================
The pyCSM library is a python library designed to make RESTAPI calls to an IBM Copy Services Manager (CSM) server.
CSM is a product used to manage block level replication for IBM Storage Systems.  Solutions
in CSM range from point in time and Safeguarded Copy management to more complex two, three or four site replication.
|
For more details on CSM or for details on the CSM RESTAPI, check out the [CSM Documentation](https://www.ibm.com/docs/en/csm)
|
##How to use the pyCSM library
The pyCSM library is broken up into three main sections:  Authorization, Clients and Services.
When you use the library you can choose from one of the following configurations.
|
##Client class only
This option allows the caller to init a python class which manages the authorization automatically
for all subsequent calls to the server.  The caller can pass in the authentication information once during the init
and then calls to methods withing that class will ensure a token is obtained or automatically renewed.
It is recommended that you use the client classes so that you do not have to manage the authorization in your code.
|
##Authorization + Services
This option allows the caller to manage the authorization calls itself.  You can use the
Authorization methods to obtain a token which can then be passed into the services methods.  Using this option gives
a caller greater control over when the token is obtained, however it would be up to the caller to handle failures
when the token expires.
|
##Services only
This option allows the caller to manage the authorization itself through a means other than using
the Authorization call provided by pyCSM.  The caller will need to obtain a token still in order to pass into the
Services calls.


.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Authorization Documentation
The Authorization module contains the method to obtain a token from the CSM server.

   authorization_docs/*

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Clients Documentation
There are three clients that can be used for various actions on the CSM server.
The [client_session](clients/client_session.py) class is designed to make calls related to managing CSM sessions and
replication.
The [client_hardware](clients/client_hardware.py) class is designed to make calls for actions pertaining to setting
up and managing connections from CSM to the Storage System.
The [client_system](clients/client_system.py) class is designed to make calls pertaining to the server and system
configuration.

   clients_docs/*

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Session Services Documentation
The [Session service](session_service/sessions.py) provides the methods for managing sessions on the CSM server.  This
includes creating and running commands to sessions.
The [Copy Sets service](session_service/copysets.py) provides the methods for adding, removing and exporting copy sets
from a CSM session.
The [Schedule service](session_service/schedule.py) provides the methods for viewing and running scheduled tasks on
the CSM server.

   session_service_docs/*

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Hardware Services Documentation
The [Hardware service](hardware_service/hardware.py) provides methods around managing the hardware connection from
CSM to the storage system or retrieving information from the storage system.

   hardware_service_docs/*

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: System Services Documentation
The [System service](system_service/system.py) provides methods for configuring the CSM server, creating log packages,
and other server level commands.
   system_service_docs/*

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
