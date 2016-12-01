{* Show all string of a multistr
   on success page is shown
   on failure error is shown on top of page
   Variables:
    $raw_str : raw multi string
    $all_strs: decomposed strings of multi str
*}

{include file="header.tpl" title="Show Multiple Strings"}
{include file="err_head.tpl"}
<table border="0"  class="List_Main" cellspacing="1" bordercolor="#FFFFFF" cellpadding="0" width=100%>
	<tr> <td>
		<!-- List Title Table -->
		<table border="0" cellspacing="0" cellpadding="0" class="List_Title">
			<tr>
				<td class="List_Title_Begin" rowspan="2"><img border="0" src="/IBSng/images/form/begin_form_title_red.gif"></td>
				<td class="List_Title" rowspan="2">Show Multiple Strings {helpicon subject="multi str" category="util"}</td>
				<td class="List_Title_End" rowspan="2"><img border="0" src="/IBSng/images/list/end_of_list_title_red.gif" width="5" height="20"></td>
				<td class="List_Title_Top_Line" align="RIGHT">
				Raw Multi String:<font color="#800000"> {$raw_str|truncate:40}</font></td>
			</tr>
			<tr>
				<td class="List_Title_End_Line"></td>
			</tr>
		</table>
		<!-- End List Title Table -->
		</td>
		    <tr>
			<td>
	{multiTable}
	    {foreach from=$all_strs key=index item=str}
	        {if $index%4==0}
		    {multiTableTR}
    		{/if}
		{multiTableTD type="left"}
		    {math equation="index+1" index=$index}.
		{/multiTableTD}
		{multiTableTD type="right" width="25%"}
		    {$str}
		{/multiTableTD}
	    {/foreach}

	    {math equation="index+1" index=$index assign="index"}
	    {multiTablePad last_index=$index go_until=4}
	    
	{/multiTable}
	<!-- view table Foot -->
	<tr class="List_Foot_Line_red">
		<td colspan=100></td>
	</tr>
	<!-- End view table Foot-->
</table>


{literal}
<script language="javascript">
    window.focus();
</script>
{/literal}

{include file="footer.tpl"}
