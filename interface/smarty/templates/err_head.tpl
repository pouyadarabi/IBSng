{if isset($err_msgs) or isInRequest("err_msg")}
<table align=center border=0>
{if isset($err_msgs) }
    {foreach from=$err_msgs item=err}
	<tr>
	    <td align=left>
		<img border="0" src="/IBSng/images/msg/before_error_message.gif">
	    </td>
	    <td align=left class="error_messages">	    
		{$err|escape:"html"}
	    </td>
	</tr>
    {/foreach}
{/if}
{if isInRequest("err_msg")}
	<tr>
	    <td align=left>
		<img border="0" src="/IBSng/images/msg/before_error_message.gif">
	    </td>
	    <td align=left class="error_messages">	    
		{$smarty.request.err_msg|escape:"html"}
	    </td>
	</tr>
{/if}
</table>
<br>
{/if}