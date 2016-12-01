import gc

print "Is Enabled? %s"%gc.isenabled()
print gc.set_debug(gc.DEBUG_STATS)
#print gc.set_debug(gc.DEBUG_UNCOLLECTABLE)
#print gc.set_debug(gc.DEBUG_COLLECTABLE)
print gc.get_debug()
print "Objects: %s"%gc.garbage
print "Collect: %s"%gc.collect()

import re
print "re: %s"%re.purge()
