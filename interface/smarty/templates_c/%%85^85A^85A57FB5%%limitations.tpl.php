<?php /* Smarty version 2.6.13, created on 2006-06-14 19:25:02
         compiled from plugins/user/view/limitations.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'userInfoTable', 'plugins/user/view/limitations.tpl', 1, false),array('block', 'userInfoTD', 'plugins/user/view/limitations.tpl', 2, false),array('block', 'ifHasAttr', 'plugins/user/view/limitations.tpl', 7, false),array('function', 'editCheckBox', 'plugins/user/view/limitations.tpl', 3, false),array('function', 'helpicon', 'plugins/user/view/limitations.tpl', 15, false),array('modifier', 'replace', 'plugins/user/view/limitations.tpl', 40, false),)), $this); ?>
<?php $this->_tag_stack[] = array('userInfoTable', array('title' => 'Limitations','nofoot' => 'TRUE')); $_block_repeat=true;smarty_block_userInfoTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_left')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
        <?php if ($this->_tpl_vars['can_change']):  echo smarty_function_editCheckBox(array('edit_tpl_name' => 'session_timeout'), $this); endif; ?>
        Session Timeout
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_right')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'user','var_name' => 'session_timeout')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['user_attrs']['session_timeout']; ?>
 Seconds
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'group')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'group','var_name' => 'session_timeout')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['group_attrs']['session_timeout']; ?>
 Seconds
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
	<?php echo smarty_function_helpicon(array('subject' => 'session timeout','category' => 'user'), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_left')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
        <?php if ($this->_tpl_vars['can_change']):  echo smarty_function_editCheckBox(array('edit_tpl_name' => 'idle_timeout'), $this); endif; ?>
        Idle Timeout
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_right')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'user','var_name' => 'idle_timeout')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['user_attrs']['idle_timeout']; ?>
 Seconds
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'group')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'group','var_name' => 'idle_timeout')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['group_attrs']['idle_timeout']; ?>
 Seconds
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
	<?php echo smarty_function_helpicon(array('subject' => 'idle timeout','category' => 'user'), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
 
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_left','comment' => 'TRUE')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
        <?php if ($this->_tpl_vars['can_change']):  echo smarty_function_editCheckBox(array('edit_tpl_name' => 'limit_mac'), $this); endif; ?>
        Limit Mac Address
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_right','comment' => 'TRUE')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'user','var_name' => 'limit_mac')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo ((is_array($_tmp=$this->_tpl_vars['user_attrs']['limit_mac'])) ? $this->_run_mod_handler('replace', true, $_tmp, ",", "<br>") : smarty_modifier_replace($_tmp, ",", "<br>")); ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'group','comment' => 'TRUE')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'group','var_name' => 'limit_mac')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo ((is_array($_tmp=$this->_tpl_vars['group_attrs']['limit_mac'])) ? $this->_run_mod_handler('replace', true, $_tmp, ",", "<br>") : smarty_modifier_replace($_tmp, ",", "<br>")); ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
	<?php echo smarty_function_helpicon(array('subject' => 'Limit Mac Address','category' => 'user'), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_left','comment' => 'TRUE')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
        <?php if ($this->_tpl_vars['can_change']):  echo smarty_function_editCheckBox(array('edit_tpl_name' => 'limit_station_ip'), $this); endif; ?>
        Limit Station IP
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_right','comment' => 'TRUE')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'user','var_name' => 'limit_station_ip')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo ((is_array($_tmp=$this->_tpl_vars['user_attrs']['limit_station_ip'])) ? $this->_run_mod_handler('replace', true, $_tmp, ",", "<br>") : smarty_modifier_replace($_tmp, ",", "<br>")); ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'group','comment' => 'TRUE')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'group','var_name' => 'limit_station_ip')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo ((is_array($_tmp=$this->_tpl_vars['group_attrs']['limit_station_ip'])) ? $this->_run_mod_handler('replace', true, $_tmp, ",", "<br>") : smarty_modifier_replace($_tmp, ",", "<br>")); ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
	<?php echo smarty_function_helpicon(array('subject' => 'Limit Station IP Address','category' => 'user'), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>



    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_left','comment' => 'TRUE')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
        <?php if ($this->_tpl_vars['can_change']):  echo smarty_function_editCheckBox(array('edit_tpl_name' => 'limit_caller_id'), $this); endif; ?>
        Limit Caller ID
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_right','comment' => 'TRUE')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'user','var_name' => 'limit_caller_id')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo ((is_array($_tmp=$this->_tpl_vars['user_attrs']['limit_caller_id'])) ? $this->_run_mod_handler('replace', true, $_tmp, ",", "<br>") : smarty_modifier_replace($_tmp, ",", "<br>")); ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'group','comment' => 'TRUE')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'group','var_name' => 'limit_caller_id')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo ((is_array($_tmp=$this->_tpl_vars['group_attrs']['limit_caller_id'])) ? $this->_run_mod_handler('replace', true, $_tmp, ",", "<br>") : smarty_modifier_replace($_tmp, ",", "<br>")); ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
	<?php echo smarty_function_helpicon(array('subject' => 'Limit Caller ID','category' => 'user'), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_left')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
        Allow user without Caller ID
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_right')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'user','var_name' => 'limit_caller_id_allow_not_defined')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php if ($this->_tpl_vars['user_attrs']['limit_caller_id_allow_not_defined'] == FALSE): ?>
		No
	    <?php else: ?>
		Yes
	    <?php endif; ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'group')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('object' => 'group','var_name' => 'limit_caller_id_allow_not_defined')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php if ($this->_tpl_vars['group_attrs']['limit_caller_id_allow_not_defined'] == FALSE): ?>
		No
	    <?php else: ?>
		Yes
	    <?php endif; ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
	<?php echo smarty_function_helpicon(array('subject' => 'Allow users without caller id','category' => 'user'), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>