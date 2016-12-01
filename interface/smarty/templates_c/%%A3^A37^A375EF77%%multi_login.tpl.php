<?php /* Smarty version 2.6.13, created on 2006-07-12 14:39:50
         compiled from plugins/group/view/multi_login.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'viewTable', 'plugins/group/view/multi_login.tpl', 1, false),array('block', 'addEditTD', 'plugins/group/view/multi_login.tpl', 2, false),array('block', 'ifHasAttr', 'plugins/group/view/multi_login.tpl', 9, false),array('function', 'editCheckBox', 'plugins/group/view/multi_login.tpl', 4, false),array('function', 'helpicon', 'plugins/group/view/multi_login.tpl', 12, false),)), $this); ?>
<?php $this->_tag_stack[] = array('viewTable', array('title' => 'Multi Login','nofoot' => 'TRUE')); $_block_repeat=true;smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php echo '';  if ($this->_tpl_vars['can_change']):  echo ' ';  echo smarty_function_editCheckBox(array('edit_tpl_name' => 'multi_login'), $this); echo ' ';  endif;  echo 'Multi Login'; ?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'right')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'group','var_name' => 'multi_login')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <?php echo $this->_tpl_vars['group_attrs']['multi_login']; ?>
 instances 
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
		<?php echo smarty_function_helpicon(array('subject' => 'multi login','category' => 'user'), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
