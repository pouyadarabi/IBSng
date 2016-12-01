<?php /* Smarty version 2.6.13, created on 2006-07-18 14:42:24
         compiled from admin/user/search_user/user_list.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'listTable', 'admin/user/search_user/user_list.tpl', 5, false),array('block', 'listTableHeader', 'admin/user/search_user/user_list.tpl', 6, false),array('block', 'listTR', 'admin/user/search_user/user_list.tpl', 12, false),array('block', 'listTD', 'admin/user/search_user/user_list.tpl', 14, false),array('function', 'eval', 'admin/user/search_user/user_list.tpl', 22, false),)), $this); ?>
<script language="javascript">
    var user_ids=new CheckBoxContainer();
</script>

<?php $this->_tag_stack[] = array('listTable', array('no_header' => 'TRUE')); $_block_repeat=true;smarty_block_listTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
    <?php $this->_tag_stack[] = array('listTableHeader', array('cols_num' => 30,'type' => 'left')); $_block_repeat=true;smarty_block_listTableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	List of Users
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('listTableHeader', array('type' => 'right')); $_block_repeat=true;smarty_block_listTableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	Total Results:  <font color="#9a1111"><?php echo $this->_tpl_vars['result_count']; ?>
</font> 
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('listTR', array('type' => 'header')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    	<?php if ($this->_tpl_vars['can_change']): ?>
			<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    	<input type=checkbox name="check_all_users"> 
		    	<script language="javascript">
					user_ids.setCheckAll("edit_user","check_all_users");
		    	</script>
			<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    	<?php endif; ?>
    	
	<?php echo smarty_function_eval(array('var' => $this->_tpl_vars['generated_tpl_header']), $this);?>


    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $_from = $this->_tpl_vars['reports']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['row']):
?>

	<?php $this->assign('user_id', ($this->_tpl_vars['row']['report_root']['user_id'])); ?>
	<?php $this->_tag_stack[] = array('listTR', array('type' => 'body','cycle_color' => 'TRUE','hover_location' => "/IBSng/admin/user/user_info.php?user_id=".($this->_tpl_vars['user_id']))); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php if ($this->_tpl_vars['can_change']): ?>
			<?php $this->_tag_stack[] = array('listTD', array('extra' => "onClick='event.cancelBubble=true;'")); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    		<input type=checkbox name="edit_user_id_<?php echo $this->_tpl_vars['user_id']; ?>
" value="<?php echo $this->_tpl_vars['user_id']; ?>
"> 
		    	<script language="javascript">
					user_ids.addByName("edit_user","edit_user_id_<?php echo $this->_tpl_vars['user_id']; ?>
");
		    	</script>
        	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>	
	    <?php endif; ?>
	    <?php echo smarty_function_eval(array('var' => $this->_tpl_vars['generated_tpl_body']), $this);?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  endforeach; endif; unset($_from); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>