{* Add New Port
    ras_ip: new ras ip (invisible)
    port name: string representation of port
    phone: phone number
    type: port type
    comment: 
    
    Success: client will be redirected to the ras information page
    Failure: this page is shown again with error message at top of the page

*}
{include file="admin_header.tpl" title="Add Port To Ras" selected="RAS"}
{include file="err_head.tpl"}

<form method=POST name=add_port>
    {addEditTable title="Add New Port to Ras" table_width=320 action_icon="add"}

	{addEditTD type="left" err="ras_ip_err"}
	    Ras IP:
	{/addEditTD}
	{addEditTD type="right"}
	    {$ras_ip}    
	{/addEditTD}

	{addEditTD type="left" err="name_err"}
	    Port Name
	{/addEditTD}
	{addEditTD type="right"}
	    	<input class="text" type=text name=port_name value="{$port_name}">
		{helpicon subject="port name" category="ras"}
		{multistr form_name="add_port" input_name="port_name"}
    	{/addEditTD}

	{addEditTD type="left" err="port_type_err"}
	    Port Type
	{/addEditTD}
	{addEditTD type="right"}
		<select name=port_type>
		    {html_options output=$port_types values=$port_types default=$port_type}
		</select>
	    	{helpicon subject="port type" category="ras"}
    	{/addEditTD}

	{addEditTD type="left" err="port_type_err"}
	    Phone No. 
	{/addEditTD}
	{addEditTD type="right"}
		<input type=text name=phone value="{$phone}" class=text>
	    	{helpicon subject="phone" category="ras"}
		{multistr form_name="add_port" input_name="phone"}
    	{/addEditTD}

	{addEditTD type="left" err="ippool_comment_err" comment=TRUE}
	    Comment
	{/addEditTD}
	{addEditTD type="right" comment=TRUE}
	    <textarea name=comment class=text>{$comment|strip}</textarea>
	{/addEditTD}

    {/addEditTable}
</form>

{addRelatedLink}
    <a href="/IBSng/admin/ras/ras_info.php?ras_ip={$ras_ip}" class="RightSide_links">
	RAS <b>{$ras_ip}</b> Info
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

{setAboutPage title="Add New Port"}

{/setAboutPage}
{include file="admin_footer.tpl"}
