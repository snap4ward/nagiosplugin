New 1.x API design
==================

A probe queries the system to obtain data and return it as a list of
MeasuredPerformance objects::

   class Probe(object):
      def __init__(self, *args, **kwargs):
         pass

      def __call__(self):
         pass

An evaluator is called with the MeasuredPerformance objects from the probe and
transforms them into Status and Performance objects::

   class Evaluator(object):
      def __init__(self, *args, **kwargs):
         pass

      def __call__(self, probe):
         pass

      @property
      def status(self):
         return [Status(...)]

      @property
      def performance(self):
         return [Performance(...)]

A Plugin object defines various plugin life cycle methods::

   class Plugin(object):
      name = 'short name'
      description = 'plugin description'
      version = 'plugin version'
      default_timeout = 15

      def __init__(self):
         pass

      def cmdline(self, optparse):
         optparse.add_option(...)

      def setup(self, options, arguments):
         pass

      def precheck(self):
         pass

      def postcheck(self):
         pass

      @property
      def probe(self):
         return Probe(...)

      @property
      def evaluator(self):
         return Evaluator(...)

      def message(self, status):
         return Status.merge_messages(status)
