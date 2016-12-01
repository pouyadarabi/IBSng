from core.bandwidth_limit import bw_main

node_ids = bw_main.getLoader().getAllNodeIDs()
for node_id in node_ids:
    node_obj=bw_main.getLoader().getNodeByID(node_id)
    children=node_obj.getChildren()
    print "Node ID %s, children %s"%(node_id,children)
