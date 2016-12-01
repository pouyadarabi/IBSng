{* Group List
   $group_infos: array of associative arrays containing group infos
*}

{include file="admin_header.tpl" title="Group List" selected="Group List"}
{include file="err_head.tpl"}

{listTable title="Group  List" cols_num=4}
	{listTableHeaderIcon action="view" close_tr=TRUE}
	{listTR type="header"}
	    {listTD}
		Row
	    {/listTD}
	    {listTD}
		ID
	    {/listTD}
	    {listTD}
		Group Name
	    {/listTD}
	    {listTD}
		Owner
	    {/listTD}
	{/listTR}

		
	{foreach from=$group_infos item=group_info}
	    {listTR type="body"}
		{listTD}
		    {counter}
		{/listTD}
		{listTD}
		    {$group_info.group_id}
		{/listTD}
		{listTD}
		    {$group_info.group_name}
    		{/listTD}
		{listTD}
		    {$group_info.owner_name}
    		{/listTD}
		{listTD icon=TRUE}
		    <a href="/IBSng/admin/group/group_info.php?group_name={$group_info.group_name|escape:"url"}">{listTableBodyIcon action="view" cycle_color="TRUE"}</a>
    		{/listTD}
		
	    {/listTR}
	{/foreach}
{/listTable}
{addRelatedLink}
    <a href="/IBSng/admin/group/add_new_group.php" class="RightSide_links">
	Add New Group
    </a>
{/addRelatedLink}
{include file="admin_footer.tpl"}
