{* IP pools  List
   $ippool_infos: array of associative arrays containing ippool infos

*}

{include file="admin_header.tpl" title="IP Pools List" selected="IPPool"}
{include file="err_head.tpl"}

{listTable title="IP Pool List" cols_num=5}
	{listTableHeaderIcon action="view" close_tr=TRUE}
	{listTR type="header"}
	    {listTD}
		Row
	    {/listTD}
	    {listTD}
		ID
	    {/listTD}
	    {listTD}
		IP Pool Name
	    {/listTD}
	    {listTD}
		Comment
	    {/listTD}
	    {listTD}
		IPs(Truncated)
	    {/listTD}
	{/listTR}
		
	{foreach from=$ippool_infos item=ippool_info}
	    {listTR type="body" cycle_color=FALSE}
		{listTD}
		    {counter}
		{/listTD}
		{listTD}
		    {$ippool_info.ippool_id}
		{/listTD}
		{listTD}
		    {$ippool_info.ippool_name}
		{/listTD}
		{listTD}
		    {$ippool_info.comment}
		{/listTD}
		{listTD}
		    {$ippool_info.ips_text|truncate:80:"...":false}
		{/listTD}
		{listTD icon="TRUE"}
		    <a href="/IBSng/admin/ippool/ippool_info.php?ippool_name={$ippool_info.ippool_name|escape:"url"}">
			{listTableBodyIcon action="view" cycle_color=TRUE}
		    </a>
		{/listTD}
	    {/listTR}
	{/foreach}

{/listTable}
{addRelatedLink}
    <a href="/IBSng/admin/ippool/add_new_ippool.php" class="RightSide_links">
	Add New IPPool
    </a>
{/addRelatedLink}
{setAboutPage title="IPPool List"}

{/setAboutPage}

{include file="admin_footer.tpl"}