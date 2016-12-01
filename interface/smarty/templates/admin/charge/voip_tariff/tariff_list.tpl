{* Tariffs  List
   $tariffs: array of associative arrays containing tariffs infos

*}

{include file="admin_header.tpl" title="Tariff List" selected="VoIP Tariff"}
{include file="err_head.tpl"}

{listTable title="Tariff List" cols_num=4}
	{listTableHeaderIcon action="view" close_tr=TRUE}
	{listTR type="header"}
	    {listTD}
		Row
	    {/listTD}
	    {listTD}
		ID
	    {/listTD}
	    {listTD}
		Tariff Name
	    {/listTD}
	    {listTD}
		Comment
	    {/listTD}
	{/listTR}
		
	{foreach from=$tariffs item=tariff}
	    {listTR type="body" cycle_color=FALSE}
		{listTD}
		    {counter}
		{/listTD}
		{listTD}
		    {$tariff.tariff_id}
		{/listTD}
		{listTD}
		    {$tariff.tariff_name}
		{/listTD}
		{listTD}
		    {$tariff.comment}
		{/listTD}
		{listTD icon="TRUE"}
		    <a href="/IBSng/admin/charge/voip_tariff/tariff_info.php?tariff_name={$tariff.tariff_name|escape:"url"}">
			{listTableBodyIcon action="view" cycle_color=TRUE}
		    </a>
		{/listTD}
	    {/listTR}
	{/foreach}

{/listTable}

{addRelatedLink}
    <a href="/IBSng/admin/charge/voip_tariff/add_edit_tariff.php" class="RightSide_links">
	Add New Tariff
    </a>
{/addRelatedLink}

{setAboutPage title="Tariff List"}

{/setAboutPage}

{include file="admin_footer.tpl"}