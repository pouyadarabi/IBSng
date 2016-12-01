from core.ippool import ippool_main
print str(ippool_main.getLoader().getAllIPpoolNames())
print str(ippool_main.getLoader().getIPpoolByName('test').getInfo())