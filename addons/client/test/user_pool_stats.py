from core.user import user_main
from core import defs

user_pool=user_main.getUserPool()
print "Hits: %s Misses: %s Total: %s"%(user_pool.hits,user_pool.misses,user_pool.hits+user_pool.misses)
print "POOL LEN: %s MAX POOL Size: %s"%(user_pool._UserPool__pool_len,defs.MAX_USER_POOL_SIZE)

#user_pool._UserPool__pool_by_id)
