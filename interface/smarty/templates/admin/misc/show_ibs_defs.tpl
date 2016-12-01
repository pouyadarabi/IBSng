{include file="admin_header.tpl" title="IBS Definitions" selected="Advanced Configuration"}
{include file="err_head.tpl"}

{headerMsg var_name="save_success"}Definitions updated successfully.{/headerMsg}
{headerMsg}
Warning: Changing these values may results IBSng not working properly. <br>Don't change any value until you know
what are you doing.
{/headerMsg}

    <form method=POST>
    {addEditTable title="IBS Definitions" table_width="400"}
    {foreach from=$defs_arr item=def_arr}
    	{if is_array($def_arr.value)}

	{addEditTD type="left" comment="TRUE"}
	    {$def_arr.name|replace:"_":" "}
	{/addEditTD}
	{addEditTD type="right" comment="TRUE"}
		{foreach from=$def_arr.value key=index item=member }
		    <input class="large_text" type=text name="def_{$def_arr.name}__{$index}__" value="{$member}">
		{/foreach}
		    <font size=1>(new value)</font><input class="text" type=text name="def_{$def_arr.name}__new__" value="">
	{/addEditTD}    
	    {else}
	{addEditTD type="left"}
	    {$def_arr.name|replace:"_":" "}
	{/addEditTD}
	{addEditTD type="right"}
	    <input class="large_text" type=text name="def_{$def_arr.name}" value="{$def_arr.value}">
	{/addEditTD}    

        {/if}
    {/foreach}
{/addEditTable}
<input type=hidden name=action value=save>
</form>

{addRelatedLink}
    <a href="/IBSng/admin/setting" class="RightSide_links">
	Settings
    </a>
{/addRelatedLink}


{addRelatedLink}
    <a href="/IBSng/admin/misc/core_statistics.php" class="RightSide_links">
	Core Statistics
    </a>
{/addRelatedLink}

{setAboutPage title="IBS Definitions"}

{/setAboutPage}
{include file="admin_footer.tpl"}
