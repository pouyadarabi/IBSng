
		</td>
		<td width="180" align="center" valign="top" id="menu_full">
		    {include file="admin_right_sidebar.tpl"}
		</td>
		<td width="32" align="center" valign="top" id="menu_hidden">
		    {include file="admin_right_sidebar_hidden.tpl"}
		</td>
	
	</tr>
</table>
</td></tr>
<!-- End Main Table -->
<script language="javascript">
{if isset($hide_menu)}
    var menu_selected = "menu_hidden";
{else}
    var menu_selected = "menu_full";
{/if}

    menu_select=new DomContainer();
    menu_select.addByID("menu_full",[]);
    menu_select.addByID("menu_hidden",[]);
    menu_select.setOnSelect("display","");
    menu_select.setOnUnSelect("display","none");
    menu_select.select(menu_selected);
</script>
<!-- Footer -->
<table border="0" width="100%" cellspacing="0" cellpadding="0">
	<tr>
		<td class="Page_Bottom_Space" colspan="3"></td>
	</tr>
	<tr>
		<td>&nbsp;</td>
		<td width="34" rowspan="2"><img border="0" src="/IBSng/images/logo/logo_parspooyesh.gif"></td>
		<td rowspan="2" width="280" class="Page_Footer">
		<!--Footer Links -->
			<a class="Footer_Link" target="_blank" href="http://www.ParsPooyesh.com">www.Parspooyesh.com</a>
			&nbsp; 
			Contact Info | 
			Help | 
			License</td>
		<!--END Footer Links -->
	</tr>
	<tr>
		<td class="Page_Footer_Line"></td>
	</tr>
</table>
<!-- End Footer -->
</td></tr></table>