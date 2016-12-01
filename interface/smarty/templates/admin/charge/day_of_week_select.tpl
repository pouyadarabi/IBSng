    
    {literal}
    <script language="javascript" src="/IBSng/js/check_box_container.js"></script>
    <script language="javascript">
	var dows=new CheckBoxContainer();
    </script>
    {/literal}
    <table border="0"  class="List_Main" cellspacing="0" bordercolor="#FFFFFF" cellpadding="0" width=100%>
	<tr>
		<td colspan="30" valign="bottom">
		<!-- List Title Table -->
		<table border="0" cellspacing="0" cellpadding="0" class="List_Title">
			<tr>
				<td class="List_Title_Begin" rowspan="2"><img border="0" src="/IBSng/images/form/begin_form_title_red.gif"></td>
				<td class="List_Title" rowspan="2">Days of Week&nbsp;<img border="0" src="/IBSng/images/arrow/arrow_orange_on_red.gif" width="10" height="10"></td>
				<td class="List_Title_End" rowspan="2"><img border="0" src="/IBSng/images/list/end_of_list_title_red.gif" width="5" height="20"></td>
				<td class="List_Title_Top_Line" align="RIGHT"><input style="height:11" class="checkbox" type=checkbox name="checkall">checkall</td>
			</tr>
			<tr>
				<td class="List_Title_End_Line"></td>
			</tr>
		</table>
		<!-- End List Title Table -->
		</td>
	<tr>
	        <td colspan="30" class="Form_Content_Row_Space"></td>
	</tr>

    <tr>
    {foreach from=$day_of_weeks key=index item=day_of_week}
    
		<td class="Form_Content_Row_Begin"><img border="0" src="/IBSng/images/row/begin_of_row_light.gif"></td>
		<td class="Form_Content_Row_Left_light" style="width:5">
    		<input type=checkbox name="{$day_of_week}" {ifisinrequest name=$day_of_week default_var=$day_of_week default="" value="checked"} >
		<script language="javascript">
		    dows.addByName("{$form_name}","{$day_of_week}");
		</script></td>
		<td class="Form_Content_Row_Left_light" style="width:20">
			{$day_of_week}</td>
		<td class="Form_Content_Row_End"><img border="0" src="/IBSng/images/row/end_of_row_light.gif"></td>
    {/foreach}
    <script language="javascript">
	    {if isset($check_all_days) and $check_all_days}
		dows.checkAll();
	    {/if}
	    dows.setCheckAll("{$form_name}","checkall");
    </script>
	<!-- List Foot -->
	<tr>
	        <td colspan="30" class="Form_Content_Row_Space"></td>
	</tr>
	<tr class="List_Foot_Line_red">
		<td colspan=100></td>
	</tr>
	<!-- End List Foot-->
</table>

