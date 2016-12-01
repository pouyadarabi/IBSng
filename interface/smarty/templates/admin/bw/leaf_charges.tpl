{* interfaces  List
   $charge_names: array of charge_names 
   $leaf_name: name of leaf
   $interface_name
   

*}

{include file="admin_header.tpl" title="Leaf `$leaf_name` Charges" selected="Bandwidth"}
{include file="err_head.tpl"}

{listTable title="Leaf `$leaf_name` Charges" cols_num=2}
	{listTableHeaderIcon action="view" close_tr=TRUE}
	{listTR type="header"}
	    {listTD}
		Row
	    {/listTD}
	    {listTD}
		Charge Name
	    {/listTD}
	{/listTR}
		
	{foreach from=$charge_names item=charge_name}
	    {listTR type="body" cycle_color=FALSE}
		{listTD}
		    {counter}
		{/listTD}
		{listTD}
		    {$charge_name}
		{/listTD}
		{listTD icon="TRUE"}
		    <a href="/IBSng/admin/charge/charge_info.php?charge_name={$charge_name|escape:"url"}">
			{listTableBodyIcon action="view" cycle_color=TRUE}
		    </a>
		{/listTD}
	    {/listTR}
	{/foreach}

{/listTable}
{addRelatedLink}
    <a href="/IBSng/admin/bw/interface_info.php?interface_name={$interface_name}" class="RightSide_links">
	Interface <b>{$interface_name}</b> Info 
    </a>
{/addRelatedLink}

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

{addRelatedLink}
    <a href="/IBSng/admin/bw/active_leaves.php" class="RightSide_links">
	Active Leaves list
    </a>
{/addRelatedLink}

{setAboutPage title="Interface List"}

{/setAboutPage}

{include file="admin_footer.tpl"}