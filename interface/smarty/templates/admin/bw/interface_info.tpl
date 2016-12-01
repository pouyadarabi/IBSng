{* Interface Info
    $tree: html code of tree
*}
{include file="admin_header.tpl" title="Interface `$interface_name` Info" selected="Bandwidth"}
{include file="err_head.tpl"}
{headerMsg var_name="delete_leaf_service_success"}Leaf Service Deleted Successfully.{/headerMsg}
{headerMsg var_name="delete_node_success"}Node Deleted Successfully.{/headerMsg}
{headerMsg var_name="delete_leaf_success"}Leaf Deleted Successfully.{/headerMsg}
{viewTable title="Interface `$interface_name` Info"}
    {addEditTD type="left"}
	Interface ID
    {/addEditTD}

    {addEditTD type="right"}
	{$interface_id}
    {/addEditTD}

    {addEditTD type="left"}
	Interface Name
    {/addEditTD}

    {addEditTD type="right"}
	{$interface_name}
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	Comment
    {/addEditTD}

    {addEditTD type="right" comment=TRUE}
	{$comment}
    {/addEditTD}
{/viewTable}

<b><FONT color="990000" face="tahoma" style="font-size:8pt">
R: Rate&nbsp;&nbsp;&nbsp;
C: Ceil 
</font></b>
<br><br>
{$tree}

{if isset($show_layer_link)}
<script language="javascript">
    link='{$show_layer_link}';
    {literal}
	    window.onload=function(){document.getElementById(link).onclick();};
    {/literal}
</script>
{/if}


{addRelatedLink}
    <a href="/IBSng/admin/bw/add_interface.php?edit=1&interface_name={$interface_name}" class="RightSide_links">
	Edit Interface <b>{$interface_name}</b>
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/bw/interface_info.php?delete_interface=1&interface_name={$interface_name}" class="RightSide_links" {jsconfirm}>
	Delete Interface <b>{$interface_name}</b>
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/bw/interface_list.php" class="RightSide_links">
	Interface list
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/bw/static_ip_list.php" class="RightSide_links">
	StaticIP list
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/bw/active_leaves.php" class="RightSide_links">
	Active Leaves list
    </a>
{/addRelatedLink}

{setAboutPage title="Interface Info"}

{/setAboutPage}

{include file="admin_footer.tpl"}
