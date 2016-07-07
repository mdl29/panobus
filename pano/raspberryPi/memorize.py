"""
memorize.py is a simple decorator for memoizing a
function across multiple program executions.

A function decorated with @memorize caches its return
value every time it is called. If the function is called
later with the same arguments, the cached value is
returned (the function is not reevaluated). The cache is
stored as a .cache file in the current directory for reuse
in future executions. If the Python file containing the
decorated function has been updated since the last run,
the current cache is deleted and a new cache is created
(in case the behavior of the function has changed).

BEWARE: only pure functions should be memoized!
Otherwise you might encounter unexpected results. Ask
yourself:
* does your function alter a global object?
* do you need to see the result of print statements?
* Does the result of your function depend on something
 outside of the application that may not behave like it
 used to (external classes, methods, functions, or data)?

DO NOT use this decorator if you are planning on
running multiple instances of the memoized function
concurrently. If there is sufficient interest this feature
may be supported in the future.

DO NOT use this decorator for functions that take
arguments that cannot be dictionary keys (such as lists).
Since the cache is stored internally as a dictionary,
no information will be cached and no memoization will
take place.
"""
import pickle
import collections
import functools
import inspect
import os.path
import re
import unicodedata

def memorize(do_cache, default):
    return lambda f: Memorize(do_cache,default,f)

class Memorize(object):
    '''
    A function decorated with @memorize caches its return
    value every time it is called. If the function is called
    later with the same arguments, the cached value is
    returned (the function is not reevaluated). The cache is
    stored as a .cache file in the current directory for reuse
    in future executions. If the Python file containing the
    decorated function has been updated since the last run,
    the current cache is deleted and a new cache is created
    (in case the behavior of the function has changed).
    '''
    def __init__(self, do_cache, default,  func):
        self.do_cache = do_cache
        self.count = 0
        self.default = default
        self.func = func
        self.set_parent_file() # Sets self.parent_filepath and self.parent_filename
        self.__name__ = self.func.__name__
        self.set_cache_filename()
        self.lcache = {}
        if self.cache_exists():
            self.read_cache() # Sets self.timestamp and self.cache
            if do_cache:
                self.count = len(self.cache) - 1
        else:
            self.cache = [{}]

    def __call__(self,s, *args, **kwargs):
        key = str(args) + str(kwargs)
        if self.do_cache == False:
            if not key in self.lcache:
                self.lcache = self.cache[self.count]
                self.count += 1

            print(self.lcache)
            if self.count % len(self.cache) == 0:
                self.count = 0
            if key in self.lcache:
                v = self.lcache.pop(key)
            else:
                v = self.default

        else:
            if key in self.cache[self.count]:
                self.count += 1
                self.cache.append({})
            v = self.func(s, *args, **kwargs)
            self.cache[self.count][key] = v
            self.save_cache()
        return v

    def set_parent_file(self):
        """
        Sets self.parent_file to the absolute path of the
        file containing the memoized function.
        """
        rel_parent_file = inspect.stack()[-1].filename
        self.parent_filepath = os.path.abspath(rel_parent_file)
        self.parent_filename = _filename_from_path(rel_parent_file)

    def set_cache_filename(self):
        """
        Sets self.cache_filename to an os-compliant
        version of "file_function.cache"
        """
        filename = _slugify(self.parent_filename.replace('.py', ''))
        funcname = _slugify(self.__name__)
        self.cache_filename = filename+'_'+funcname+'.cache'

    def read_cache(self):
        """
        Read a pickled dictionary into self.timestamp and
        self.cache. See self.save_cache.
        """
        with open(self.cache_filename, 'rb') as f:
            data = pickle.loads(f.read())
            self.cache = data

    def save_cache(self):
        """
        Pickle the file's timestamp and the function's cache
        in a dictionary object.
        """
        with open(self.cache_filename, 'wb+') as f:
            f.write(pickle.dumps(self.cache))

    def cache_exists(self):
        '''
        Returns True if a matching cache exists in the current directory.
        '''
        if os.path.isfile(self.cache_filename):
            return True
        return False

    def __repr__(self):
        """ Return the function's docstring. """
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """ Support instance methods. """
        return functools.partial(self.__call__, obj)

def _slugify(value):
    """
    Normalizes string, converts to lowercase, removes
    non-alpha characters, and converts spaces to
    hyphens. From
    http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = re.sub(r'[^\w\s-]', '', value.decode('utf-8', 'ignore'))
    value = value.strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    return value

def _filename_from_path(filepath):
    return filepath.split('/')[-1]
