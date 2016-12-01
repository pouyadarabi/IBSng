{* 

    Edit Ras Port
    ras_ip: new ras ip (invisible)
    port_name: string representation of port
    phone: phone number
    type: port type
    comment: 
    
    Success: client will be redirected to the ras information page
    Failure: this page is shown again with error message at top of the page

*}
{include file="admin_header.tpl" title="Edit Ras Port" selected="RAS"}
{include file="err_head.tpl"}
    
{headerMsg}
        Warning: If you edit multiple ports, default values are shown from first port, but updating will
	occure for all ports.<br>
{/headerMsg}

        <form method=POST name=edit_port action="/IBSng/admin/ras/edit_port.php">
	<input type=hidden name=ras_ip value="{$ras_ip}">

    {addEditTable title="Edit RAS Port" table_width=320}

	{addEditTD type="left" err="ras_ip_err"}
	    Ras IP
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
		{multistr form_name="edit_port" input_name="port_name"}
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
	    Phone No 
	{/addEditTD}
	{addEditTD type="right"}
		<input type=text name=phone value="{$phone}" class=text>
	    	{helpicon subject="phone" category="ras"}
		{multistr form_name="edit_port" input_name="phone"}
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
    <a href="/IBSng/admin/ras/ras_list.php" class="RightSide_links">
	RAS List
    </a>
{/addRelatedLink}

{setAboutPage title="Edit RAS Port"}

{/setAboutPage}

{include file="admin_footer.tpl"}
