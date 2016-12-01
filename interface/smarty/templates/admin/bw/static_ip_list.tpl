{* interfaces  List
   $bw_static_ips: associative array in format $ip=>$info

*}

{include file="admin_header.tpl" title="Bw StaticIP List" selected="Bandwidth"}
{include file="err_head.tpl"}
{headerMsg var_name="del_ip_success"}StaticIP Deleted Successfully.{/headerMsg}

{listTable title="BW StaticIP List" cols_num=4}
	{listTableHeaderIcon action="edit"}
	{listTableHeaderIcon action="delete" close_tr=TRUE}
	{listTR type="header"}
	    {listTD}
		ID
	    {/listTD}
	    {listTD}
		IP
	    {/listTD}
	    {listTD}
		Send Leaf
	    {/listTD}
	    {listTD}
		Receive Leaf
	    {/listTD}
	{/listTR}
		
	{foreach from=$bw_static_ips item=info}
	    {listTR type="body" cycle_color=FALSE}
		{listTD}
		    {$info.static_ip_id}
		{/listTD}
		{listTD}
		    {$info.ip}
		{/listTD}
		{listTD}
		    {$info.tx_leaf_name}
		{/listTD}

		{listTD}
		    {$info.rx_leaf_name}
		{/listTD}
		{listTD icon="TRUE"}
		    <a href="/IBSng/admin/bw/add_static_ip.php?edit=1&ip_addr={$info.ip|escape:"url"}">
			{listTableBodyIcon action="edit"}
		    </a>
		{/listTD}

		{listTD icon="TRUE"}
		    <a href="/IBSng/admin/bw/static_ip_list.php?delete_ip=1&ip_addr={$info.ip|escape:"url"}" {jsconfirm}>
			{listTableBodyIcon action="delete" cycle_color=TRUE}
		    </a>
		{/listTD}
	    {/listTR}
	{/foreach}

{/listTable}

{addRelatedLink}
    <a href="/IBSng/admin/bw/add_static_ip.php?add=1" class="RightSide_links">
	Add Bw StaticIP
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/bw/interface_list.php" class="RightSide_links">
	Interface list
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/bw/active_leaves.php" class="RightSide_links">
	Active Leaves list
    </a>
{/addRelatedLink}


{setAboutPage title="StaticIP List"}

{/setAboutPage}

{include file="admin_footer.tpl"}