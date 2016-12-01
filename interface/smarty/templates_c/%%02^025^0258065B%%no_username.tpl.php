<?php /* Smarty version 2.6.13, created on 2006-06-17 13:10:52
         compiled from plugins/search/no_username.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'multiTable', 'plugins/search/no_username.tpl', 5, false),array('block', 'multiTableTD', 'plugins/search/no_username.tpl', 8, false),array('function', 'multiTableTR', 'plugins/search/no_username.tpl', 6, false),array('function', 'checkBoxValue', 'plugins/search/no_username.tpl', 13, false),)), $this); ?>

<tr>
<td colspan=20>

<?php $this->_tag_stack[] = array('multiTable', array()); $_block_repeat=true;smarty_block_multiTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <?php echo smarty_function_multiTableTR(array(), $this);?>


    <?php $this->_tag_stack[] = array('multiTableTD', array('type' => 'left')); $_block_repeat=true;smarty_block_multiTableTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<span style="color: black; font-weight: normal">Don't have Internet Username:</span>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_multiTableTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('multiTableTD', array('type' => 'right')); $_block_repeat=true;smarty_block_multiTableTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
        <input type=checkbox name=no_normal_username value=t <?php echo smarty_function_checkBoxValue(array('name' => 'no_normal_username'), $this);?>
>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_multiTableTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('multiTableTD', array('type' => 'left')); $_block_repeat=true;smarty_block_multiTableTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<span style="color: black; font-weight: normal">Don't have VoIP Username:</span>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_multiTableTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('multiTableTD', array('type' => 'right')); $_block_repeat=true;smarty_block_multiTableTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<input type=checkbox name=no_voip_username value=t <?php echo smarty_function_checkBoxValue(array('name' => 'no_voip_username'), $this);?>
>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_multiTableTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_multiTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

</td>