.. pyCSM documentation master file, created by
   sphinx-quickstart on Tue Mar 15 14:26:56 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyCSM's documentation!
=================================
   The pyCSM library is a python library designed to make RESTAPI calls to an IBM Copy Services Manager (CSM) server.
   CSM is a product used to manage block level replication for IBM Storage Systems.

   Solutions in CSM range from point in time and Safeguarded Copy management to more complex two, three or four
   site replication.

   For more details on CSM or for details on the CSM RESTAPI, check out the `CSM Documentation <https://www.ibm.com/docs/en/csm>`_.

==================================
**How to use the pyCSM library**
==================================
   The pyCSM library is broken up into three main sections:  Authorization, Clients and Services.

   When you use the library you can choose from one of the following configurations.

**Client class only**
---------------------
   This option allows the caller to init a python class which manages the authorization automatically
   for all subsequent calls to the server.

   The caller can pass in the authentication information once during the init and then calls to methods withing that
   class will ensure a token is obtained or **automatically renewed**.

   **It is recommended that you use the client classes so that you do not have to manage the authorization in your code.**

   Example:

   ``sessClient = session_client.sessionClient("localhost", "9559", "csmadmin", "csm")``
   ``print(sessClient.get_session_overviews().json())``

**Authorization + Services**
----------------------------
   This option allows the caller to manage the authorization calls itself.

   You can use the Authorization methods to obtain a token which can then be passed into the services methods.

   Using this option gives a caller greater control over when the token is obtained, however it would be up to the
   caller to handle failures when the token expires.

   Example:

   ``token = auth.get_token("https://localhost:9559/CSM/web", "csmadmin", "csm")``
   ``print(session_service.get_session_overviews("https://localhost:9559/CSM/web", token).json())``

**Services only**
-----------------
   This option allows the caller to manage the authorization itself through a means other than using
   the Authorization call provided by pyCSM.

   The caller will need to obtain a token still in order to pass into the Services calls.

   Example:

   ``print(session_service.get_session_overviews("https://localhost:9559/CSM/web", token).json())``

**Specifying Properties**
-------------------------
   Whether using one of the clients, or using the services, there are default properties that can be
   set for how the calls are made.

   Available properties are defined in a Python dictionary.  The current options are the following:

   * "language" - Defines the language any translated results should be returned.  Default is "en-US".
   * "verify"   - Set to True to verify the server side certificate.  Default is False.
   * "cert"     - The client certificate.  Default is None.

   You can query for the current property values from either the client or the service.
   A dictionary is returned from both.

   Example Using Client:

   ``sessClient = session_client.sessionClient(server_address, server_port, username, password)``
   ``properties = sessClient.get_properties()``

   Example Using Service:

   ``session_service.get_properties()``

   To modify the properties call the change_properties() method on either the client or service depending
   on what interface you're using.  Pass in a dictionary containing the values you wish to change.

   Example Changing the language to French:

   ``my_properties = {"language": "de"}``
   ``sessClient.change_properties(my_properties)``

   After changing the properties all calls to the client or service will use the new properties.


   **NOTE: The verify property defaults to False and the cert property to None.**
   **It is highly recommended that you set verify to True and specify a CA cert to use for a secure connection**

   Example:

   ``my_properties = {"verify": "True", "cert": "cert": ('/home/certs/localhost.crt', '/home/certs/private.key')}``
   ``sessClient.change_properties(my_properties)``


=========================================
**Clients, Authorization and Services**
=========================================

**Clients**
-----------
   There are three clients that can be used for various actions on the CSM server.

   The :doc:`../clients_docs/session_client` class is designed to make calls related to managing CSM sessions and
   replication.

   The :doc:`../clients_docs/hardware_client` class is designed to make calls for actions pertaining to setting
   up and managing connections from CSM to the Storage System.

   The :doc:`../clients_docs/system_client` class is designed to make calls pertaining to the server and system
   configuration.

**Services**
------------
   The :doc:`../hardware_service_docs/hardware` provides methods around managing the hardware connection from
   CSM to the storage system or retrieving information from the storage system.

   The :doc:`../system_service_docs/system` provides methods for configuring the CSM server, creating log packages,
   and other server level commands.

   The :doc:`../session_service_docs/sessions` provides the methods for managing sessions on the CSM server.  This
   includes creating and running commands to sessions.

   The :doc:`../session_service_docs/copysets` provides the methods for adding, removing and exporting copy sets
   from a CSM session.

   The :doc:`../session_service_docs/schedule` provides the methods for viewing and running scheduled tasks on
   the CSM server.

**Authorization**
-----------------
   The :doc:`../authorization_docs/authorization` module contains the method to obtain a token from the CSM server.

   **NOTE: This does not need to be used if you are using one of the clients.**


=============================
Index for pyCSM Documentation
=============================

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Clients Documentation

   clients_docs/*

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Session Services Documentation

   session_service_docs/*

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Hardware Services Documentation

   hardware_service_docs/*

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: System Services Documentation

   system_service_docs/*

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Authorization Documentation

   authorization_docs/*

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
