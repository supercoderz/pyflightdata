Quickstart
==========

Let's dive in with a quick example.

The main interface to pyflightdata is the FlightData class. This abstracts all the data access mechanism and also maintains the 
authenticated session to flightradar24 for users who have a paid membership.

Start by initializing the FlightData class and optionally login to the account.

.. code-block :: python
    :linenos:

    from pyflightdata import FlightData

    f=FlightData()
    f.login(foo@bar.com,foobar)

Once you login, the session token is stored on the FlightData.AUTH_TOKEN variable.

The most common use case would be to get information about a particular flight where you know the flight number.

.. code-block :: python
    :linenos:

    # get the last 5 flights for AI101
    f.get_history_by_flight_number('AI101')[-5:]

Once you have this information, you might want to inspect the flights before and after this route for a particular aircraft.

.. code-block :: python
    :linenos:

    # get the last 5 flights for the aircraft VT-ANL
    # this is an Air India aircraft
    api.get_history_by_tail_number('VT-ANL')[-5:]

You can also get the information about the aircraft itself like its age etc.

.. code-block :: python
    :linenos:

    # get the information for a particular aircraft using tail number
    api.get_info_by_tail_number('VT-ANL')

Internally pyflightdata tracks whether you are authenticated or not and the data returned by the above methods will be
restricted accordingly. Users who are not authenticated will only see data for the free limits, which is usually a week.

Please refer to the examples Jupyter notebook in the next section and the API documentation for details on all the other data that you can get using pyflightdata.