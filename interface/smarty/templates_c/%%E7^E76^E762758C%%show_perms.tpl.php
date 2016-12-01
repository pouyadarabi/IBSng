<?php /* Smarty version 2.6.13, created on 2006-06-17 12:51:51
         compiled from admin/admins/show_perms.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('function', 'config_load', 'admin/admins/show_perms.tpl', 4, false),array('function', 'eval', 'admin/admins/show_perms.tpl', 11, false),array('function', 'arrayJoin', 'admin/admins/show_perms.tpl', 78, false),array('function', 'html_options', 'admin/admins/show_perms.tpl', 93, false),array('block', 'headerMsg', 'admin/admins/show_perms.tpl', 8, false),array('block', 'listTable', 'admin/admins/show_perms.tpl', 12, false),array('block', 'listTR', 'admin/admins/show_perms.tpl', 13, false),array('block', 'listTD', 'admin/admins/show_perms.tpl', 14, false),array('block', 'addRelatedLink', 'admin/admins/show_perms.tpl', 148, false),array('block', 'setAboutPage', 'admin/admins/show_perms.tpl', 175, false),array('modifier', 'nl2br', 'admin/admins/show_perms.tpl', 46, false),array('modifier', 'escape', 'admin/admins/show_perms.tpl', 123, false),array('modifier', 'truncate', 'admin/admins/show_perms.tpl', 128, false),array('modifier', 'capitalize', 'admin/admins/show_perms.tpl', 150, false),)), $this); ?>
<?php echo smarty_function_config_load(array('file' => "perm_category_names.conf"), $this);?>

<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_header.tpl", 'smarty_include_vars' => array('title' => "Add Permission to admin [".($this->_tpl_vars['admin_username'])."]",'selected' => 'Admin List')));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
  $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "err_head.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>
    
<?php $this->_tag_stack[] = array('headerMsg', array('var_name' => 'add_success')); $_block_repeat=true;smarty_block_headerMsg($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    Permission Added Successfully.
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_headerMsg($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php echo smarty_function_eval(array('var' => $this->_tpl_vars['category_name'],'assign' => 'category_name_face'), $this);?>

	<?php $this->_tag_stack[] = array('listTable', array('title' => ($this->_tpl_vars['category_name_face']),'cols_num' => 4,'table_width' => "90%")); $_block_repeat=true;smarty_block_listTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('listTR', array('type' => 'header')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    Name
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    	Description
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			Affected Pages
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			Dependencies
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_from = $this->_tpl_vars['perms']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['perm']):
?>
	        <?php if ($this->_tpl_vars['perm']['name'] == $this->_tpl_vars['selected']): ?>
		<a name="selected"></a>
		<tr><td colspan=4>
			<!-- Form Title Table -->
			<table border="0" cellspacing="0" cellpadding="0" class="Form_Title">
			<tr>
				<td class="Form_Title_Begin"><img border="0" src="/IBSng/images/form/begin_form_title_red.gif"></td>
				<td class="Form_Title_red">Permission: <?php echo $this->_tpl_vars['perm']['name']; ?>
 <img border="0" src="/IBSng/images/arrow/arrow_orange_on_red.gif"></td>
				<td class="Form_Title_End"><img border="0" src="/IBSng/images/form/end_form_title_red.gif"></td>
		    	</tr>
		    	</table>
		    <!-- End Form Title Table  -->
		</td></tr>
		<tr class="list_Row_perm">
		<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			<nobr><?php echo $this->_tpl_vars['perm']['name']; ?>
</nobr>
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			<p class="in_body"><?php echo ((is_array($_tmp=$this->_tpl_vars['perm']['description'])) ? $this->_run_mod_handler('nl2br', true, $_tmp) : smarty_modifier_nl2br($_tmp)); ?>
</p>  
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			<?php $_from = $this->_tpl_vars['perm']['affected_pages']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['affected_page']):
?>
			    <nobr><?php echo $this->_tpl_vars['affected_page']; ?>
</nobr><br>
			<?php endforeach; endif; unset($_from); ?>
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			<?php $_from = $this->_tpl_vars['perm']['dependencies']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['dependency']):
?>
			    <nobr><?php echo $this->_tpl_vars['dependency']; ?>
</nobr><br>
			<?php endforeach; endif; unset($_from); ?>
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		<tr class="list_Row_perm">
		    <form action=/IBSng/admin/admins/show_perms.php>
    		    <input type=hidden name=admin_username value="<?php echo $this->_tpl_vars['admin_username']; ?>
">
		    <input type=hidden name=category value="<?php echo $this->_tpl_vars['category']; ?>
">
		    <input type=hidden name=perm_name value="<?php echo $this->_tpl_vars['selected']; ?>
">
		    <input type=hidden name=selected value="<?php echo $this->_tpl_vars['selected']; ?>
">
		    <td colspan=5>
			<table border=1 width=100% style="border-collapse:collapse" bordercolor="#FFFFFF">
			    <tr class="list_Row_darkcolor">
				<td>
				    <b><font color="#800000">Admin Has this Permission: 
					<?php if ($this->_tpl_vars['has_selected_perm'] == TRUE): ?> Yes </b>
					<td>
					<nobr><b><font color="#800000">Current Value: 
					    <?php if ($this->_tpl_vars['perm']['value_type'] == 'NOVALUE'): ?>
						Permission doesn't need value
					    <?php elseif ($this->_tpl_vars['cur_val'] == ""): ?>
						Empty
					    <?php elseif (is_array ( $this->_tpl_vars['cur_val'] )): ?>
					    <font size=1 color="#000000"><b>
						    <?php echo smarty_function_arrayJoin(array('array' => $this->_tpl_vars['cur_val'],'glue' => " , "), $this);?>

						</b></font>
						</nobr>
					    <?php else: ?>
						<?php echo $this->_tpl_vars['cur_val']; ?>

					    <?php endif; ?>
					<?php else: ?> 
					    No </b>
					<?php endif; ?>

		    <?php if ($this->_tpl_vars['can_change'] == TRUE && $this->_tpl_vars['perm']['value_type'] == 'SINGLEVALUE' || $this->_tpl_vars['perm']['value_type'] == 'MULTIVALUE'): ?>
			<td><b><font color="#800000">
			    New Value:
			<?php if (isset ( $this->_tpl_vars['perm']['value_candidates'] )): ?>
			    <select name="value">
				<?php echo smarty_function_html_options(array('values' => $this->_tpl_vars['perm']['value_candidates'],'output' => $this->_tpl_vars['perm']['value_candidates'],'selected' => $this->_tpl_vars['selected_value']), $this);?>

			    </select>
			<?php else: ?>
			    <input class="text" type=text name=value 
			    <?php if ($this->_tpl_vars['selected_value'] != ""): ?>
				value="<?php echo $this->_tpl_vars['selected_value']; ?>
"
			    <?php elseif ($this->_tpl_vars['perm']['value_type'] == 'SINGLEVALUE' && $this->_tpl_vars['has_selected_perm'] == TRUE): ?> 
				value="<?php echo $this->_tpl_vars['cur_val']; ?>
" 
			    <?php endif; ?> 
			    
			<?php endif; ?>
			
		    <?php endif; ?>
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
	    <?php else: ?>
		<?php $this->_tag_stack[] = array('listTR', array('type' => 'body')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			<a class="link_in_body" href="/IBSng/admin/admins/show_perms.php?category=<?php echo $this->_tpl_vars['category']; ?>
&admin_username=<?php echo $this->_tpl_vars['admin_username']; ?>
&selected=<?php echo ((is_array($_tmp=$this->_tpl_vars['perm']['name'])) ? $this->_run_mod_handler('escape', true, $_tmp, 'url') : smarty_modifier_escape($_tmp, 'url')); ?>
#selected">
			    <align="left"><nobr><b><?php echo $this->_tpl_vars['perm']['name']; ?>
</b></nobr></align>
			</a>
		    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			<p class="about_page" <?php echo ((is_array($_tmp=((is_array($_tmp=$this->_tpl_vars['perm']['description'])) ? $this->_run_mod_handler('nl2br', true, $_tmp) : smarty_modifier_nl2br($_tmp)))) ? $this->_run_mod_handler('truncate', true, $_tmp, 150, "...", false) : smarty_modifier_truncate($_tmp, 150, "...", false)); ?>
</p>
		    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			<?php $_from = $this->_tpl_vars['perm']['affected_pages']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['affected_page']):
?>
			    <nobr><?php echo $this->_tpl_vars['affected_page']; ?>
</nobr><br>
			<?php endforeach; endif; unset($_from); ?>
		    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			<?php $_from = $this->_tpl_vars['perm']['dependencies']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['dependency']):
?>
			    <nobr><?php echo $this->_tpl_vars['dependency']; ?>
</nobr><br>
			<?php endforeach; endif; unset($_from); ?>
		    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	    <?php endif; ?>
	<?php endforeach; endif; unset($_from); ?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>	
</center>
</form>
<?php if ($this->_tpl_vars['can_change'] == TRUE):  $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/admins/show_perm_categories.php?admin_username=<?php echo $this->_tpl_vars['admin_username']; ?>
" class="RightSide_links">
	Add New Permission to <b><?php echo ((is_array($_tmp=$this->_tpl_vars['admin_username'])) ? $this->_run_mod_handler('capitalize', true, $_tmp) : smarty_modifier_capitalize($_tmp)); ?>
</b>
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  endif;  $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/admins/admin_perms_list.php?admin_username=<?php echo $this->_tpl_vars['admin_username']; ?>
" class="RightSide_links">
	<b><?php echo ((is_array($_tmp=$this->_tpl_vars['admin_username'])) ? $this->_run_mod_handler('capitalize', true, $_tmp) : smarty_modifier_capitalize($_tmp)); ?>
</b> Permissions
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/admins/admin_info.php?admin_username=<?php echo $this->_tpl_vars['admin_username']; ?>
" class="RightSide_links">
	Admin <b><?php echo ((is_array($_tmp=$this->_tpl_vars['admin_username'])) ? $this->_run_mod_handler('capitalize', true, $_tmp) : smarty_modifier_capitalize($_tmp)); ?>
</b> info
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/admins/admin_list.php" class="RightSide_links">
	Admin List
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/admins/add_new_admin.php" class="RightSide_links">
	Add New Admin
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  $this->_tag_stack[] = array('setAboutPage', array('title' => 'Add New Permission')); $_block_repeat=true;smarty_block_setAboutPage($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start();  $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_setAboutPage($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_footer.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>