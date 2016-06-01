import json
from cli import *

# Here's our decorator.  The wrapper simply wraps the previous
# function in a json.loads() call to load the json encoded
# string into a dictionary and then returns it.
def dict_decorator(target_function):
    def wrapper(cmd):
        return json.loads(target_function(cmd))
    return wrapper

# Let's see how the current beahvior is.
original = clid("show interface brief")
print "Type of original clid output: " + str(type(original))
print original
# This doesn't use the @ decorator syntax but it _is_ a
# decorator none the less.
clid = dict_decorator(clid)


# Let's see what our decorator does
new = clid("show interface brief")
print "Type of new clid output: " + str(type(new))
print new
