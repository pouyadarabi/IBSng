<?php /* Smarty version 2.6.13, created on 2006-06-17 13:10:52
         compiled from plugins/search/limit_station_ip.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'addEditTD', 'plugins/search/limit_station_ip.tpl', 1, false),array('function', 'op', 'plugins/search/limit_station_ip.tpl', 5, false),array('function', 'ifisinrequest', 'plugins/search/limit_station_ip.tpl', 6, false),array('function', 'multistr', 'plugins/search/limit_station_ip.tpl', 7, false),)), $this); ?>
<?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    Limit Station IP
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  $this->_tag_stack[] = array('addEditTD', array('type' => 'right')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <?php echo smarty_function_op(array('class' => 'likestr','name' => 'limit_station_ip_op','selected' => 'limit_station_ip_op'), $this);?>

    <input type=text class=text name="limit_station_ip" value="<?php echo smarty_function_ifisinrequest(array('name' => 'limit_station_ip'), $this);?>
">
    <?php echo smarty_function_multistr(array('form_name' => 'search_user','input_name' => 'limit_station_ip'), $this);?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

