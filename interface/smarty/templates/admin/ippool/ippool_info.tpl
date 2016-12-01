{* IPpool Info 
    Show IP pool Informations and show IP's of each pool
*}
{include file="admin_header.tpl" title="IPpool Information" selected="IPPool"}
{include file="err_head.tpl"}
{if !$is_editing}
{headerMsg var_name="update_successfull"}IP pool Updated Successfully.{/headerMsg}
{headerMsg var_name="ip_deleted_successfull"}IP Deleted from IP Pool Successfully.{/headerMsg}
{headerMsg var_name="ip_added_successfull"}IP Added To IP Pool Successfully.{/headerMsg}

<table border=0 width=100%>
    <tr>
	<td width=48% align=right valign=top>
	    {viewTable title="IPPool Information" table_width="220"}
	    {addEditTD type="left" err="IPPool_ID_err"}
		    IP Pool ID
	    {/addEditTD}
	    {addEditTD type="right"}
		{$ippool_id}
	    {/addEditTD}
	    {addEditTD type="left" err="IPPool_ID_err"}
	        IP Pool Name
	    {/addEditTD}
	    {addEditTD type="right"}
		    {$ippool_name}
	    {/addEditTD}
	    {addEditTD type="left" err="name_err" comment=TRUE}
	        Comment
		{/addEditTD}

	{addEditTD type="right" comment=TRUE}
	        {$comment}
	{/addEditTD}
	{/viewTable}
<br>
    {if $can_change}
    	<form method=POST action="ippool_info.php" name="add_ip_form">
	    {addEditTable title="Add IP(s) To Pool" table_width="220" action_icon="add"}
		{addEditTD type="left" err="add_ip_err"}
		    IP(s)
	    {/addEditTD}
	    {addEditTD type="right"}
		<input type=text name=add_ip value="{ifisinrequest name="add_ip"}" class=text>{multistr form_name="add_ip_form" input_name="add_ip" left_pad="FALSE"}
	    {/addEditTD}
	    {/addEditTable}
	<input type=hidden name=ippool_name value="{$ippool_name}">
	<input type=hidden name=add_submit>
	</form>

	<form method=POST action="ippool_info.php" name="del_ip_form">
	    {addEditTable title="Delete IP(s) From Pool" table_width="220" action_icon="delete"}
		{addEditTD type="left" err="del_ip_err"}
		    IP(s)
	    {/addEditTD}
	    {addEditTD type="right"}
		<input type=text name=del_ip value="{ifisinrequest name="del_ip"}" class=text>{multistr form_name="del_ip_form" input_name="del_ip" left_pad="FALSE"}
	    {/addEditTD}
	    {/addEditTable}
	<input type=hidden name=ippool_name value="{$ippool_name}">
	<input type=hidden name=del_submit>
	</form>
    {/if}
</td>
<td width=4%></td>
<td width=48% align=left valign=top>
    {listTable title="IP List" cols_num=3}
	{if $can_change}
	    {listTableHeaderIcon action="delete" close_tr=TRUE}
	{/if}    
	    {listTR type="header"}
		{listTD}
			Row
	        {/listTD}
		{listTD}
			IP Address
	        {/listTD}
	        {listTD}
			Status
	        {/listTD}
	    {/listTR}
	{foreach from=$ip_list item=ip}
	    {listTR type="body"}
		{listTD}    
		    {counter}
	        {/listTD}
		{listTD}    
		    {$ip}
	        {/listTD}
		{listTD}
		    {if in_array($ip,$used)}
			Used
		    {else}
			Free
		    {/if}
		{/listTD}    
		{if $can_change}
			{listTD icon="TRUE"}
		        	<a href="ippool_info.php?del_submit=1&del_ip={$ip|escape:"url"}&ippool_name={$ippool_name|escape:"url"}" {jsconfirm msg="Are you sure you want to delete $ip?"}>
				    {listTableBodyIcon action="delete" cycle_color="TRUE"}
				</a>
			{/listTD}
		{/if}    
	    {/listTR}
	{/foreach}
    {/listTable}
</td>
</tr>
</table>
{if $can_change}	
{addRelatedLink}
    <a href="ippool_info.php?edit=1&ippool_name={$ippool_name|escape:"url"}" class="RightSide_links">
	Edit IPPool <b>{$ippool_name}</b>
    </a>
{/addRelatedLink}
{addRelatedLink}
        <a href="ippool_info.php?delete=1&ippool_name={$ippool_name|escape:"url"}" 
		{jsconfirm msg="Are you sure you want to delete IP Pool? Warning: You should remove ippool from ras and users"}
		 class="RightSide_links">
	Delete Ippool <b>{$ippool_name}</b>
    </a>
{/addRelatedLink}
{/if}

{else}

	<form method=POST action="ippool_info.php">
	<input type=hidden name=update value=1>
	<input type=hidden name=ippool_id value="{$ippool_id}">
	<input type=hidden name=old_ippool_name value="{$ippool_name}">
	    {addEditTable title="Edit IPPool Information"}
	    {addEditTD type="left" err="IPPool_ID_err"}
	        IP Pool ID
	    {/addEditTD}
	    {addEditTD type="right"}
		{$ippool_id}
	    {/addEditTD}
	    {addEditTD type="left" err="IPPool_ID_err"}
	        IP Pool Name
	    {/addEditTD}
	    {addEditTD type="right"}
		    <input class="text" type=text name="new_ippool_name" value="{$ippool_name}">
	    {/addEditTD}
	    {addEditTD type="left" err="name_err" comment=TRUE}
	        Comment
		{/addEditTD}

	{addEditTD type="right" comment=TRUE}
	    <textarea name="comment" class=text>{$comment|strip}</textarea>
	{/addEditTD}
	{/addEditTable}

{addRelatedLink}
        <a href="ippool_info.php?ippool_name={$ippool_name}" class="RightSide_links">
	Ippool <b>{$ippool_name}</b> Info
    </a>
{/addRelatedLink}
{/if}
{addRelatedLink}
    <a href="ippool_list.php" class="RightSide_links">
	 List IPPool
    </a>
{/addRelatedLink}
{addRelatedLink}
    <a href="/IBSng/admin/ippool/add_new_ippool.php" class="RightSide_links">
	Add New IPPool
    </a>
{/addRelatedLink}
{setAboutPage title="IPPool information"}
Here you can Edit Add and 
Delete IP(s)of a IPPool.
{/setAboutPage}

{include file="admin_footer.tpl"}