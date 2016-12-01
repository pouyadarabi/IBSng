{* List permissions of an admin
    
*}
{config_load file=perm_category_names.conf}
{include file="header.tpl" title="Template Permission List"}
{include file="err_head.tpl"}
    {viewTable title="Template $template_name Permission List" table_width="100%"}
    <tr><td>
    {foreach from=$perms key=category item=cat_perms}
	{listTable title="`$category_names.$category`" cols_num=3 table_width="100%"}
	    {listTR type="header"}
		{listTD}
		    Name
		{/listTD}
		{listTD}
		    Value
		{/listTD}
		{listTD}
			Description
		{/listTD}
	    {/listTR}	
	    {section loop=$cat_perms name=index}
	        {listTR type="body"}
		{listTD}
		    <nobr><b><font size=2>{$cat_perms[index].name}</font></b>
		{/listTD}
		{listTD}
		<nobr>
		    {if $cat_perms[index].value_type eq "NOVALUE"}
			No Value
		    {elseif $cat_perms[index].value_type eq "SINGLEVALUE"}
			{$cat_perms[index].value} 
		    {elseif $cat_perms[index].value_type eq "MULTIVALUE"}
			<table border=1 style="border-collapse:collapse" bordercolor="#c0c0c0" width="100%">
			{foreach from=$cat_perms[index].value item=val}
			    <tr class="{cycle values="list_Row_LightColor,list_Row_DarkColor"}">
				<td>
				    {$val} 
			{/foreach}
			</table>
			    			
		    {/if}
		{/listTD}
		{listTD}
		    {$cat_perms[index].description|truncate:50}
		{/listTD}
		{/listTR}
	    {/section}
	{/listTable}
    {/foreach}
</td></tr>
{/viewTable}
{literal}
<script language="javascript">
    window.focus();
</script>
{/literal}
