from core.user import user_main
onlines=user_main.getOnline().getOnlineUsers()
for user_id in onlines:
    print "%s\t%s\t%s"%(user_id,onlines[user_id].calcCurrentCredit(),onlines[user_id].getTypeObj().getInOutBytes(1))
print str(onlines[1].getInstanceInfo(1))
#print str(onlines[1].getInstanceInfo(2))

