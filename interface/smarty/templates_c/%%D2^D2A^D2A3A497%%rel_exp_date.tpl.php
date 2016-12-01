<?php /* Smarty version 2.6.13, created on 2006-07-19 12:12:10
         compiled from plugins/user/edit/rel_exp_date.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('function', 'attrUpdateMethod', 'plugins/user/edit/rel_exp_date.tpl', 1, false),array('function', 'attrDefault', 'plugins/user/edit/rel_exp_date.tpl', 21, false),array('function', 'relative_units', 'plugins/user/edit/rel_exp_date.tpl', 22, false),array('block', 'userInfoTable', 'plugins/user/edit/rel_exp_date.tpl', 2, false),array('block', 'userInfoTD', 'plugins/user/edit/rel_exp_date.tpl', 3, false),array('block', 'ifHasAttr', 'plugins/user/edit/rel_exp_date.tpl', 10, false),)), $this); ?>
<?php echo smarty_function_attrUpdateMethod(array('update_method' => 'relExpDate'), $this);?>

<?php $this->_tag_stack[] = array('userInfoTable', array('title' => 'User Expiration Date','nofoot' => 'TRUE')); $_block_repeat=true;smarty_block_userInfoTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_left')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	Has Reletaive Expiration Date
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_right')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<input type=checkbox name="has_rel_exp" value="t" class=checkbox <?php if (attrDefault ( $this->_tpl_vars['user_attrs'] , 'rel_exp_date' , 'has_rel_exp' ) != ""): ?>checked<?php endif; ?> onClick='rel_exp_select.toggle("rel_exp_date")'>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'group')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('var_name' => 'rel_exp_date','object' => 'group','alternate' => 'No')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    Yes
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_left')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	Relative Expiration Date:
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'user_right')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<input id="rel_exp_date" type=text class=small_text name="rel_exp_date" value="<?php echo smarty_function_attrDefault(array('default_request' => 'rel_exp_date','default_var' => 'rel_exp_date','target' => 'user'), $this);?>
">
	<?php echo smarty_function_relative_units(array('id' => 'rel_exp_date_unit','name' => 'rel_exp_date_unit','default_var' => 'rel_exp_date_unit','default_request' => 'rel_exp_date_unit','target' => 'user'), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('userInfoTD', array('type' => 'group')); $_block_repeat=true;smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('ifHasAttr', array('var_name' => 'rel_exp_date','object' => 'group')); $_block_repeat=true;smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['group_attrs']['rel_exp_date']; ?>
 <?php echo $this->_tpl_vars['group_attrs']['rel_exp_date_unit']; ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_userInfoTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
<br>
<script language="javascript">
	rel_exp_select=new DomContainer();
	rel_exp_select.disable_unselected=true;
	rel_exp_select.addByID("rel_exp_date",Array("rel_exp_date_unit"));
<?php if (attrDefault ( $this->_tpl_vars['user_attrs'] , 'rel_exp_date' , 'has_rel_exp' ) != ""): ?>
    rel_exp_select.select("rel_exp_date");
<?php else: ?>
    rel_exp_select.select(null);
<?php endif; ?>
</script>