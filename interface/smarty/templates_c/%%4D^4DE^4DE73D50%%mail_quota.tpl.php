<?php /* Smarty version 2.6.13, created on 2006-07-12 14:39:50
         compiled from plugins/group/view/mail_quota.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'viewTable', 'plugins/group/view/mail_quota.tpl', 1, false),array('block', 'addEditTD', 'plugins/group/view/mail_quota.tpl', 2, false),array('block', 'ifHasAttr', 'plugins/group/view/mail_quota.tpl', 6, false),array('function', 'editCheckBox', 'plugins/group/view/mail_quota.tpl', 3, false),array('function', 'helpicon', 'plugins/group/view/mail_quota.tpl', 9, false),array('modifier', 'byte', 'plugins/group/view/mail_quota.tpl', 7, false),)), $this); ?>
<?php $this->_tag_stack[] = array('viewTable', array('title' => 'Mailbox','nofoot' => 'TRUE')); $_block_repeat=true;smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php if ($this->_tpl_vars['can_change']):  echo smarty_function_editCheckBox(array('edit_tpl_name' => 'mail_quota'), $this); endif; ?> Mailbox Quota
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'right')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'group','var_name' => 'mail_quota')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo ((is_array($_tmp=$this->_tpl_vars['group_attrs']['mail_quota'])) ? $this->_run_mod_handler('byte', true, $_tmp) : smarty_modifier_byte($_tmp)); ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
	<?php echo smarty_function_helpicon(array('subject' => 'has mailbox','category' => 'user'), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>