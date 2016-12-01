{* Add/Edit Static IP
    
    action: either of edit or add
    action_icon: icon of form
    action_title: action string used in titles
    
    static_ip_id(edit only): id of static ip
    
    ip_addr: ip address w/wo netmask
    tx_leaf_name: leaf name of send
    rx_leaf_name: leaf name of receive
    
    Success: client will be redirected to the Static IP list page
    Failure: this page is shown again with error message at top of the page
*}
{include file="admin_header.tpl" title="`$action_title` Bw StaticIP" selected="Bandwidth"}
{include file="err_head.tpl"}

<form method=POST action="add_static_ip.php">
<input type=hidden name={$action} value=1>

    {addEditTable title="`$action_title` Bw StaicIP" action_icon=$action_icon}
    {if $action == "edit"}
	    <input type=hidden name=static_ip_id value={$static_ip_id}>
	    <input type=hidden name=old_ip_addr value={$ip}>
	    {addEditTD type="left" err="static_ip_id_err"}
		StaticIP ID 
	    {/addEditTD}

	    {addEditTD type="right"}
		{$static_ip_id}
	    {/addEditTD}
    {/if}

	{addEditTD type="left" err="ip_err"}
	    IP Address(/netmask)
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=ip_addr value="{ifisinrequest name="ip_addr" default_var="ip"}" class="text">
	    {helpicon subject='static ip address' category='bandwidth'}
	{/addEditTD}

	{addEditTD type="left" err="leaf_name_err"}
	    Send Leaf Name
	{/addEditTD}

	{addEditTD type="right"}
	    {html_options name="tx_leaf_name" output=$leaf_names values=$leaf_names selected=$tx_leaf_selected}
	    {helpicon subject='send leaf name' category='bandwidth'}
	{/addEditTD}

	{addEditTD type="left" err="leaf_name_err"}
	    Receive Leaf Name
	{/addEditTD}

	{addEditTD type="right"}
	    {html_options name="rx_leaf_name" output=$leaf_names values=$leaf_names selected=$rx_leaf_selected}
	    {helpicon subject='receive leaf name' category='bandwidth'}
	{/addEditTD}
	
    {/addEditTable}
</form>
{addRelatedLink}
    <a href="/IBSng/admin/bw/static_ip_list.php" class="RightSide_links">
	StaticIP list
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
