{* Add/Edit Prefix
    tarif_name: tariff name
    prefix_id: edit only
    prefix_name
    prefix_code
    cpm
    round_to
    min_duration
    free_seconds
    
    
    Success: client will be redirected to the tariff information page
    Failure: this page is shown again with error message at top of the page

*}
{include file="admin_header.tpl" title="`$action_title` Prefix" selected="VoIP Tariff"}
{include file="err_head.tpl"}

<form method=POST action="add_edit_prefix.php">
<input type=hidden name={$action} value=1>
<input type=hidden name=tariff_name value="{$tariff_name}">
{addEditTable title="`$action_title` Prefix" action_icon="`$action_icon`"}
    {addEditTD type="left" err="tariff_name_err"}
	Tariff Name
    {/addEditTD}

    {addEditTD type="right"}
	{$tariff_name}
	{helpicon subject='tariff name' category='voip tariff'}
    {/addEditTD}

    {if $action == "edit"}
	<input type=hidden name=prefix_id value={$prefix_id}>
	<input type=hidden name=old_prefix_name value='{$prefix_name}'>
	    {addEditTD type="left" err="prefix_id_err"}
		Prefix ID
	    {/addEditTD}

	    {addEditTD type="right"}
		{$prefix_id}
	    {/addEditTD}
    {/if}

	{addEditTD type="left" err="prefix_name_err"}
	    Prefix Name
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=prefix_name value="{ifisinrequest name="prefix_name" default_var="prefix_name"}" class="text">
	    {helpicon subject='prefix name' category='voip tariff'}
	{/addEditTD}

	{addEditTD type="left" err="prefix_code_err"}
	    Prefix Code
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=prefix_code value="{ifisinrequest name="prefix_code" default_var="prefix_code"}" class="text">
	    {helpicon subject='prefix code' category='voip tariff'}
	{/addEditTD}

	{addEditTD type="left" err="cpm_err"}
	    CPM
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=cpm value="{ifisinrequest name="cpm" default_var="cpm"}" class="text"> {$MONEY_UNIT}
	    {helpicon subject='cpm' category='voip tariff'}
	{/addEditTD}

	{addEditTD type="left" err="free_secs_err"}
	    Free Seconds
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=free_seconds value="{ifisinrequest name="free_seconds" default_var="free_seconds" default="0"}" class="text">
	    {helpicon subject='Free Seconds' category='voip tariff'}
	{/addEditTD}

	{addEditTD type="left" err="min_duration_err"}
	    Minimum Duration
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=min_duration value="{ifisinrequest name="min_duration" default_var="min_duration" default="0"}" class="text"> Seconds
	    {helpicon subject='minimum duration' category='voip tariff'}
	{/addEditTD}

	{addEditTD type="left" err="round_to_err"}
	    Round To
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=round_to value="{ifisinrequest name="round_to" default_var="round_to" default="0"}" class="text"> Seconds
	    {helpicon subject='round to' category='voip tariff'}
	{/addEditTD}

	{addEditTD type="left" err="min_chargable_duration_err"}
	    Minimum Chargable Duration
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=min_chargable_duration value="{ifisinrequest name="min_chargable_duration" default_var="min_chargable_duration" default="0"}" class="text"> Seconds
	    {helpicon subject='min_chargable_duration' category='voip tariff'}
	{/addEditTD}
	
    {/addEditTable}
</form>

{if $action == "add"}
    <form method="POST" action="add_edit_prefix.php" enctype="multipart/form-data">
    <input type=hidden name={$action} value=1>
    <input type=hidden name=tariff_name value="{$tariff_name}">
    <font size=3>
	File Format: prefix name,prefix code,cpm,free seconds,min duration,round to,min chargable duration
    </font>
    {addEditTable title="Upload Prefixes as CSV" table_width=400}
	{addEditTD type="left"}
	    File
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=file name="prefixes_file" class=text>
	{/addEditTD}

	{addEditTD type="left"}
	    Separator
	{/addEditTD}
	{addEditTD type="right"}
	    {separatorSelect name="csv" default_request="csv"}
	{/addEditTD}
    {/addEditTable}

    </form>
{/if}

{addRelatedLink}
    <a href="/IBSng/admin/charge/voip_tariff/tariff_info.php?tariff_name={$tariff_name|escape:"url"}" class="RightSide_links">
        Tariff <b>{$tariff_name}</b> Info
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/charge/voip_tariff/tariff_list.php" class="RightSide_links">
	Tariff list
    </a>
{/addRelatedLink}

{if $action == "add"}
    {setAboutPage title="Add Prefix"}

    {/setAboutPage}
{else}
    {setAboutPage title="Edit Prefix"}

    {/setAboutPage}
{/if}

{include file="admin_footer.tpl"}
