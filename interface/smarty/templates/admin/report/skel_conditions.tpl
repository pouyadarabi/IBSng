<script language="javascript" src="/IBSng/js/check_box_container.js"></script>
<script language="javascript">
    {$name}_selected = new CheckBoxContainer();
</script>

    {listTableHeader cols_num=30 type="left"}
	{$title}
    {/listTableHeader}
    {listTableHeader type="right"}
	<table cellpadding=0 cellspacing=0 border=0 class="List_Top_line" align="right">
	<tr>
	    <td><input style="height:11" type=checkbox name={$name}_check_all></td>
	    <td>Check All Attributes</td>	
	</tr>
	</table>
    {/listTableHeader}
        <tr><td colspan=30>
	{multiTable}
		{if isset($inc)}
		    {include file=$inc}
		{elseif $file_value}
			{eval var=$file_value}
		{/if}
	{/multiTable}
	</td></tr>
<script language="javascript">
    {$name}_selected.setCheckAll('{$form_name}','{$name}_check_all');
</script>
