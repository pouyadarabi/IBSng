{* 
*}

{include file="header.tpl" title="Check Usernames For User Add"}
{include file="err_head.tpl"}
    {foreach from=$alerts key=error item=users}
	<table align=center border=0>
	<tr>
	    <td align=left>
		<img border="0" src="/IBSng/images/msg/before_error_message.gif">
	    </td>
	    <td align=left class="error_messages">	    
		Error: {$error}
	    </td>
	</tr>
	</table>
	<br>
	{listTable no_header=TRUE no_foot=TRUE table_width="100%"} 
        {listTableHeader cols_num=30 type="left"}
		Usernames With Error
	{/listTableHeader}
	{listTableHeader type="right"}
	    &nbsp;
	{/listTableHeader}
	{multiTable}
	{foreach from=$users item=user key=index}
	{if $index%4==0}
	    {multiTableTR}
    	{/if}
	    {multiTableTD type="left"}
		    {math equation="index+1" index=$index}.
		{/multiTableTD}
		{multiTableTD type="right"}
		    {$user}
		{/multiTableTD}
	{/foreach}
	{/multiTable}
	{/listTable}
    {foreachelse}
	<table align=center border=0>
	<tr>
	    <td align=left>
		<img border="0" src="/IBSng/images/msg/before_successful_msg.gif">
	    </td>
	    <td align=left class="error_messages">	    
		No Alerts!

	    </td>
	</tr>
	</table>
    {/foreach}
{include file="footer.tpl"}
