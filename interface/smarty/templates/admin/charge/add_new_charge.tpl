{* Add New Charge
    charge_name: new ras ip
    charge_type: type of new charge
    comment: 
    visible_to_all: Visible to all flag for charge
    
    Success: client will be redirected to the new charge information page
    Failure: this page is shown again with error message at top of the page

*}
{include file="admin_header.tpl" title="Add New Charge" selected="Charge"} 
{include file="err_head.tpl"}

<form method=POST>
    {addEditTable title="Add New Charge"}

	{addEditTD type="left" err="charge_name_err"}
	    Charge Name
	{/addEditTD}
	{addEditTD type="right"}
	    <input class="text" type=text name=charge_name value="{$charge_name}">
	    {helpicon subject="charge name" category="charge"}
	{/addEditTD}
	
	{addEditTD type="left" err="charge_type_err"}
	    Charge Type
	{/addEditTD}
	{addEditTD type="right"}
	    <select name=charge_type>
		{html_options output=$charge_types values=$charge_types selected=$charge_type}
	    </select>
	    {helpicon subject="charge type" category="charge"}
	{/addEditTD}
	
	{addEditTD type="left" err="visible_to_all_err"}
	    Visible To All
	{/addEditTD}
	{addEditTD type="right"}
	    <input class="checkbox" type=checkbox name=visible_to_all {$visible_to_all}>{helpicon subject="visible to all" category="charge"}
	{/addEditTD}
	
	{addEditTD type="left" err="comment_err" comment=TRUE}
	    Comment
	{/addEditTD}
	{addEditTD type="right" comment=TRUE}
	    <textarea name=comment class=text>{$comment|strip}</textarea>
	{/addEditTD}
	
    {/addEditTable}
</form>
{addRelatedLink}
    <a href="/IBSng/admin/charge/charge_list.php" class="RightSide_links">
	 Charge List
    </a>
{/addRelatedLink}
{setAboutPage title="Add New Charge"}

{/setAboutPage}

{include file="admin_footer.tpl"}
