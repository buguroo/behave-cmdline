behave-cmdline
==============

`behave-cmdline` helps you to test your command line applications using
behave.

.. warning::

   This is a work-in-progress project. API may change while in in
   version v0.X.Y. 


Usage
-----

1. Load the steps for your language
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From your `steps.py` file import the step definition for your language:

.. code-block:: python

   import behave_cmdline.steps.en  # For English
   # import behave_cmdline.steps.es  # For Spanish


2. Add some hooks in your environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add this two lines in your `environment.py`, in the functions before and
after scenario. If you don't have those, then create them as in the
example:

.. code-block:: python

   from behave_cmdline import environment as cmdline

   def before_scenario(context, scenario):
       cmdline.before_scenario(context, scenario)
       # The rest of your code goes here...

   def after_scenario(context, scenario):
       cmdline.after_scenario(context, scenario)
       # The rest of your code goes here...


3. Write some features
~~~~~~~~~~~~~~~~~~~~~~

Now you can invoke the steps from your features as usual. For the step
definition you can check the file `behave_cmdline/steps/_steps.py` and
`behave_cmdline/steps/i18n.py`.

.. todo:: Write some feature examples.


Translations
------------

You can help us translating the steps to your own language. Please,
issue a pull request adding your translations to the file
`behave_cmdline/steps/i18n.py`.
