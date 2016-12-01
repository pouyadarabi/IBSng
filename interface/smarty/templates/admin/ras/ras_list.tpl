{* 
    Ras List
   $ras_infos: array of associative arrays containing active ras infos
   $inactive_ras_infos: array of associative arrays containing inactive ras infos

*}

{include file="admin_header.tpl" title="Ras List" selected="RAS"}
{include file="err_head.tpl"}

<center>
{headerMsg var_name="deactive_success"}Ras DeActivated Successfully.{/headerMsg}
{headerMsg var_name="reactive_success"}Ras ReActivated Successfully.{/headerMsg}

{listTable title="Active Rases" cols_num=6}
	{listTableHeaderIcon action="view"}
	{listTableHeaderIcon action="disable" close_tr=TRUE}
	{listTR type="header"}
	    {listTD}
		Row
	    {/listTD}
	    {listTD}
		ID
	    {/listTD}
	    {listTD}
		RAS IP
	    {/listTD}

	    {listTD}
		Description
	    {/listTD}

	    {listTD}
		Type
	    {/listTD}
	    {listTD}
		Radius Secret
	    {/listTD}
	{/listTR}
	{foreach from=$ras_infos item=ras_info}
	{listTR type="body"}
	    {listTD}
		    {counter name="enabled_row_no"}
	    {/listTD}
	    {listTD}
		    {$ras_info.ras_id}
	    {/listTD}
	    {listTD}
		    {$ras_info.ras_ip}
	    {/listTD}
	    {listTD}
		    {$ras_info.ras_description}
	    {/listTD}
	    {listTD}
	    	    {$ras_info.ras_type}
	    {/listTD}
	    {listTD}
		    {$ras_info.radius_secret}
	    {/listTD}
	    {listTD icon="TRUE"}
		<a href="/IBSng/admin/ras/ras_info.php?ras_ip={$ras_info.ras_ip|escape:"url"}">
		    {listTableBodyIcon action="view" cycle_color=TRUE}
		</a>
	    {/listTD}
	    {if $can_change}
	    {listTD icon="TRUE"}
		<a href="/IBSng/admin/ras/ras_list.php?deactive={$ras_info.ras_ip|escape:"url"}" {jsconfirm}>
		    {listTableBodyIcon action="disable"}
		</a> 
	    {/listTD}
	    {/if}
	{/listTR}
	{/foreach}

{/listTable}
<br>
{listTable title="Deactive Rases" cols_num=5}
	{listTableHeaderIcon action="enable" close_tr=TRUE}
	{listTR type="header"}
	    {listTD}
		Row
	    {/listTD}
	    {listTD}
		ID
	    {/listTD}
	    {listTD}
		RAS IP
	    {/listTD}
	    {listTD}
		Type
	    {/listTD}
	    {listTD}
		Radius Secret
	    {/listTD}
	{/listTR}
	{foreach from=$inactive_ras_infos item=ras_info}
	{listTR type="body"}
	    {listTD}
		    {counter name="disabled_row_no"}
	    {/listTD}
	    {listTD}
		    {$ras_info.ras_id}
	    {/listTD}
	    {listTD}
		    {$ras_info.ras_ip}
	    {/listTD}
	    {listTD}
	    	    {$ras_info.ras_type}
	    {/listTD}
	    {listTD}
		    {$ras_info.radius_secret}
	    {/listTD}
	    {if $can_change}
	    {listTD icon="TRUE"}
			<a href="/IBSng/admin/ras/ras_list.php?reactive={$ras_info.ras_ip|escape:"url"}">
			    {listTableBodyIcon action="enable"}
			</a> 
	    {/listTD}
	    {/if}
	{/listTR}
	{/foreach}
{/listTable}
{addRelatedLink}
    <a href="/IBSng/admin/ras/add_new_ras.php" class="RightSide_links">
	Add New RAS
    </a>
{/addRelatedLink}

{setAboutPage title="RAS List"}

{/setAboutPage}


{include file="admin_footer.tpl"}