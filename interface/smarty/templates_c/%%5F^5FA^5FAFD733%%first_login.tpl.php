<?php /* Smarty version 2.6.13, created on 2006-06-17 13:10:52
         compiled from plugins/search/first_login.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'addEditTD', 'plugins/search/first_login.tpl', 1, false),array('function', 'op', 'plugins/search/first_login.tpl', 5, false),array('function', 'absDateSelect', 'plugins/search/first_login.tpl', 6, false),)), $this); ?>
<?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    First Login
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  $this->_tag_stack[] = array('addEditTD', array('type' => 'right')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <?php echo smarty_function_op(array('class' => 'ltgteq','name' => 'first_login_op','selected' => 'first_login_op'), $this);?>

    <?php echo smarty_function_absDateSelect(array('name' => 'first_login','default_request' => 'first_login'), $this);?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>