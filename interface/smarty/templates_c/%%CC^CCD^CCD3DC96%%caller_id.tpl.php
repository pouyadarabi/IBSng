<?php /* Smarty version 2.6.13, created on 2006-06-14 19:25:01
         compiled from plugins/user/view/caller_id.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'viewTable', 'plugins/user/view/caller_id.tpl', 1, false),array('block', 'addEditTD', 'plugins/user/view/caller_id.tpl', 2, false),array('block', 'ifHasAttr', 'plugins/user/view/caller_id.tpl', 10, false),array('function', 'editCheckBox', 'plugins/user/view/caller_id.tpl', 4, false),array('function', 'multistr', 'plugins/user/view/caller_id.tpl', 13, false),array('function', 'helpicon', 'plugins/user/view/caller_id.tpl', 15, false),)), $this); ?>
<?php $this->_tag_stack[] = array('viewTable', array('title' => 'Caller ID','table_width' => "100%",'nofoot' => 'TRUE')); $_block_repeat=true;smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php if ($this->_tpl_vars['can_change_voip']): ?>
	    <?php echo smarty_function_editCheckBox(array('edit_tpl_name' => 'caller_id'), $this);?>

	<?php endif; ?>
	VoIP Caller ID
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'right')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('var_name' => 'caller_id','object' => 'user')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['user_attrs']['caller_id']; ?>

	    <input type=hidden name=hidden_caller_id value="<?php echo $this->_tpl_vars['user_attrs']['caller_id']; ?>
">
	    <?php echo smarty_function_multistr(array('form_name' => 'user_info','input_name' => 'hidden_caller_id'), $this);?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php echo smarty_function_helpicon(array('subject' => 'caller id','category' => 'user'), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>