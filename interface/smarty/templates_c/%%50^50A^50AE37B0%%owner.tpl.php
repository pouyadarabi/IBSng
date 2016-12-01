<?php /* Smarty version 2.6.13, created on 2006-06-17 13:10:52
         compiled from plugins/search/owner.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('function', 'multiTableTR', 'plugins/search/owner.tpl', 4, false),array('function', 'counter', 'plugins/search/owner.tpl', 10, false),array('function', 'ifisinrequest', 'plugins/search/owner.tpl', 11, false),array('function', 'multiTablePad', 'plugins/search/owner.tpl', 19, false),array('block', 'multiTableTD', 'plugins/search/owner.tpl', 9, false),)), $this); ?>
<?php if (amIGod ( ) || permValueRestricted ( 'CHANGE_USER_OWNER' , getAuthUsername ( ) )):  $_from = $this->_tpl_vars['admin_names']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['index'] => $this->_tpl_vars['owner_name']):
?>
    <?php if ($this->_tpl_vars['index'] == 0): ?>
        <?php echo smarty_function_multiTableTR(array(), $this);?>

    <?php elseif ($this->_tpl_vars['index']%4 == 0): ?>
        <?php echo smarty_function_multiTableTR(array('begin_close_tr' => 'TRUE'), $this);?>

    <?php endif; ?>

    <?php $this->_tag_stack[] = array('multiTableTD', array('type' => 'left')); $_block_repeat=true;smarty_block_multiTableTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <?php echo smarty_function_counter(array('name' => 'owner_search_id','assign' => 'owner_search_id'), $this);?>

	<input name="owner_name_<?php echo $this->_tpl_vars['owner_search_id']; ?>
" value="<?php echo $this->_tpl_vars['owner_name']; ?>
" type=checkbox <?php echo smarty_function_ifisinrequest(array('name' => "owner_name_".($this->_tpl_vars['owner_search_id']),'value' => 'checked'), $this);?>
>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_multiTableTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>	
    <?php $this->_tag_stack[] = array('multiTableTD', array('type' => 'right','width' => "25%")); $_block_repeat=true;smarty_block_multiTableTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
         <?php echo $this->_tpl_vars['owner_name']; ?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_multiTableTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  endforeach; endif; unset($_from); ?>

<?php endif;  echo smarty_function_multiTablePad(array('last_index' => $this->_tpl_vars['index'],'go_until' => 3,'width' => "25%"), $this);?>

</tr><tr><td colspan=30 height=1 bgcolor="#FFFFFF"></td></tr>