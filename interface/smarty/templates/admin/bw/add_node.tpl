{* Add/Edit Node
    limit_kbits: limit this node bandwidth
    
    interface_name: interface_name we're adding node to
    parent_id: id of parent onde
    
    Success: client will be redirected to the interface information page
    Failure: this page is shown again with error message at top of the page
*}
{include file="admin_header.tpl" title="`$action_title` Node" selected="Bandwidth"}
{include file="err_head.tpl"}

<form method=POST action="add_node.php">
<input type=hidden name={$action} value=1>

    {addEditTable title="`$action_title` Node" action_icon=$action_icon}
    {if $action == "edit"}
	    <input type=hidden name=node_id value={$node_id}>
	    {addEditTD type="left" err="node_id_err"}
		Node ID 
	    {/addEditTD}

	    {addEditTD type="right"}
		{$node_id}
	    {/addEditTD}
    {/if}

	{addEditTD type="left" err="interface_name_err"}
	    Interface
	{/addEditTD}

	{addEditTD type="right"}
	    {$interface_name}
	    <input type=hidden name=interface_name value="{$interface_name}">
	    {helpicon subject='interface name' category='bandwidth'}
	{/addEditTD}

	{addEditTD type="left" err="parent_id_err"}
	    Parent Node ID
	{/addEditTD}

	{addEditTD type="right"}
	    {$parent_id}
    	    <input type=hidden name=parent_id value="{$parent_id}">
	    {helpicon subject='Parent Node' category='bandwidth'}
	{/addEditTD}

	{addEditTD type="left" err="limit_kbits_err"}
	    Bandwidth Rate 
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=rate_kbits value="{ifisinrequest name="rate_kbits" default_var="rate_kbits"}" class="text"> kbit/s
	    {helpicon subject='node rate kbits' category='bandwidth'}
	{/addEditTD}

	{addEditTD type="left" err="limit_kbits_err"}
	    Bandwidth Ceil
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=ceil_kbits value="{ifisinrequest name="ceil_kbits" default_var="ceil_kbits"}" class="text"> kbit/s
	    {helpicon subject='node ceil kbits' category='bandwidth'}
	{/addEditTD}
	
    {/addEditTable}
</form>
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

{if $action == "add"}
    {setAboutPage title="Add Node"}

    {/setAboutPage}
{else}
    {setAboutPage title="Add Node"}

    {/setAboutPage}
{/if}

{include file="admin_footer.tpl"}
