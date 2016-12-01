<script language="javascript" src="/IBSng/js/dom_container.js"> </script>
<script language="javascript">
    ras_select=new DomContainer();
    ras_select.setOnSelect("display","");
    ras_select.setOnUnSelect("display","none");
</script>

	<table border="0"  class="form_Main" cellspacing="0" cellpadding="0" width=100%>
	<tr>
		<td  valign="bottom">
		<!-- view  Title Table -->
		<table border="0" cellspacing="0" cellpadding="0" class="form_title">
			<tr>
				<td class="form_Title_Begin"><img border="0" src="/IBSng/images/form/begin_form_title_orange.gif"></td>
				<td class="form_Title_orange"><input type=radio name=ras value="_ALL_" {if $ras_selected eq "_ALL_"} checked {/if} onClick='ras_select.select("_ALL_")'>
				 All RASes</td>
				<td class="form_Title_End"><img border="0" src="/IBSng/images/form/end_form_title_orange.gif"></td>
			</tr>
		</table>
		<!-- End view  Title Table -->
		</td>
    	<tr>
		<td height=2 colspan=100></td>
	</tr>

        <tr>
	<td>
	    
	    <div id="_ALL_"></div>
	    <script language="javascript">
		ras_select.addByID("_ALL_");
	    </script>
    {foreach from=$rases key=ras_ip item=ports}
    
	{ipescape ip=$ras_ip assign="ras_ip_escaped"}
	
	<table border="0"  class="List_Main" cellspacing="1" bordercolor="#FFFFFF" cellpadding="0" width=100%>
	<tr>
		<td colspan="5" valign="bottom">
		<!-- List Title Table -->
		<table border="0" cellspacing="0" cellpadding="0" class="List_Title">
			<tr>
				<td class="List_Title_Begin" rowspan="2"><img border="0" src="/IBSng/images/form/begin_form_title_red.gif"></td>
				<td class="List_Title" rowspan="2">
				<input type=radio name=ras value="{$ras_ip}"  {if $ras_selected eq $ras_ip} checked {/if} onClick="ras_select.select('{$ras_ip}')">
				RAS {$ras_desc_mapping.$ras_ip}&nbsp;
				<img border="0" src="/IBSng/images/arrow/arrow_orange_on_red.gif" width="10" height="10">
				</td>
				<td class="List_Title_End" rowspan="2"><img border="0" src="/IBSng/images/list/end_of_list_title_red.gif" width="5" height="20"></td>
				<td class="List_Title_Top_Line" align="RIGHT"><input style="height:11" class="checkbox" type=checkbox name="{$ras_ip_escaped}_ALL_" {ifisinrequest name="`$ras_ip_escaped`__ALL_" default_var="`$ras_ip`__ALL_" default="" value="checked"}>All Ports</td>
			</tr>
			<tr>
				<td class="List_Title_End_Line"></td>
			</tr>
		</table>
		<!-- End List Title Table -->
		</td>
		    <tr>
			<td>
			    <table id="{$ras_ip}" width="100%" border=0 cellspacing=0 cellpadding=0>
	{foreach from=$ports key=index item=port}
	        {if $index%5==0}
			</tr>
			<tr>
			    <td height=1></td>
			</tr>
			{cycle values="light,dark" assign="color"}	
			<tr class="list_row_{$color}color">
    		{/if}
		<td class="Form_Content_Row_Begin"><img border="0" src="/IBSng/images/row/begin_of_row_{$color}.gif"></td>
		<td class="Form_Content_Row_Begin"><input type=checkbox name="{$ras_ip_escaped}__{$port.port_name}" {ifisinrequest name="`$ras_ip_escaped`__`$port.port_name`" default_var="`$ras_ip`_`$port.port_name`" default="" value="checked"}></td>
		<td align="left" class="List_col"><b>{$port.port_name}</b></td>
		<td class="Form_Content_Row_End"><img border="0" src="/IBSng/images/row/end_of_row_{$color}.gif"></td>
	    
	{/foreach}
		    </tr>
			</td>
			    </table>
	<script language="javascript">
	    ras_select.addByID("{$ras_ip}");
	</script>
	<!-- List Foot -->
	
	</tr>
	    </table>
	
    {/foreach}

	<tr>
		<td height=2 colspan=100></td>
	</tr>
	<!-- End view table Foot-->
</table>

    <script language="javascript">
	ras_select.select("{$ras_selected}");
    </script>
