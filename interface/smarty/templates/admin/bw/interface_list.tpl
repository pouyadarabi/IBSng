{* interfaces  List
   $interfaces: array of associative arrays containing interfaces infos

*}

{include file="admin_header.tpl" title="Interface List" selected="Bandwidth"}
{include file="err_head.tpl"}

{listTable title="Interface List" cols_num=4}
	{listTableHeaderIcon action="view" close_tr=TRUE}
	{listTR type="header"}
	    {listTD}
		Row
	    {/listTD}
	    {listTD}
		ID
	    {/listTD}
	    {listTD}
		Interface Name
	    {/listTD}
	    {listTD}
		Comment
	    {/listTD}
	{/listTR}
		
	{foreach from=$interfaces item=interface}
	    {listTR type="body" cycle_color=FALSE}
		{listTD}
		    {counter}
		{/listTD}
		{listTD}
		    {$interface.interface_id}
		{/listTD}
		{listTD}
		    {$interface.interface_name}
		{/listTD}
		{listTD}
		    {$interface.comment}
		{/listTD}
		{listTD icon="TRUE"}
		    <a href="/IBSng/admin/bw/interface_info.php?interface_name={$interface.interface_name|escape:"url"}">
			{listTableBodyIcon action="view" cycle_color=TRUE}
		    </a>
		{/listTD}
	    {/listTR}
	{/foreach}

{/listTable}
{addRelatedLink}
    <a href="/IBSng/admin/bw/add_interface.php" class="RightSide_links">
	Add New Interface
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