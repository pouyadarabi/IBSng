<?php /* Smarty version 2.6.13, created on 2006-06-14 19:25:09
         compiled from plugins/user/edit/skelton.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'headerMsg', 'plugins/user/edit/skelton.tpl', 8, false),array('block', 'attrTableFoot', 'plugins/user/edit/skelton.tpl', 31, false),array('block', 'addRelatedLink', 'plugins/user/edit/skelton.tpl', 35, false),array('block', 'setAboutPage', 'plugins/user/edit/skelton.tpl', 47, false),array('modifier', 'escape', 'plugins/user/edit/skelton.tpl', 36, false),array('modifier', 'truncate', 'plugins/user/edit/skelton.tpl', 37, false),)), $this); ?>
<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_header.tpl", 'smarty_include_vars' => array('title' => 'Edit User Attributes','selected' => 'User Information')));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
  $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "err_head.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>

<?php if (! $this->_tpl_vars['single_user']):  $this->_tag_stack[] = array('headerMsg', array()); $_block_repeat=true;smarty_block_headerMsg($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    Warning: When editing multiple users, user default values and group values are always empty
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_headerMsg($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>    
<?php endif; ?>

<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin/user/user_pages_user_id_header.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>
<br>

<table width=380><tr><td>
<form method=POST action="/IBSng/admin/plugins/edit.php" name="user_edit" enctype="multipart/form-data">

    <input type=hidden name="target" value="user">
    <input type=hidden name="target_id" value="<?php echo $this->_tpl_vars['user_id']; ?>
">
    <input type=hidden name="update" value="1">
    <input type=hidden name="edit_tpl_cs" value="<?php echo $this->_tpl_vars['edit_tpl_cs']; ?>
">
    <?php if (isInRequest ( 'tab1_selected' )): ?>
	<input type=hidden name="tab1_selected" value="<?php echo $_REQUEST['tab1_selected']; ?>
">
    <?php endif;  $_from = $this->_tpl_vars['edit_tpl_files']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['tpl_file']):
?>
    <?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => $this->_tpl_vars['tpl_file'], 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>    
<?php endforeach; endif; unset($_from); ?>
</td></tr></table>

<?php $this->_tag_stack[] = array('attrTableFoot', array('action_icon' => 'ok','cancel_icon' => 'TRUE')); $_block_repeat=true;smarty_block_attrTableFoot($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start();  $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_attrTableFoot($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
</form>

<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/user/user_info.php?user_id_multi=<?php echo ((is_array($_tmp=$this->_tpl_vars['user_id'])) ? $this->_run_mod_handler('escape', true, $_tmp, 'url') : smarty_modifier_escape($_tmp, 'url')); ?>
" class="RightSide_links">
	User <b><?php echo ((is_array($_tmp=$this->_tpl_vars['user_id'])) ? $this->_run_mod_handler('truncate', true, $_tmp, 15) : smarty_modifier_truncate($_tmp, 15)); ?>
</b> Info
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/group/group_list.php" class="RightSide_links">
	Group List
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('setAboutPage', array('title' => 'User Info')); $_block_repeat=true;smarty_block_setAboutPage($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    You can edit attributes of users that you have selected.
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_setAboutPage($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_footer.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>