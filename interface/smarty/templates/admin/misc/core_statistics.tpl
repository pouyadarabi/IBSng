{include file="admin_header.tpl" title="Core Statistics" selected="Core Statistics"}
{include file="err_head.tpl"}


{viewTable title="Statistics" }

    {foreach from=$stats item=stat}

	{addEditTD type="left"}
	    	{$stat[0]|replace:"_":" "|capitalize}
	{/addEditTD}
	{addEditTD type="right"}
		{if $stat[1][1] == "int"}
		    {$stat[1][0]|price}
		{elseif $stat[1][1] == "seconds"}
		    {$stat[1][0]|duration}
		{elseif $stat[1][1] == "bytes"}
		    {$stat[1][0]|byte}
		{else}
		    {$stat[1][0]}
		{/if}
	{/addEditTD}    


    {/foreach}

{/viewTable}


{addRelatedLink}
    <a href="/IBSng/admin/misc/show_ibs_defs.php" class="RightSide_links">
	Advanced Configuration	
    </a>
{/addRelatedLink}

{setAboutPage title="Core Statistics"}

{/setAboutPage}
{include file="admin_footer.tpl"}
