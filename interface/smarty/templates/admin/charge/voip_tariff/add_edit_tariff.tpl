{* Add/Edit Tariff
    tarif_name: new/edit tariff name
    comment: comment!
    
    Success: client will be redirected to the tariff information page
    Failure: this page is shown again with error message at top of the page

*}
{include file="admin_header.tpl" title="`$action_title` Tariff" selected="VoIP Tariff"}
{include file="err_head.tpl"}

<form method=POST action="add_edit_tariff.php">
<input type=hidden name={$action} value=1>
    {addEditTable title="`$action_title` Tariff" action_icon="`$action_icon`"}

    {if $action == "edit"}
	<input type=hidden name=old_tariff_name value="{$tariff_name}">
	<input type=hidden name=tariff_id value={$tariff_id}>
	    {addEditTD type="left" err="tariff_id_err"}
		Tariff ID 
	    {/addEditTD}

	    {addEditTD type="right"}
		{$tariff_id}
	    {/addEditTD}
    {/if}

	{addEditTD type="left" err="tariff_name_err"}
	    Tariff Name
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=tariff_name value="{ifisinrequest name="tariff_name" default_var="tariff_name"}" class="text">
	    {helpicon subject='tariff name' category='voip tariff'}
	{/addEditTD}
	
	{addEditTD type="left" err="comment_err" comment=TRUE}
	    Comment
	{/addEditTD}
	{addEditTD type="right" comment=TRUE}
	    <textarea name=comment class=text>{ifisinrequest name="comment" default_var="comment"}</textarea>
	{/addEditTD}
	
    {/addEditTable}
</form>
{addRelatedLink}
    <a href="/IBSng/admin/charge/voip_tariff/tariff_list.php" class="RightSide_links">
	Tariff list
    </a>
{/addRelatedLink}

{if $action == "edit" }
    {addRelatedLink}
	<a href="/IBSng/admin/charge/voip_tariff/tariff_info.php?tariff_name={$tariff_name|escape:"url"}" class="RightSide_links">
	    Tariff </b>{$tariff_name}</b> Info
        </a>
    {/addRelatedLink}
{/if}

{if $action == "add"}
    {setAboutPage title="Add Tariff"}

    {/setAboutPage}
{else}
    {setAboutPage title="Edit Tariff"}

    {/setAboutPage}
{/if}

{include file="admin_footer.tpl"}
