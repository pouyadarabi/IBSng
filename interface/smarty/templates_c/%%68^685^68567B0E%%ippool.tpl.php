<?php /* Smarty version 2.6.13, created on 2006-06-14 19:25:02
         compiled from plugins/user/view/ippool.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'userInfoTable', 'plugins/user/view/ippool.tpl', 1, false),array('block', 'userInfoTD', 'plugins/user/view/ippool.tpl', 2, false),array('block', 'ifHasAttr', 'plugins/user/view/ippool.tpl', 7, false),array('function', 'editCheckBox', 'plugins/user/view/ippool.tpl', 3, false),array('function', 'helpicon', 'plugins/user/view/ippool.tpl', 15, false),array('modifier', 'replace', 'plugins/user/view/ippool.tpl', 24, false),)), $this); ?>
<?php $this->_tag_stack[] = array('userInfoTable', array('title' => 'IPpool','nofoot' => 'TRUE')); $_block_repeat=true;smarty_block_userInfoTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_left')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
        <?php if ($this->_tpl_vars['can_change']):  echo smarty_function_editCheckBox(array('edit_tpl_name' => 'ippool'), $this); endif; ?>
        IPpool
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_right')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'user','var_name' => 'ippool')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['user_attrs']['ippool']; ?>
  
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'group')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'group','var_name' => 'ippool')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['group_attrs']['ippool']; ?>
  
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
	<?php echo smarty_function_helpicon(array('subject' => 'ippool','category' => 'user'), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_left')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
        <?php if ($this->_tpl_vars['can_change']):  echo smarty_function_editCheckBox(array('edit_tpl_name' => 'assign_ip'), $this); endif; ?>
        Assign IP Address To User
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_right')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'user','var_name' => 'assign_ip')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo ((is_array($_tmp=$this->_tpl_vars['user_attrs']['assign_ip'])) ? $this->_run_mod_handler('replace', true, $_tmp, ",", "<br>") : smarty_modifier_replace($_tmp, ",", "<br>")); ?>
  
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'group')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'group','var_name' => 'assign_ip')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo ((is_array($_tmp=$this->_tpl_vars['group_attrs']['assign_ip'])) ? $this->_run_mod_handler('replace', true, $_tmp, ",", "<br>") : smarty_modifier_replace($_tmp, ",", "<br>")); ?>
  
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
	<?php echo smarty_function_helpicon(array('subject' => 'ippool','category' => 'user'), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>