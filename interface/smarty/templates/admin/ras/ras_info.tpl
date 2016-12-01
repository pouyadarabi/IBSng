{* 

Ras Info
    Shows one ras information, including ports and attributes
    on fatal errors that no info can be shown, client is redirected to admin_list
    else error is shown on top of page
    
    Variables:

*}

{include file="admin_header.tpl" title="Ras Information" selected="RAS"}
{include file="err_head.tpl"}

{headerMsg var_name="update_ras_info_success"}
    Ras Info Updated Successfully.
{/headerMsg}

{headerMsg var_name="update_ras_attrs_success}
    Ras Attributes Updated Successfully.
{/headerMsg}

{headerMsg var_name="reset_ras_attrs_success"}
    Ras Attributes Reset Successfully.
{/headerMsg}    

{headerMsg var_name="del_port_success"}
    Port(s) Deleted Successfully.
{/headerMsg}

{headerMsg var_name="add_ippool_success"}
    IP Pool Added To Ras Successfully.
{/headerMsg}

{headerMsg var_name="del_ippool_success"}
    	IP Deleted From Ras Successfully.
{/headerMsg}

{if $is_editing or $attr_editing}
    <form method=POST action="/IBSng/admin/ras/ras_info.php">
{/if}
    {if $is_editing}
	<input type=hidden name=edit value=1>
        <input type=hidden name=old_ras_ip value="{$info.ras_ip}">
	<input type=hidden name=ras_id value="{$info.ras_id}">

	{addEditTable title="Edit RAS Information" double="TRUE"}

	    {addEditTD type="left1" double="TRUE" err="ras_ip_err"}
		RAS IP
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
		<input class="text" type=text name=ras_ip value="{$info.ras_ip}">
	    {/addEditTD}
	    {addEditTD type="left2" double="TRUE" err="ras_desc_err"}
	    	RAS Description
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
		<input class="text" type=text name=ras_description value="{$info.ras_description}">
	    {/addEditTD}
	    {addEditTD type="left1" double="TRUE" err="ras_type_err"}
		Type
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
	        <select name=ras_type>
		    {html_options output=$ras_types values=$ras_types selected=`$info.ras_type`}
		</select>
	    {/addEditTD}
	    {addEditTD type="left2" double="TRUE"} 
	        Radius Secret
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
	    	    <input class="text" type=text name=radius_secret value="{$info.radius_secret}">
    	    {/addEditTD}

	    {addEditTD type="left" double="TRUE" comment="TRUE"} 
		Comment
	    {/addEditTD}
	    {addEditTD type="right" double="TRUE" comment="TRUE"}
		<textarea name=comment class=text>{$info.comment}</textarea>
	    {/addEditTD}

        {/addEditTable}
    {else}
	{viewTable title="RAS Information" double="TRUE"}

	    {addEditTD type="left1" double="TRUE"}
		RAS IP
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
		    {$info.ras_ip}
	    {/addEditTD}
	    {addEditTD type="left2" double="TRUE"}
	    	RAS Description
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
		{$info.ras_description}
	    {/addEditTD}
	    {addEditTD type="left1" double="TRUE"}
		Type
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
	        {$info.ras_type}
	    {/addEditTD}
	    {addEditTD type="left2" double="TRUE"} 
	        Radius Secret:
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
	    	    {$info.radius_secret}
	    {/addEditTD}
	    
	    {addEditTD type="left" double="TRUE" comment="TRUE"} 
		Comment
	    {/addEditTD}
	    {addEditTD type="right" double="TRUE" comment="TRUE"}
	        {$info.comment}
	    {/addEditTD}

        {/viewTable}
    {/if}	
    {if $attr_editing}
        <input type=hidden name=attr_editing_done value=1>
	<input type=hidden name=ras_ip value="{$info.ras_ip}">
	{addEditTable title="Attributes" table_width="480"}
		{foreach from=$attrs item=attr_tuple}
		    	{addEditTD type="left"}
			    {$attr_tuple[0]}
			{/addEditTD}
		        {addEditTD type="right"}
			    <input class="large_text" type=text name="attr__{$attr_tuple[0]}" value="{$attr_tuple[1]}">
			{/addEditTD}    
		{/foreach}
	{/addEditTable}
    {else}		    
	{viewTable title="Attributes" table_width="480"}
		{foreach from=$attrs item=attr_tuple}
		    	{addEditTD type="left"}
			    {$attr_tuple[0]}
			{/addEditTD}
		        {addEditTD type="right"}
			    {$attr_tuple[1]}
			{/addEditTD}    
		{/foreach}
	{/viewTable}
    {/if}

<table width=100% border=0>
    <tr valign=top> 
	<td  valign="top" align="right">
    {listTable title="RAS IPPools" cols_num=1}
	{if not $is_editing and not $attr_editing and $can_change}
	    {listTableHeaderIcon action="delete" close_tr=TRUE}
	{/if}
	{listTR type="header"}
	    {listTD}
		 IPPool Name
	    {/listTD}
	{/listTR}
    {foreach from=$ras_ippools item=ras_ippool_name}
	{listTR type="body"}
		{listTD}
		    {$ras_ippool_name}
	    	{/listTD}
		{if not $is_editing and not $attr_editing and $can_change}
		    {listTD icon=TRUE}
			<a href="/IBSng/admin/ras/ras_info.php?ras_ip={$info.ras_ip|escape:"url"}&del_ip_pool={$ras_ippool_name|escape:"url"}" {jsconfirm msg="Are you sure you want to delete IPPool `$ras_ippool_name`"}>{listTableBodyIcon action="delete" cycle_color="TRUE"}</a>
		    {/listTD}
		{/if}
	{/listTR}
	{/foreach}
	{/listTable}

{if not $is_editing and not $attr_editing and $can_change}
    <form method=POST action="/IBSng/admin/ras/ras_info.php">
	{addEditTable title="Add IPPool" table_width="220" action_icon="add"}
	    {addEditTD type="left" err="edit_port_err"}
	        Add IPpool To Ras
	    {/addEditTD}
	    {addEditTD type="right"}
		<select name="add_ip_pool">
				{html_options values=$ippool_names output=$ippool_names}
			    </select>
	    {/addEditTD}
        <input type=hidden name=ras_ip value="{$info.ras_ip}">
    {/addEditTable}
	</form>
    <form method=POST action="/IBSng/admin/ras/ras_info.php" name=del_port>
	<input type=hidden name=ras_ip value="{$info.ras_ip}">
	{addEditTable title="Delete Port(s)" table_width="220" action_icon="delete"}
	    {addEditTD type="left" err="del_port_err"}
	        Ports(s)
	    {/addEditTD}
	    {addEditTD type="right"}
		<input class="text" type=text name=del_port> {multistr form_name="del_port" input_name="del_port"}		
    	    {/addEditTD}
	    <input type=hidden name=ras_ip value="{$info.ras_ip}">
    {/addEditTable}
    </form>
    <form method=POST action="/IBSng/admin/ras/edit_port.php" name=edit_port>
	<input type=hidden name=ras_ip value="{$info.ras_ip}">
	{addEditTable title="Edit Port(s)" table_width="220" action_icon="edit"}
	    {addEditTD type="left" err="edit_port_err"}
	        Ports(s)
	    {/addEditTD}
	    {addEditTD type="right"}
		<input class="text" type=text name=port_name> {multistr form_name="edit_port" input_name="port_name"}		
    	    {/addEditTD}
	    <input type=hidden name=ras_ip value="{$info.ras_ip}">
        {/addEditTable}
    </form>
{/if}
<td width="4%"></td>
<td align="left" valign="top">
    
    {listTable title="RAS Ports List" cols_num=4}
	{if not $is_editing and not $attr_editing and $can_change}
		{listTableHeaderIcon action="view"}
	        {listTableHeaderIcon action="delete" close_tr=TRUE}
	{/if}
	{listTR type="header"}
	    {listTD}
		Port Name
	    {/listTD}
	    {listTD}
		Type
	    {/listTD}
	    {listTD}
		Phone
	    {/listTD}
	    {listTD}
		Comment
	    {/listTD}
	{/listTR}
		{foreach from=$ports item=port_info}
		{listTR type="body"}
			{listTD}
			    {$port_info.port_name}
			{/listTD}
		        {listTD}
			    {$port_info.type}
			{/listTD}
		        {listTD}
			    {$port_info.phone}
			{/listTD}
			{listTD}
			    {$port_info.comment}
			{/listTD}
    			{if not $is_editing and not $attr_editing and $can_change}
			    {listTD icon=TRUE}
				<a href="/IBSng/admin/ras/edit_port.php?ras_ip={$info.ras_ip|escape:"url"}&port_name={$port_info.port_name|escape:"url"}">
				    {listTableBodyIcon action="view" cycle_color="TRUE"}
				</a>
			    {/listTD}
			    {listTD icon=TRUE}
				<a href="/IBSng/admin/ras/ras_info.php?ras_ip={$info.ras_ip|escape:"url"}&del_port={$port_info.port_name|escape:"url"}" {jsconfirm msg="Are you sure you want to delete port `$port_info.port_name`"}>
				    {listTableBodyIcon action="delete"}
				</a>
			    {/listTD}
			{/if}
		{/listTR}
		{/foreach}
        {/listTable}
	    
</table>
{if $is_editing or $attr_editing}
    </form>
{addRelatedLink}
    <a href="/IBSng/admin/ras/ras_info.php?ras_ip={$info.ras_ip}" class="RightSide_links">
	RAS <b>{$info.ras_ip}</b> Info
    </a>
{/addRelatedLink}
{/if}
{if !$is_editing}
{addRelatedLink}
    <a href="/IBSng/admin/ras/ras_info.php?ras_ip={$info.ras_ip}&edit=1" class="RightSide_links">
	Edit RAS Information
    </a>
{/addRelatedLink}
{/if}
{if !$attr_editing}
{addRelatedLink}
    <a href="/IBSng/admin/ras/ras_info.php?ras_ip={$info.ras_ip}&edit_attrs=1" class="RightSide_links">
	Edit RAS Attributes
    </a>
{/addRelatedLink}
{/if}

{addRelatedLink}
    <a href="/IBSng/admin/ras/ras_info.php?ras_ip={$info.ras_ip}&reset_attrs=1" {jsconfirm msg="Reset attributes of ras `$info.ras_ip` to default?"} class="RightSide_links">
	Reset Ras Attributes 
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/ras/add_port.php?ras_ip={$info.ras_ip}" class="RightSide_links">
	Add Port to RAS
    </a>
{/addRelatedLink}
{addRelatedLink}
    <a href="/IBSng/admin/ras/ras_list.php" class="RightSide_links">
	RAS List
    </a>
{/addRelatedLink}
{addRelatedLink}
    <a href="/IBSng/admin/ras/add_new_ras.php" class="RightSide_links">
	Add New RAS
    </a>
{/addRelatedLink}

{setAboutPage title="RAS Information"}

{/setAboutPage}

{include file="admin_footer.tpl"}
