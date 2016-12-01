<?php /* Smarty version 2.6.13, created on 2006-06-13 19:23:20
         compiled from admin/report/connection_logs/conditions/skel_conditions.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'listTableHeader', 'admin/report/connection_logs/conditions/skel_conditions.tpl', 6, false),array('block', 'multiTable', 'admin/report/connection_logs/conditions/skel_conditions.tpl', 18, false),)), $this); ?>
<script language="javascript" src="/IBSng/js/check_box_container.js"></script>
<script language="javascript">
    <?php echo $this->_tpl_vars['name']; ?>
_selected = new CheckBoxContainer();
</script>

    <?php $this->_tag_stack[] = array('listTableHeader', array('cols_num' => 30,'type' => 'left')); $_block_repeat=true;smarty_block_listTableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php echo $this->_tpl_vars['title']; ?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('listTableHeader', array('type' => 'right')); $_block_repeat=true;smarty_block_listTableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<table cellpadding=0 cellspacing=0 border=0 class="List_Top_line" align="right">
	<tr>
	    <td><input style="height:11" type=checkbox name=<?php echo $this->_tpl_vars['name']; ?>
_check_all></td>
	    <td>Check All Attributes</td>	
	</tr>
	</table>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
        <tr><td colspan=30>
	<?php $this->_tag_stack[] = array('multiTable', array()); $_block_repeat=true;smarty_block_multiTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => $this->_tpl_vars['inc'], 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_multiTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	</td></tr>
<script language="javascript">
    <?php echo $this->_tpl_vars['name']; ?>
_selected.setCheckAll('<?php echo $this->_tpl_vars['form_name']; ?>
','<?php echo $this->_tpl_vars['name']; ?>
_check_all');
</script>