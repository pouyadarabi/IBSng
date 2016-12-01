{* Add/Edit Leaf Service
    leaf_name: name of leaf that we add service
    interface_name: interface_name we're adding leaf service to
    
    Success: client will be redirected to the interface information page
    Failure: this page is shown again with error message at top of the page
*}
{include file="admin_header.tpl" title="`$action_title` Leaf Service" selected="Bandwidth"}
{include file="err_head.tpl"}

<form method=POST action="add_leaf_service.php" name="leaf_service">
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

	{addEditTD type="left" err="leaf_name_err"}
	    Leaf Name
	{/addEditTD}

	{addEditTD type="right"}
	    {$leaf_name}
    	    <input type=hidden name=leaf_name value="{$leaf_name}">
	    {helpicon subject='Leaf Name' category='bandwidth'}
	{/addEditTD}

	{if $action=="edit"}
	    {addEditTD type="left" err="leaf_name_err"}
		Leaf Service ID
	    {/addEditTD}

    	    {addEditTD type="right"}
		{$leaf_service_id}
		<input type=hidden name=leaf_service_id value="{$leaf_service_id}">
    	    {/addEditTD}
	{/if}
	{addEditTD type="left" err="protocol_err"}
	    Protocol
	{/addEditTD}

	{addEditTD type="right"}
    	    {html_options name="protocol" values=$protocols output=$protocols selected=$protocol_selected}
	    {helpicon subject='protocol' category='bandwidth'}
	{/addEditTD}

	{addEditTD type="left" err="filter_err"}
	    Filter Type 
	{/addEditTD}

	{addEditTD type="right"}
    	    {html_options name="filter_type" options=$filter_types selected=$filter_type_selected}
	    {helpicon subject='filter type' category='bandwidth'}
	{/addEditTD}

	{addEditTD type="left" err="filter_err"}
	    Filter Value
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=filter_value value="{ifisinrequest name="filter_value" default_var="filter_value"}" class=text>
	    {multistr form_name="leaf_service" input_name="filter_value" left_pad="FALSE"}
	    {helpicon subject='filter value' category='bandwidth'}
	{/addEditTD}
	
	{addEditTD type="left" err="limit_kbits_err"}
	    Bandwidth Rate
	{/addEditTD}

	{addEditTD type="right"}
    	    <input type=text name=rate_kbits value="{ifisinrequest name="rate_kbits" default_var="rate_kbits"}" class=text> kbits
	    {helpicon subject='rate kbits' category='bandwidth'}
	{/addEditTD}

	{addEditTD type="left" err="limit_kbits_err"}
	    Bandwidth Ceil
	{/addEditTD}

	{addEditTD type="right"}
    	    <input type=text name=ceil_kbits value="{ifisinrequest name="ceil_kbits" default_var="ceil_kbits"}" class=text> kbits
	    {helpicon subject='ceil kbits' category='bandwidth'}
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


{if $action=="add"}
    {setAboutPage title="Add Leaf Service"}

    {/setAboutPage}
{else}
    {setAboutPage title="Edit Leaf Service"}

    {/setAboutPage}
{/if}

{include file="admin_footer.tpl"}
