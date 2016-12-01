{* Active Leaves List
   $active_leaves: array of associative arrays containing active leaf infos

*}

{include file="admin_header.tpl" title="Active Leaves List" selected="Bandwidth"}
{include file="err_head.tpl"}

{include file="refresh_header.tpl" title="Refresh"}

{listTable title="Active Leaves" cols_num=11}
	{listTR type="header"}
	    {listTD}
		IP
	    {/listTD}
	    
	    {listTD}
		Send Bytes
	    {/listTD}

	    {listTD}
		Recv Bytes
	    {/listTD}

	    {listTD}
		Send Rate
	    {/listTD}

	    {listTD}
		Recv Rate
	    {/listTD}

	    {listTD}
		Send Pkts
	    {/listTD}

	    {listTD}
		Recv Pkts
	    {/listTD}

	    {listTD}
		Send Leaf
	    {/listTD}

	    {listTD}
		Recv Leaf
	    {/listTD}

	    {listTD}
		Send Interface
	    {/listTD}

	    {listTD}
		Recv Interface
	    {/listTD}


	{/listTR}
		
	{foreach from=$active_leaves key=ip item=arr}
	    {listTR type="body" cycle_color=TRUE}
		{listTD}
		    {$ip}
		{/listTD}

		{listTD}
		    {$arr[0].bytes|byte}
		{/listTD}
		{listTD}
		    {$arr[1].bytes|byte}
		{/listTD}

		{listTD}
		    {$arr[0].rate|byte:"bit/s"}
		{/listTD}
		{listTD}
		    {$arr[1].rate|byte:"bit/s"}
		{/listTD}

		{listTD}
		    {$arr[0].pkts|price}
		{/listTD}
		{listTD}
		    {$arr[1].pkts|price}
		{/listTD}

		{listTD}
		    {$arr[0].leaf_name}
		{/listTD}
		{listTD}
		    {$arr[1].leaf_name}
		{/listTD}

		{listTD}
		    {$arr[0].interface_name}
		{/listTD}
		{listTD}
		    {$arr[1].interface_name}
		{/listTD}
	    {/listTR}
	{/foreach}

{/listTable}
{addRelatedLink}
    <a href="/IBSng/admin/bw/interface_list.php" class="RightSide_links">
	Interface list
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/bw/static_ip_list.php" class="RightSide_links">
	StaticIP list
    </a>
{/addRelatedLink}

{setAboutPage title="Active Leaves"}

{/setAboutPage}

{include file="admin_footer.tpl"}