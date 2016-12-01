<?php /* Smarty version 2.6.13, created on 2006-06-14 19:25:09
         compiled from admin/user/user_pages_user_id_header.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'viewTable', 'admin/user/user_pages_user_id_header.tpl', 1, false),array('block', 'addEditTD', 'admin/user/user_pages_user_id_header.tpl', 3, false),array('modifier', 'replace', 'admin/user/user_pages_user_id_header.tpl', 8, false),array('function', 'multistr', 'admin/user/user_pages_user_id_header.tpl', 8, false),)), $this); ?>
<?php $this->_tag_stack[] = array('viewTable', array('title' => 'User  Information','table_width' => '380','nofoot' => 'TRUE')); $_block_repeat=true;smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>

    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left','comment' => 'TRUE')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	User ID
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'right','comment' => 'TRUE')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
      <form name="user_id_header">
	<?php echo ((is_array($_tmp=$this->_tpl_vars['user_id'])) ? $this->_run_mod_handler('replace', true, $_tmp, ",", ", ") : smarty_modifier_replace($_tmp, ",", ", ")); ?>
 <?php echo smarty_function_multistr(array('form_name' => 'user_id_header','input_name' => 'user_id'), $this);?>

	<input type=hidden name="user_id" value="<?php echo $this->_tpl_vars['user_id']; ?>
">
      </form>
	
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>