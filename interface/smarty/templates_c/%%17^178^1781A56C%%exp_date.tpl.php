<?php /* Smarty version 2.6.13, created on 2006-06-14 19:25:01
         compiled from plugins/user/view/exp_date.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'userInfoTable', 'plugins/user/view/exp_date.tpl', 1, false),array('block', 'userInfoTD', 'plugins/user/view/exp_date.tpl', 2, false),array('block', 'ifHasAttr', 'plugins/user/view/exp_date.tpl', 7, false),array('function', 'editCheckBox', 'plugins/user/view/exp_date.tpl', 3, false),array('function', 'helpicon', 'plugins/user/view/exp_date.tpl', 16, false),)), $this); ?>
<?php $this->_tag_stack[] = array('userInfoTable', array('title' => 'User Expiration Date','nofoot' => 'TRUE')); $_block_repeat=true;smarty_block_userInfoTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_left')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php if ($this->_tpl_vars['can_change']):  echo smarty_function_editCheckBox(array('edit_tpl_name' => 'rel_exp_date'), $this); endif; ?>Relative Expiration Date:
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_right')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('var_name' => 'rel_exp_date','object' => 'user')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['user_attrs']['rel_exp_date']; ?>
 <?php echo $this->_tpl_vars['user_attrs']['rel_exp_date_unit']; ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'group')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('var_name' => 'rel_exp_date','object' => 'group')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['group_attrs']['rel_exp_date']; ?>
 <?php echo $this->_tpl_vars['group_attrs']['rel_exp_date_unit']; ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php echo smarty_function_helpicon(array('subject' => 'absolute expiration date','category' => 'user'), $this);?>
		    
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_left')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php if ($this->_tpl_vars['can_change']):  echo smarty_function_editCheckBox(array('edit_tpl_name' => 'abs_exp_date'), $this); endif; ?>Absolute Expiration Date:
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_right')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('var_name' => 'abs_exp_date','object' => 'user')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['user_attrs']['abs_exp_date']; ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'group')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('var_name' => 'abs_exp_date','object' => 'group')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['group_attrs']['abs_exp_date']; ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php echo smarty_function_helpicon(array('subject' => 'absolute expiration date','category' => 'user'), $this);?>
		    
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_left')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php if ($this->_tpl_vars['can_change']):  echo smarty_function_editCheckBox(array('edit_tpl_name' => 'first_login'), $this); endif; ?>First Login:
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_right')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('var_name' => 'first_login','object' => 'user')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['user_attrs']['first_login']; ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'group')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	N/A
	<?php echo smarty_function_helpicon(array('subject' => 'first login','category' => 'user'), $this);?>
		    
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_left')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	Nearest Expiration Date:
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_right')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('var_name' => 'nearest_exp_date','object' => 'user')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['user_attrs']['nearest_exp_date']; ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'group')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	N/A
	<?php echo smarty_function_helpicon(array('subject' => 'nearest expiration date','category' => 'user'), $this);?>
		    
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


    
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>