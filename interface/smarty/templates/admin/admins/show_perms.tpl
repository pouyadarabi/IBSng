{* 
	Show Permissions of one category
*}
{config_load file=perm_category_names.conf}
{include file="admin_header.tpl" title="Add Permission to admin [$admin_username]" selected="Admin List"}
{include file="err_head.tpl"}
    
{headerMsg var_name="add_success"}
    Permission Added Successfully.
{/headerMsg}
	{eval var=$category_name assign="category_name_face"}
	{listTable title="$category_name_face" cols_num=4 table_width="90%"}
	    {listTR type="header"}
		{listTD}
		    Name
		{/listTD}
		{listTD}
		    	Description
		{/listTD}
		{listTD}
			Affected Pages
		{/listTD}
		{listTD}
			Dependencies
		{/listTD}
	    {/listTR}
	{foreach from=$perms item=perm}
	        {if $perm.name eq $selected}
		<a name="selected"></a>
		<tr><td colspan=4>
			<!-- Form Title Table -->
			<table border="0" cellspacing="0" cellpadding="0" class="Form_Title">
			<tr>
				<td class="Form_Title_Begin"><img border="0" src="/IBSng/images/form/begin_form_title_red.gif"></td>
				<td class="Form_Title_red">Permission: {$perm.name} <img border="0" src="/IBSng/images/arrow/arrow_orange_on_red.gif"></td>
				<td class="Form_Title_End"><img border="0" src="/IBSng/images/form/end_form_title_red.gif"></td>
		    	</tr>
		    	</table>
		    <!-- End Form Title Table  -->
		</td></tr>
		<tr class="list_Row_perm">
		{listTD}
			<nobr>{$perm.name}</nobr>
		{/listTD}
		{listTD}
			<p class="in_body">{$perm.description|nl2br}</p>  
		{/listTD}
		{listTD}
			{foreach from=$perm.affected_pages item=affected_page}
			    <nobr>{$affected_page}</nobr><br>
			{/foreach}
		{/listTD}
		{listTD}
			{foreach from=$perm.dependencies item=dependency}
			    <nobr>{$dependency}</nobr><br>
			{/foreach}
		{/listTD}
		<tr class="list_Row_perm">
		    <form action=/IBSng/admin/admins/show_perms.php>
    		    <input type=hidden name=admin_username value="{$admin_username}">
		    <input type=hidden name=category value="{$category}">
		    <input type=hidden name=perm_name value="{$selected}">
		    <input type=hidden name=selected value="{$selected}">
		    <td colspan=5>
			<table border=1 width=100% style="border-collapse:collapse" bordercolor="#FFFFFF">
			    <tr class="list_Row_darkcolor">
				<td>
				    <b><font color="#800000">Admin Has this Permission: 
					{if $has_selected_perm eq TRUE} Yes </b>
					<td>
					<nobr><b><font color="#800000">Current Value: 
					    {if $perm.value_type eq "NOVALUE"}
						Permission doesn't need value
					    {elseif $cur_val eq ""}
						Empty
					    {elseif is_array($cur_val)}
					    <font size=1 color="#000000"><b>
						    {arrayJoin array=$cur_val glue=" , "}
						</b></font>
						</nobr>
					    {else}
						{$cur_val}
					    {/if}
					{else} 
					    No </b>
					{/if}

		    {if $can_change eq TRUE && $perm.value_type eq "SINGLEVALUE" || $perm.value_type eq "MULTIVALUE" }
			<td><b><font color="#800000">
			    New Value:
			{if isset($perm.value_candidates)}
			    <select name="value">
				{html_options values=$perm.value_candidates output=$perm.value_candidates selected=$selected_value}
			    </select>
			{else}
			    <input class="text" type=text name=value 
			    {if $selected_value ne ""}
				value="{$selected_value}"
			    {elseif $perm.value_type eq "SINGLEVALUE" && $has_selected_perm eq TRUE} 
				value="{$cur_val}" 
			    {/if} 
			    
			{/if}
			
		    {/if}
		    </td></tr>
		    </table>
		    <tr><td colspan=4>
			    <table border="0" cellspacing="0" cellpadding="0" class="Form_Foot">
				<tr>
					<td class="Form_Foot_Begin_Line_red"></td>
					<td rowspan="2" class="Form_Foot_End"><img border="0" src="/IBSng/images/list/end_of_line_bottom_of_table.gif"></td>
					<td rowspan="2" class="Form_Foot_Buttons"><input type=image src="/IBSng/images/icon/add.gif"></td>
				</tr>
				<tr>
					<td class="Form_Foot_Below_Line_red"></td>
				</tr>
			</table>
		    </td></tr>		
	    {else}
		{listTR type="body"}
		    {listTD}
			<a class="link_in_body" href="/IBSng/admin/admins/show_perms.php?category={$category}&admin_username={$admin_username}&selected={$perm.name|escape:"url"}#selected">
			    <align="left"><nobr><b>{$perm.name}</b></nobr></align>
			</a>
		    {/listTD}
		    {listTD}
			<p class="about_page" {$perm.description|nl2br|truncate:150:"...":false}</p>
		    {/listTD}
		    {listTD}
			{foreach from=$perm.affected_pages item=affected_page}
			    <nobr>{$affected_page}</nobr><br>
			{/foreach}
		    {/listTD}
		    {listTD}
			{foreach from=$perm.dependencies item=dependency}
			    <nobr>{$dependency}</nobr><br>
			{/foreach}
		    {/listTD}
		{/listTR}
	    {/if}
	{/foreach}

    {/listTable}	
</center>
</form>
{if $can_change eq TRUE}
{addRelatedLink}
    <a href="/IBSng/admin/admins/show_perm_categories.php?admin_username={$admin_username}" class="RightSide_links">
	Add New Permission to <b>{$admin_username|capitalize}</b>
    </a>
{/addRelatedLink}
{/if}
{addRelatedLink}
    <a href="/IBSng/admin/admins/admin_perms_list.php?admin_username={$admin_username}" class="RightSide_links">
	<b>{$admin_username|capitalize}</b> Permissions
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/admins/admin_info.php?admin_username={$admin_username}" class="RightSide_links">
	Admin <b>{$admin_username|capitalize}</b> info
    </a>
{/addRelatedLink}
{addRelatedLink}
    <a href="/IBSng/admin/admins/admin_list.php" class="RightSide_links">
	Admin List
    </a>
{/addRelatedLink}
{addRelatedLink}
    <a href="/IBSng/admin/admins/add_new_admin.php" class="RightSide_links">
	Add New Admin
    </a>
{/addRelatedLink}
{setAboutPage title="Add New Permission"}
{/setAboutPage}


{include file="admin_footer.tpl"}