<?php /* Smarty version 2.6.13, created on 2006-06-17 12:51:29
         compiled from admin/admins/admin_perms_list.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('function', 'config_load', 'admin/admins/admin_perms_list.tpl', 4, false),array('function', 'listTableHeaderIcon', 'admin/admins/admin_perms_list.tpl', 39, false),array('function', 'eval', 'admin/admins/admin_perms_list.tpl', 65, false),array('function', 'cycle', 'admin/admins/admin_perms_list.tpl', 72, false),array('function', 'jsconfirm', 'admin/admins/admin_perms_list.tpl', 78, false),array('function', 'listTableBodyIcon', 'admin/admins/admin_perms_list.tpl', 100, false),array('block', 'headerMsg', 'admin/admins/admin_perms_list.tpl', 13, false),array('block', 'listTable', 'admin/admins/admin_perms_list.tpl', 38, false),array('block', 'listTR', 'admin/admins/admin_perms_list.tpl', 43, false),array('block', 'listTD', 'admin/admins/admin_perms_list.tpl', 44, false),array('block', 'addRelatedLink', 'admin/admins/admin_perms_list.tpl', 122, false),array('block', 'setAboutPage', 'admin/admins/admin_perms_list.tpl', 144, false),array('modifier', 'escape', 'admin/admins/admin_perms_list.tpl', 77, false),array('modifier', 'truncate', 'admin/admins/admin_perms_list.tpl', 95, false),array('modifier', 'capitalize', 'admin/admins/admin_perms_list.tpl', 124, false),)), $this); ?>
<?php echo smarty_function_config_load(array('file' => "admin_perms_list.conf"), $this);?>

<?php echo smarty_function_config_load(array('file' => "perm_category_names.conf"), $this);?>

<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_header.tpl", 'smarty_include_vars' => array('title' => "Admin [".($this->_tpl_vars['admin_username'])."] Permission List",'selected' => 'Admin List')));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
  $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "err_head.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>

    

<center>

<?php $this->_tag_stack[] = array('headerMsg', array('var_name' => 'del_perm_success')); $_block_repeat=true;smarty_block_headerMsg($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    Permission deleted from admin successfully
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_headerMsg($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('headerMsg', array('var_name' => 'del_perm_val_success')); $_block_repeat=true;smarty_block_headerMsg($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    Permission Value updated successfully
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_headerMsg($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('headerMsg', array('var_name' => 'save_template_success')); $_block_repeat=true;smarty_block_headerMsg($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    Permissions Saved to template successfully
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_headerMsg($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('headerMsg', array('var_name' => 'load_template_success')); $_block_repeat=true;smarty_block_headerMsg($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    Permission Template Loaded into admin successfully
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_headerMsg($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('headerMsg', array('var_name' => 'del_template_succes')); $_block_repeat=true;smarty_block_headerMsg($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    Permission Template Deleted successfully
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_headerMsg($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


<table boreder=1>
<tr><td>

    <?php $_from = $this->_tpl_vars['perms']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['category'] => $this->_tpl_vars['cat_perms']):
?>
	<?php $this->_tag_stack[] = array('listTable', array('title' => ($this->_tpl_vars['category_names'][$this->_tpl_vars['category']]),'cols_num' => 3,'table_width' => "100%")); $_block_repeat=true;smarty_block_listTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo smarty_function_listTableHeaderIcon(array('action' => 'view'), $this);?>

	<?php if ($this->_tpl_vars['can_change'] == TRUE): ?>
	    <?php echo smarty_function_listTableHeaderIcon(array('action' => 'delete','close_tr' => 'TRUE'), $this);?>

	<?php endif; ?>
	    <?php $this->_tag_stack[] = array('listTR', array('type' => 'header')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    Name
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    Value
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			Description
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>	
        <?php $_from = $this->_tpl_vars['cat_perms']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['perm']):
?>
	    <?php $this->_tag_stack[] = array('listTR', array('type' => 'body')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <nobr><b><font size=2><?php echo $this->_tpl_vars['perm']['name']; ?>
</font></b>
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <?php if ($this->_tpl_vars['perm']['value_type'] == 'NOVALUE'): ?>
			No Value
		    <?php elseif ($this->_tpl_vars['perm']['value_type'] == 'SINGLEVALUE'): ?>
			<?php echo $this->_tpl_vars['perm']['value']; ?>
 
			<?php if ($this->_tpl_vars['can_change'] == TRUE): ?>
			    <a class="link_in_body" href="<?php echo smarty_function_eval(array('var' => $this->_config[0]['vars']['show_perms_link']), $this);?>
">
				Change
			    </a>
			<?php endif; ?>
		<?php elseif ($this->_tpl_vars['perm']['value_type'] == 'MULTIVALUE'): ?>
			<table border=1 style="border-collapse:collapse" bordercolor="#c0c0c0">
			<?php $_from = $this->_tpl_vars['perm']['value']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['val']):
?>
			    <tr class="<?php echo smarty_function_cycle(array('values' => "list_Row_LightColor,list_Row_DarkColor"), $this);?>
">
				<td>
				    <?php echo $this->_tpl_vars['val']; ?>
 
				<td>
				    <?php if ($this->_tpl_vars['can_change'] == TRUE): ?>
					<a class="link_in_body" href="/IBSng/admin/admins/admin_perms_list.php?admin_username=<?php echo $this->_tpl_vars['admin_username']; ?>
&delete_perm=<?php echo ((is_array($_tmp=$this->_tpl_vars['perm']['name'])) ? $this->_run_mod_handler('escape', true, $_tmp, 'url') : smarty_modifier_escape($_tmp, 'url')); ?>
&delete_perm_val=<?php echo ((is_array($_tmp=$this->_tpl_vars['val'])) ? $this->_run_mod_handler('escape', true, $_tmp, 'url') : smarty_modifier_escape($_tmp, 'url')); ?>
" 
					 <?php echo smarty_function_jsconfirm(array('msg' => "Are you sure you want to delete value ".($this->_tpl_vars['val'])." from ".($this->_tpl_vars['perm']['name'])), $this);?>
>
					    <font size=1><b>Delete</b></font>
					</a>
				    <?php endif; ?>
			<?php endforeach; endif; unset($_from); ?>
			<?php if ($this->_tpl_vars['can_change'] == TRUE): ?>
			    <tr class="<?php echo smarty_function_cycle(array('values' => "list_Row_LightColor,list_Row_DarkColor"), $this);?>
">
				<td colspan=2>
				    <a class="link_in_body" href="<?php echo smarty_function_eval(array('var' => $this->_config[0]['vars']['show_perms_link']), $this);?>
">
					    <b><nobr>Add Another Value</b>
				    </a>
			<?php endif; ?>
			</table>
			    			
		    <?php endif; ?>
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <?php echo ((is_array($_tmp=$this->_tpl_vars['perm']['description'])) ? $this->_run_mod_handler('truncate', true, $_tmp, 100) : smarty_modifier_truncate($_tmp, 100)); ?>

		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
				
		<?php $this->_tag_stack[] = array('listTD', array('icon' => 'TRUE')); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <a href="<?php echo smarty_function_eval(array('var' => $this->_config[0]['vars']['show_perms_link']), $this);?>
">
			    <?php echo smarty_function_listTableBodyIcon(array('action' => 'view','cycle_color' => 'TRUE'), $this);?>

		    </a>
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

		<?php $this->_tag_stack[] = array('listTD', array('icon' => 'TRUE')); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php if ($this->_tpl_vars['can_change'] == TRUE): ?>
		    <a href="/IBSng/admin/admins/admin_perms_list.php?admin_username=<?php echo $this->_tpl_vars['admin_username']; ?>
&delete_perm=<?php echo ((is_array($_tmp=$this->_tpl_vars['perm']['name'])) ? $this->_run_mod_handler('escape', true, $_tmp, 'url') : smarty_modifier_escape($_tmp, 'url')); ?>
"
		    <?php echo smarty_function_jsconfirm(array('msg' => "Are you sure you want to delete Permission ".($this->_tpl_vars['perm']['name'])), $this);?>
>
		    <?php echo smarty_function_listTableBodyIcon(array('action' => 'delete'), $this);?>

		    </a>
		<?php endif; ?>
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	        <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	    <?php endforeach; endif; unset($_from); ?>
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	    <?php endforeach; endif; unset($_from); ?>
	    </td></tr></table>


<?php if ($this->_tpl_vars['can_change'] == TRUE): ?>
    <?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin/admins/admin_perms_list_templates.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
  $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/admins/show_perm_categories.php?admin_username=<?php echo $this->_tpl_vars['admin_username']; ?>
" class="RightSide_links">
	Add New Permission to <b><?php echo ((is_array($_tmp=$this->_tpl_vars['admin_username'])) ? $this->_run_mod_handler('capitalize', true, $_tmp) : smarty_modifier_capitalize($_tmp)); ?>
</b>
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  endif; ?>

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
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  $this->_tag_stack[] = array('setAboutPage', array('title' => 'Admin Change Password')); $_block_repeat=true;smarty_block_setAboutPage($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_setAboutPage($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_footer.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>