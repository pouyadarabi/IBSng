from core.event import periodic_events
i=0
for evt in periodic_events.getManager().events:
    print i,evt
    i+=1