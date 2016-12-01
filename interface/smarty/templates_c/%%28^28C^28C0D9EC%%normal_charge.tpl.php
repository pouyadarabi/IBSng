<?php /* Smarty version 2.6.13, created on 2006-07-12 14:39:50
         compiled from plugins/group/view/normal_charge.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'viewTable', 'plugins/group/view/normal_charge.tpl', 1, false),array('block', 'addEditTD', 'plugins/group/view/normal_charge.tpl', 2, false),array('block', 'ifHasAttr', 'plugins/group/view/normal_charge.tpl', 9, false),array('function', 'editCheckBox', 'plugins/group/view/normal_charge.tpl', 4, false),array('function', 'helpicon', 'plugins/group/view/normal_charge.tpl', 14, false),array('modifier', 'escape', 'plugins/group/view/normal_charge.tpl', 10, false),)), $this); ?>
<?php $this->_tag_stack[] = array('viewTable', array('title' => 'Internet Charge','nofoot' => 'TRUE')); $_block_repeat=true;smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php echo '';  if ($this->_tpl_vars['can_change']):  echo '';  echo smarty_function_editCheckBox(array('edit_tpl_name' => 'normal_charge'), $this); echo '';  endif;  echo 'Internet Charge'; ?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'right')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'group','var_name' => 'normal_charge')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <a class="link_in_body_black" href="/IBSng/admin/charge/charge_info.php?charge_name=<?php echo ((is_array($_tmp=$this->_tpl_vars['group_attrs']['normal_charge'])) ? $this->_run_mod_handler('escape', true, $_tmp, 'url') : smarty_modifier_escape($_tmp, 'url')); ?>
">
			<?php echo $this->_tpl_vars['group_attrs']['normal_charge']; ?>
  
		    </a>
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
		<?php echo smarty_function_helpicon(array('subject' => 'normal charge','category' => 'user'), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>