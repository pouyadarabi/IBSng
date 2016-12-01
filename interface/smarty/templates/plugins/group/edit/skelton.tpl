{*



*}
{include file="admin_header.tpl" title="Edit Group Attributes" selected="Group List"}
{include file="err_head.tpl"}
{viewTable title="Group Information" nofoot="TRUE"}
    {addEditTD type="left"}
	Group ID
    {/addEditTD}

    {addEditTD type="right"}
	{$group_id}
    {/addEditTD}

    {addEditTD type="left"}
	Group Name
    {/addEditTD}

    {addEditTD type="right"}
	    {$group_name}
    {/addEditTD}
{/viewTable}
<br>
<form method=POST action="/IBSng/admin/plugins/edit.php" name="group_edit">

    <input type=hidden name="target" value="group">
    <input type=hidden name="target_id" value="{$group_name}">
    <input type=hidden name="update" value="1">
    <input type=hidden name="edit_tpl_cs" value="{$edit_tpl_cs}">

    {if isInRequest("tab1_selected")}
	<input type=hidden name="tab1_selected" value="{$smarty.request.tab1_selected}">
    {/if}

{foreach from=$edit_tpl_files item="tpl_file"}
    {include file=$tpl_file}    
{/foreach}

{attrTableFoot action_icon="ok" table_width="280" cancel_icon="TRUE"}
{/attrTableFoot}

</form>
{addRelatedLink}
    <a href="/IBSng/admin/group/group_info.php?group_name={$group_name|escape:"url"}" class="RightSide_links">
	Group Info
    </a>
{/addRelatedLink}


{addRelatedLink}
    <a href="/IBSng/admin/group/group_list.php" class="RightSide_links">
	Group List
    </a>
{/addRelatedLink}

{setAboutPage title="Group Info"}
    You can edit attributes of group that you have selected.
{/setAboutPage}

{include file="admin_footer.tpl"}