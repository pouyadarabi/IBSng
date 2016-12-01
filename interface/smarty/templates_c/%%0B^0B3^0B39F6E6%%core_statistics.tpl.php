<?php /* Smarty version 2.6.13, created on 2006-06-17 13:09:32
         compiled from admin/misc/core_statistics.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'viewTable', 'admin/misc/core_statistics.tpl', 5, false),array('block', 'addEditTD', 'admin/misc/core_statistics.tpl', 9, false),array('block', 'addRelatedLink', 'admin/misc/core_statistics.tpl', 30, false),array('block', 'setAboutPage', 'admin/misc/core_statistics.tpl', 36, false),array('modifier', 'replace', 'admin/misc/core_statistics.tpl', 10, false),array('modifier', 'capitalize', 'admin/misc/core_statistics.tpl', 10, false),array('modifier', 'price', 'admin/misc/core_statistics.tpl', 14, false),array('modifier', 'duration', 'admin/misc/core_statistics.tpl', 16, false),array('modifier', 'byte', 'admin/misc/core_statistics.tpl', 18, false),)), $this); ?>
<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_header.tpl", 'smarty_include_vars' => array('title' => 'Core Statistics','selected' => 'Core Statistics')));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
  $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "err_head.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>


<?php $this->_tag_stack[] = array('viewTable', array('title' => 'Statistics')); $_block_repeat=true;smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>

    <?php $_from = $this->_tpl_vars['stats']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['stat']):
?>

	<?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    	<?php echo ((is_array($_tmp=((is_array($_tmp=$this->_tpl_vars['stat'][0])) ? $this->_run_mod_handler('replace', true, $_tmp, '_', ' ') : smarty_modifier_replace($_tmp, '_', ' ')))) ? $this->_run_mod_handler('capitalize', true, $_tmp) : smarty_modifier_capitalize($_tmp)); ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $this->_tag_stack[] = array('addEditTD', array('type' => 'right')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php if ($this->_tpl_vars['stat'][1][1] == 'int'): ?>
		    <?php echo ((is_array($_tmp=$this->_tpl_vars['stat'][1][0])) ? $this->_run_mod_handler('price', true, $_tmp) : smarty_modifier_price($_tmp)); ?>

		<?php elseif ($this->_tpl_vars['stat'][1][1] == 'seconds'): ?>
		    <?php echo ((is_array($_tmp=$this->_tpl_vars['stat'][1][0])) ? $this->_run_mod_handler('duration', true, $_tmp) : smarty_modifier_duration($_tmp)); ?>

		<?php elseif ($this->_tpl_vars['stat'][1][1] == 'bytes'): ?>
		    <?php echo ((is_array($_tmp=$this->_tpl_vars['stat'][1][0])) ? $this->_run_mod_handler('byte', true, $_tmp) : smarty_modifier_byte($_tmp)); ?>

		<?php else: ?>
		    <?php echo $this->_tpl_vars['stat'][1][0]; ?>

		<?php endif; ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>    


    <?php endforeach; endif; unset($_from); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/misc/show_ibs_defs.php" class="RightSide_links">
	Advanced Configuration	
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('setAboutPage', array('title' => 'Core Statistics')); $_block_repeat=true;smarty_block_setAboutPage($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_setAboutPage($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_footer.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>