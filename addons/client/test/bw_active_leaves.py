from core.bandwidth_limit import bw_main

tc = bw_main.getTCRunner()
print tc.getCounters("eth0")
print bw_main.getManager().user_leaves["192.168.1.11/32"][1].getDefaultMinorTC_ID()
print bw_main.getManager().user_leaves["192.168.1.11/32"][0].getTotalMinorTC_ID()
print bw_main.getManager().getAllUserLeavesInfo()["192.168.1.11/32"]