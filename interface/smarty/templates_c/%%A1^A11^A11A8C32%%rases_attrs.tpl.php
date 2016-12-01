<?php /* Smarty version 2.6.13, created on 2006-06-13 19:23:20
         compiled from admin/report/connection_logs/conditions/rases_attrs.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'addEditTD', 'admin/report/connection_logs/conditions/rases_attrs.tpl', 1, false),array('function', 'rasCheckBoxes', 'admin/report/connection_logs/conditions/rases_attrs.tpl', 6, false),)), $this); ?>
<?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left','double' => 'TRUE','comment' => 'TRUE')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	Rases
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<td class="Form_Content_Row_right_Textarea_2col" valign="top" colspan="7">
	<?php echo smarty_function_rasCheckBoxes(array('prefix' => 'ras','add_show_hide_table' => 0), $this);?>
 
</td></tr>

<tr>
	<td colspan="9" class="Form_Content_Row_Space"></td>
</tr>