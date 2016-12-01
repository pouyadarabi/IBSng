<?php /* Smarty version 2.6.13, created on 2006-06-14 19:25:01
         compiled from plugins/user/view/fast_dial.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'viewTable', 'plugins/user/view/fast_dial.tpl', 1, false),array('block', 'addEditTD', 'plugins/user/view/fast_dial.tpl', 2, false),array('block', 'ifHasAttr', 'plugins/user/view/fast_dial.tpl', 9, false),array('function', 'editCheckBox', 'plugins/user/view/fast_dial.tpl', 4, false),array('function', 'helpicon', 'plugins/user/view/fast_dial.tpl', 14, false),)), $this); ?>
<?php $this->_tag_stack[] = array('viewTable', array('title' => 'Fast Dial','nofoot' => 'TRUE','table_width' => "100%")); $_block_repeat=true;smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left','comment' => 'TRUE')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php echo '';  if ($this->_tpl_vars['can_change']):  echo ' ';  echo smarty_function_editCheckBox(array('edit_tpl_name' => 'fast_dial'), $this); echo ' ';  endif;  echo 'Fast Dial'; ?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'right','comment' => 'TRUE')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'user','var_name' => 'fast_dial')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <?php $_from = $this->_tpl_vars['user_attrs']['fast_dial']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['index'] => $this->_tpl_vars['fast_dial']):
?>
			<?php echo $this->_tpl_vars['index']; ?>
 -> <?php echo $this->_tpl_vars['user_attrs']['fast_dial'][$this->_tpl_vars['index']]; ?>
 <br />
		    <?php endforeach; endif; unset($_from); ?>
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
		<?php echo smarty_function_helpicon(array('subject' => 'fast dial','category' => 'user'), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
