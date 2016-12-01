{* 
    Charge List
    $charge_infos: array of associative arrays containing charge infos
*}

{include file="admin_header.tpl" title="Charge List" selected="Charge"}
{include file="err_head.tpl"}

{listTable title="Charge List" cols_num=5}
	{listTableHeaderIcon action="view" close_tr=TRUE}
	{listTR type="header"}
	    {listTD}
		Row
	    {/listTD}
	    {listTD}
		Charge Name
	    {/listTD}
	    {listTD}
		Charge Type
	    {/listTD}
	    {listTD}
		Creator
	    {/listTD}
	    {listTD}
		Visible To All
	    {/listTD}
	{/listTR}

		
	{foreach from=$charge_infos key=charge_name item=charge_info}
	    {listTR type="body"}
		{listTD}
		    {counter}
		{/listTD}
		{listTD}
		    {$charge_name}
		{/listTD}
		{listTD}
		    {$charge_info.charge_type}
    		{/listTD}
		{listTD}
		    {$charge_info.creator}
    		{/listTD}
		{listTD}
		    {$charge_info.visible_to_all}
    		{/listTD}
		{listTD icon=TRUE}
		    <a href="/IBSng/admin/charge/charge_info.php?charge_name={$charge_name|escape:"url"}">{listTableBodyIcon action="view" cycle_color="TRUE"}</a>
    		{/listTD}
		
	    {/listTR}
	{/foreach}
{/listTable}
{addRelatedLink}
    <a href="/IBSng/admin/charge/add_new_charge.php" class="RightSide_links">
	Add New Charge
    </a>
{/addRelatedLink}

{setAboutPage title="Charge List"}

{/setAboutPage}

{include file="admin_footer.tpl"}