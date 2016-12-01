{* Tariff info
    $tariff_id
    $tariff_name
    $comment
    $prefixes
*}
{include file="admin_header.tpl" title="Tariff `$tariff_name` Informations" selected="VoIP Tariff"}
{include file="err_head.tpl"}

{headerMsg var_name="delete_prefix_success"}Prefixes Deleted Successfully.{/headerMsg}
{viewTable title="VoIP Tariff `$tariff_name` Informations"}
    
    {addEditTD type="left"}
	Tariff ID
    {/addEditTD}

    {addEditTD type="right"}
	{$tariff_id}
    {/addEditTD}

    {addEditTD type="left"}
	Tariff Name
    {/addEditTD}

    {addEditTD type="right"}
	{$tariff_name}
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	Comment
    {/addEditTD}

    {addEditTD type="right" comment=TRUE}
	{$comment}
    {/addEditTD}
{/viewTable}

{listTable title="Show Prefixes" cols_num=1}
{listTD}

{foreach from=$start_withs item=name_regex}
    <a href="tariff_info.php?tariff_name={$tariff_name}&name_regex={$name_regex[1]}" class="link_in_body" style=" font-size: 9pt; color:black">
	{$name_regex[0]}
    </a>&nbsp;
{/foreach}

{/listTD}
{/listTable}

{if isset($prefixes)}

<form method=POST action="tariff_info.php" name="prefix_select">
<input type=hidden name=tariff_name value="{$tariff_name}">
<input type=hidden name=del_prefix_checkbox value=1>

<script language="javascript" src="/IBSng/js/check_box_container.js"></script>
<script language="javascript">
    var rows_select=new CheckBoxContainer();
</script>


{listTable title="Prefix List" cols_num=10}
    {if $can_change}
        {listTableHeaderIcon action="edit"}
        {listTableHeaderIcon action="delete" close_tr=TRUE}
    {/if}    
    {listTR type="header"}
	{listTD}
	<input type=checkbox name="check_all">
	<script language="javascript">
	    rows_select.setCheckAll("prefix_select","check_all");
	</script>
	{/listTD}
	
	{listTD}
	    Row
	{/listTD}

	{listTD}
	    Prefix ID
        {/listTD}

	{listTD}
	    Prefix Name
        {/listTD}
		
        {listTD}
	    Prefix Code
        {/listTD}

        {listTD}
	    CPM
        {/listTD}

        {listTD}
	    Free Seconds
        {/listTD}

        {listTD}
	    Min Duration
        {/listTD}

        {listTD}
	    Round To
        {/listTD}

        {listTD}
	    Min Chargable Duration
        {/listTD}
    {/listTR}
    {foreach from=$prefixes item=prefix}
        {listTR type="body"}
	    {listTD}
		{counter name="row" assign="row_no" print=false}
		<input type=checkbox name="del_prefix_{$row_no}" value="{$prefix.prefix_code}">
		<script language="javascript">
			rows_select.addByName("prefix_select","del_prefix_{$row_no}");
		</script>
		
	    {/listTD}
	
    	    {listTD}    
		{$row_no}
	    {/listTD}

	    {listTD}
		{$prefix.prefix_id}
	    {/listTD}

	    {listTD}
		{$prefix.prefix_name}
	    {/listTD}

	    {listTD}
		{$prefix.prefix_code}
	    {/listTD}

	    {listTD}
		{$prefix.cpm|price}
	    {/listTD}

	    {listTD}
		{$prefix.free_seconds}
	    {/listTD}

	    {listTD}
		{$prefix.min_duration}
	    {/listTD}

	    {listTD}
		{$prefix.round_to}
	    {/listTD}

	    {listTD}
		{$prefix.min_chargable_duration}
	    {/listTD}

	    {if $can_change}
	        {listTD icon="TRUE"}
	        	<a href="add_edit_prefix.php?edit=1&prefix_id={$prefix.prefix_id|escape:"url"}&tariff_name={$tariff_name|escape:"url"}&prefix_name={$prefix.prefix_name|escape:"url"}">
			    {listTableBodyIcon action="edit" cycle_color=TRUE}
			</a>
	        {/listTD}

	        {listTD icon="TRUE"}
		        <a href="tariff_info.php?del_prefix={$prefix.prefix_code|escape:"url"}&tariff_name={$tariff_name|escape:"url"}" {jsconfirm msg="Are you sure you want to delete prefix `$prefix.prefix_code`?"}>
			    {listTableBodyIcon action="delete"}
			</a>
	        {/listTD}
	    {/if}    
	{/listTR}
    {/foreach}
{/listTable}
{if $can_change}
    <input type=image src="/IBSng/images/icon/delete.gif" {jsconfirm}>
    <input type=hidden name="delete" value="delete">
{/if}
</form>

{/if} {* end isset($prefixes) *}
<p>
<form action="tariff_info.php">
<input type=hidden name="tariff_name" value="{$tariff_name}">
{addEditTable title="Download Prefixes As CSV"}
    {addEditTD type="left"}
	Separator
    {/addEditTD}
    {addEditTD type="right"}
	{separatorSelect name="csv" default_request="csv"}
    {/addEditTD}
{/addEditTable}
</form>


{if $can_change}
    {addRelatedLink}
	<a href="/IBSng/admin/charge/voip_tariff/add_edit_tariff.php?edit=1&tariff_name={$tariff_name|escape:"url"}" class="RightSide_links">
	    Edit Tariff <b>{$tariff_name}</b>
	</a>
    {/addRelatedLink}

    {addRelatedLink}
	<a href="/IBSng/admin/charge/voip_tariff/tariff_info.php?tariff_name={$tariff_name|escape:"url"}&del_tariff=1" class="RightSide_links" {jsconfirm}>
	    Delete Tariff <b>{$tariff_name}</b>
	</a>
    {/addRelatedLink}

    {addRelatedLink}
	<a href="/IBSng/admin/charge/voip_tariff/add_edit_prefix.php?tariff_name={$tariff_name|escape:"url"}&add=1" class="RightSide_links">
	    Add Prefix(es)
	</a>
    {/addRelatedLink}

    {addRelatedLink}
	<a href="/IBSng/admin/charge/voip_tariff/add_edit_tariff.php" class="RightSide_links">
	    Add New Tariff
	</a>
    {/addRelatedLink}
{/if}

{addRelatedLink}
    <a href="/IBSng/admin/charge/voip_tariff/tariff_list.php" class="RightSide_links">
	Tariff list
    </a>
{/addRelatedLink}

{setAboutPage title="Tariff Info"}

{/setAboutPage}

{include file="admin_footer.tpl"}