<?php /* Smarty version 2.6.13, created on 2006-06-17 12:51:44
         compiled from admin/admins/perm_category_select.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('function', 'config_load', 'admin/admins/perm_category_select.tpl', 4, false),array('block', 'addRelatedLink', 'admin/admins/perm_category_select.tpl', 48, false),array('block', 'setAboutPage', 'admin/admins/perm_category_select.tpl', 76, false),array('modifier', 'capitalize', 'admin/admins/perm_category_select.tpl', 50, false),)), $this); ?>
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

<table border="0"  class="List_Main" cellspacing="1" bordercolor="#FFFFFF" cellpadding="0" width="400">
	<tr>
		<td class="Menu_Content_Row_white" align="center" colspan=4>
		<font size=2 color="#800000">Please Select Permission category:</font></td>
	<tr>	
	    <td>
		<img border=0 src="/IBSng/images/permission/admin_permission.gif">
	    <td class="Menu_Content_Row_white">
	    <a class="page_menu" href="/IBSng/admin/admins/show_perms.php?category=ADMIN&admin_username=<?php echo $this->_tpl_vars['admin_username']; ?>
"><?php echo $this->_config[0]['vars']['ADMIN']; ?>
</a>
		
	    <td>
		<img border=0 src="/IBSng/images/permission/user_permission.gif">
	    <td class="Menu_Content_Row_white">	
		<a class="page_menu" href="/IBSng/admin/admins/show_perms.php?category=USER&admin_username=<?php echo $this->_tpl_vars['admin_username']; ?>
"><?php echo $this->_config[0]['vars']['USER']; ?>
</a>

	<tr>	
	    <td>
		<img border=0 src="/IBSng/images/permission/charge_permission.gif">
	    <td class="Menu_Content_Row_white">
		<a class="page_menu" href="/IBSng/admin/admins/show_perms.php?category=CHARGE&admin_username=<?php echo $this->_tpl_vars['admin_username']; ?>
"><?php echo $this->_config[0]['vars']['CHARGE']; ?>
</a>
		
	    <td>
		<img border=0 src="/IBSng/images/permission/group_permission.gif">
	    <td class="Menu_Content_Row_white">
		<a class="page_menu" href="/IBSng/admin/admins/show_perms.php?category=GROUP&admin_username=<?php echo $this->_tpl_vars['admin_username']; ?>
"><?php echo $this->_config[0]['vars']['GROUP']; ?>
</a>

	<tr>	
	    <td>
		<img border=0 src="/IBSng/images/permission/ras_permission.gif">
	    <td class="Menu_Content_Row_white">
		<a class="page_menu" href="/IBSng/admin/admins/show_perms.php?category=RAS&admin_username=<?php echo $this->_tpl_vars['admin_username']; ?>
"><?php echo $this->_config[0]['vars']['RAS']; ?>
</a>
		
	    <td>
		<img border=0 src="/IBSng/images/permission/misc_permission.gif">
	    <td class="Menu_Content_Row_white">
		<a class="page_menu" href="/IBSng/admin/admins/show_perms.php?category=MISC&admin_username=<?php echo $this->_tpl_vars['admin_username']; ?>
"><?php echo $this->_config[0]['vars']['MISC']; ?>
</a>

    </table>

</form>
<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/admins/show_perm_categories.php?admin_username=<?php echo $this->_tpl_vars['admin_username']; ?>
" class="RightSide_links">
	Add New Permission to <b><?php echo ((is_array($_tmp=$this->_tpl_vars['admin_username'])) ? $this->_run_mod_handler('capitalize', true, $_tmp) : smarty_modifier_capitalize($_tmp)); ?>
</b>
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
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
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('setAboutPage', array('title' => 'Add New Permission')); $_block_repeat=true;smarty_block_setAboutPage($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_setAboutPage($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_footer.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>