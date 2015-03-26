PRMS Adaptor
============


In order for PRMS data to be interoperable with the rest of the Virtual
Watershed (VW) ecosystem, we need to be able to convert to and from NetCDF format,
the reference data format of the VW. To do this we've developed the PRMS
adaptors as an element of the growing suite of VW adaptors. 

*include more details if you like*


How to use them
---------------

.. code-block:: python 
    
    """This should be an example of how to use the functions you wrote to
        convert between NetCDF and PRMS
    """
    from dataConverter import prmsToNetcdf, netcdfToPrms, PRMS
    
    # show how your code accomplishes this
    prms_file = 'prms.txt'
    prms_object = PRMS(prms_file)
    # convert PRMS data to NetCDF
    netcdf_from_prms = prmsToNetcdf(prms_object)

    # show that you can convert back with no loss
    prms = netcdfToPrms(netcdf_from_prms)

    # somehow prove that in fact these are the same
    assert prms.data == prms_object.data



Module Documentation
--------------------

(This is just an example based on the fake code I wrote in the code block
above).

The class ``PRMS`` is found in ``gdalConverter.py``. It takes a file path as 
input and provides the following methods for manipulation:

* Method 1
* Method 2
* Method 3

To convert a ``PRMS`` object to a ``NetCDF`` Dataset, just call
``prmsToNetcdf``, which can be found in the ``dataConverter.py`` module.
To convert a ``PRMS`` object back to a ``NetCDF`` Dataset, use the function
``netcdfToPrms`` also found in ``dataConverter.py``.
