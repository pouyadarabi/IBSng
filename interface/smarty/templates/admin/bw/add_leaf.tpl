{* Add/Edit Leaf
    leaf_name: name of leaf
    parent_id: id of parent onde
    total_rate_kbits: total rate limit of this leaf
    total_ceil_kbits: total ceil limit of this leaf
    default_rate_kbits: default rate limit of this leaf
    default_lceil_kbits: default ceil limit of this leaf

    interface_name: interface_name we're adding node to
    
    Success: client will be redirected to the interface information page
    Failure: this page is shown again with error message at top of the page
*}
{include file="admin_header.tpl" title="`$action_title` Leaf" selected="Bandwidth"}
{include file="err_head.tpl"}

<form method=POST action="add_leaf.php">
    <input type=hidden name="{$action}" value="1">
    {addEditTable title="`$action_title` Leaf" action_icon=`$action_icon`}

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

	{if $action == "edit"}
	    <input type=hidden name="old_leaf_name" value="{$leaf_name}">
	    {addEditTD type="left" err="leaf_id_err"}
		Leaf ID
	    {/addEditTD}

	    {addEditTD type="right"}
		<input type=hidden name=leaf_id value="{$leaf_id}">
		{$leaf_id}
	    {/addEditTD}
	{/if}

	{addEditTD type="left" err="leaf_name_err"}
	    Leaf Name
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=leaf_name value="{ifisinrequest name="leaf_name" default_var="leaf_name"}" class="text">
	    {helpicon subject='leaf name' category='bandwidth'}
	{/addEditTD}

	{addEditTD type="left" err="total_limit_kbits_err"}
	    Total Bandwidth Rate
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=total_rate_kbits value="{ifisinrequest name="total_rate_kbits" default_var="total_rate_kbits"}" class=text> kbit/s
	    {helpicon subject='total rate kbits' category='bandwidth'}
	{/addEditTD}

	{addEditTD type="left" err="total_limit_kbits_err"}
	    Total Bandwidth Ceil
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=total_ceil_kbits value="{ifisinrequest name="total_ceil_kbits" default_var="total_ceil_kbits"}" class=text> kbit/s
	    {helpicon subject='total ceil kbits' category='bandwidth'}
	{/addEditTD}


	{addEditTD type="left" err="default_kbits_err"}
	    Default Bandwidth Rate
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=default_rate_kbits value="{ifisinrequest name="default_rate_kbits" default_var="default_rate_kbits"}" class=text> kbit/s
	    {helpicon subject='default rate kbits' category='bandwidth'}
	{/addEditTD}

	{addEditTD type="left" err="default_kbits_err"}
	    Default Bandwidth Ceil
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=default_ceil_kbits value="{ifisinrequest name="default_ceil_kbits" default_var="default_ceil_kbits"}" class=text> kbit/s
	    {helpicon subject='default ceil kbits' category='bandwidth'}
	{/addEditTD}
	
    {/addEditTable}
</form>
{addRelatedLink}
    <a href="/IBSng/admin/bw/interface_info.php?interface_name_name={$interface_name}" class="RightSide_links">
	Interface <b>{$interface_name}</b> Info
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/bw/interface_list.php" class="RightSide_links">
	Interface list
    </a>
{/addRelatedLink}

{setAboutPage title="Add Leaf"}

{/setAboutPage}

{include file="admin_footer.tpl"}
