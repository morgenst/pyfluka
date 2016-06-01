.. _plugins_ref:

Builtin plugins
===============

This page summarises the available builtin plugins shipped with pyfluka. Their intend as well as their configuration
will be discussed in depth. For further reference see the API documentation.


Decorator plugin
----------------

Decorates the stored data by arbitrary information. This is particularly useful if you intend to create a table in the
 end and want to display any builtin data, such as half life times or specific limits for each radionuclide.

Configuration:

.. code-block:: yaml

      Decorator:
        - EInh

Filter plugin
-------------

Filters data corresponding to given quantity and threshold. Threshold can be either absolute or relative. By default
absolute thresholds have to be given with value and unit, while relative thresholds must be given as floats.

Configuration (absolute): Filters data such that all entries with activies below 10 Bq are removed

.. code-block:: yaml

      Filter:
        - quantity: Activity
        - threshold: 10 Bq

Configuration (relative): Filters data such that all entries with activities contributing less than 1% to the total
 activity are removed

.. code-block:: yaml

      Filter:
        - quantity: Activity
        - threshold: 0.01


Summation plugin
----------------

Calculates the sum of a given quantity stored in the central data store.

.. code-block:: yaml

      SummationOperator:
        quantity: quantity
        stored_quantity (optional): result name

By default the result is stored under "Summed"+quantity_name, e.g. if the total activity is requested to be calculated
from the list of activities of a single isotope it will be stored as SummedActivity. This can be customised via the
  stored_quantity initialisation property.


Multiplication plugin
---------------------

The multiplication plugin multiplies arbitrary quantities, which can either be PhysicsQuantities or scalars. Since
several multiplication operations can be requested the plugins must have a unique name assigned in the configuration,
e.g. appending _n for the nth definition of the plugin.

.. code-block:: yaml

      MultiplicationOperator_2:
            type: type
            multiplier: SpecificActivity
            multiplicand: const:4.000000e-04 s*m^-3
            product: ReleasedSpecificActivityMulti

with type being either scalar for multiplication with scalar or dict for multiplication of dictionaries. Multiplier
and multiplicand define the multiplier and multiplicand which can be of scalar constant type or be read from the data
store by providing the name. Scalar quantities can be decorated by a unit given as string argument. Product is the result
of the multiplication. A name under which it is stored in the central data store must be provided. For later
calculations it can be referred by that name.


Table Maker
-----------

The Table Maker plugin provides functionality for generic creation of tabulated data.

.. code-block:: yaml

      TableMaker:
       cols:
        - col1
        - col2

Via cols option columns to be printed can be requested. Their names must correspond to corresponding entries in the
central data store. By default column headers are retrieved from the corresponding PhysicsQuantity definition, but can
be customised via ...