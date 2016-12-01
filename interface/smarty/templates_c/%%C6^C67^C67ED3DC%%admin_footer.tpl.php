<?php /* Smarty version 2.6.13, created on 2006-06-13 19:23:16
         compiled from admin_footer.tpl */ ?>

		</td>
		<td width="180" align="center" valign="top" id="menu_full">
		    <?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_right_sidebar.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>
		</td>
		<td width="32" align="center" valign="top" id="menu_hidden">
		    <?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_right_sidebar_hidden.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>
		</td>
	
	</tr>
</table>
</td></tr>
<!-- End Main Table -->
<script language="javascript">
<?php if (isset ( $this->_tpl_vars['hide_menu'] )): ?>
    var menu_selected = "menu_hidden";
<?php else: ?>
    var menu_selected = "menu_full";
<?php endif; ?>

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