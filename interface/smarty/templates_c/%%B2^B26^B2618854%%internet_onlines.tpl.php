<?php /* Smarty version 2.6.13, created on 2006-07-02 18:01:42
         compiled from admin/report/internet_onlines.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'listTable', 'admin/report/internet_onlines.tpl', 1, false),array('block', 'listTR', 'admin/report/internet_onlines.tpl', 7, false),array('block', 'listTD', 'admin/report/internet_onlines.tpl', 8, false),array('block', 'sortableHeader', 'admin/report/internet_onlines.tpl', 13, false),array('block', 'reportDetailLayer', 'admin/report/internet_onlines.tpl', 176, false),array('block', 'layerTable', 'admin/report/internet_onlines.tpl', 177, false),array('block', 'layerTR', 'admin/report/internet_onlines.tpl', 179, false),array('function', 'listTableHeaderIcon', 'admin/report/internet_onlines.tpl', 2, false),array('function', 'math', 'admin/report/internet_onlines.tpl', 91, false),array('function', 'jsconfirm', 'admin/report/internet_onlines.tpl', 148, false),array('function', 'listTableBodyIcon', 'admin/report/internet_onlines.tpl', 149, false),array('modifier', 'duration', 'admin/report/internet_onlines.tpl', 110, false),array('modifier', 'price', 'admin/report/internet_onlines.tpl', 114, false),array('modifier', 'truncate', 'admin/report/internet_onlines.tpl', 123, false),array('modifier', 'byte', 'admin/report/internet_onlines.tpl', 127, false),)), $this); ?>
<?php $this->_tag_stack[] = array('listTable', array('title' => 'Internet Online Users','cols_num' => 13)); $_block_repeat=true;smarty_block_listTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <?php echo smarty_function_listTableHeaderIcon(array('action' => 'kick'), $this);?>

    <?php echo smarty_function_listTableHeaderIcon(array('action' => 'clear'), $this);?>

    <?php echo smarty_function_listTableHeaderIcon(array('action' => 'graph'), $this);?>

    <?php echo smarty_function_listTableHeaderIcon(array('action' => 'history'), $this);?>

    <?php echo smarty_function_listTableHeaderIcon(array('action' => 'details','close_tr' => 'TRUE'), $this);?>

    <?php $this->_tag_stack[] = array('listTR', array('type' => 'header')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    Row
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('sortableHeader', array('name' => 'user_id')); $_block_repeat=true;smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
		User ID
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('sortableHeader', array('name' => 'normal_username')); $_block_repeat=true;smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
		Username
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('sortableHeader', array('name' => 'login_time_epoch','default' => 'TRUE','default_desc' => 'TRUE')); $_block_repeat=true;smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		Login Time
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('sortableHeader', array('name' => 'duration_secs')); $_block_repeat=true;smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		Duration
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('sortableHeader', array('name' => 'current_credit')); $_block_repeat=true;smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
		Credit
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('sortableHeader', array('name' => 'ras_description')); $_block_repeat=true;smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
		Ras
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('sortableHeader', array('name' => 'unique_id_val')); $_block_repeat=true;smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
	        Port/ID
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('sortableHeader', array('name' => 'in_bytes')); $_block_repeat=true;smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
		In Bytes
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('sortableHeader', array('name' => 'out_bytes')); $_block_repeat=true;smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
		Out Bytes
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('sortableHeader', array('name' => 'in_rate')); $_block_repeat=true;smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
		In Rate
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('sortableHeader', array('name' => 'out_rate')); $_block_repeat=true;smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
		Out Rate
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('sortableHeader', array('name' => 'owner_name')); $_block_repeat=true;smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
		Owner
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_sortableHeader($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->assign('index', 1); ?>

    <?php $_from = $this->_tpl_vars['internet_onlines']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['info_dic']):
?>
	<?php $this->_tag_stack[] = array('listTR', array('type' => 'body','hover_location' => "/IBSng/admin/user/user_info.php?user_id=".($this->_tpl_vars['info_dic']['user_id']))); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>

	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php echo $this->_tpl_vars['index']; ?>

		<?php echo smarty_function_math(array('equation' => "index+1",'index' => $this->_tpl_vars['index'],'assign' => 'index'), $this);?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<a href="/IBSng/admin/user/user_info.php?user_id=<?php echo $this->_tpl_vars['info_dic']['user_id']; ?>
" class="link_in_body">
		    <?php echo $this->_tpl_vars['info_dic']['user_id']; ?>

		</a>
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php echo $this->_tpl_vars['info_dic']['normal_username']; ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php echo $this->_tpl_vars['info_dic']['login_time']; ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php echo ((is_array($_tmp=$this->_tpl_vars['info_dic']['duration_secs'])) ? $this->_run_mod_handler('duration', true, $_tmp) : smarty_modifier_duration($_tmp)); ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php echo ((is_array($_tmp=$this->_tpl_vars['info_dic']['current_credit'])) ? $this->_run_mod_handler('price', true, $_tmp) : smarty_modifier_price($_tmp)); ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php echo $this->_tpl_vars['info_dic']['ras_description']; ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php echo ((is_array($_tmp=$this->_tpl_vars['info_dic']['unique_id_val'])) ? $this->_run_mod_handler('truncate', true, $_tmp, 8, "...", true) : smarty_modifier_truncate($_tmp, 8, "...", true)); ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php echo ((is_array($_tmp=$this->_tpl_vars['info_dic']['in_bytes'])) ? $this->_run_mod_handler('byte', true, $_tmp) : smarty_modifier_byte($_tmp)); ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php echo ((is_array($_tmp=$this->_tpl_vars['info_dic']['out_bytes'])) ? $this->_run_mod_handler('byte', true, $_tmp) : smarty_modifier_byte($_tmp)); ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php echo ((is_array($_tmp=$this->_tpl_vars['info_dic']['in_rate'])) ? $this->_run_mod_handler('byte', true, $_tmp) : smarty_modifier_byte($_tmp)); ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php echo ((is_array($_tmp=$this->_tpl_vars['info_dic']['out_rate'])) ? $this->_run_mod_handler('byte', true, $_tmp) : smarty_modifier_byte($_tmp)); ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php echo $this->_tpl_vars['info_dic']['owner_name']; ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	    <?php $this->_tag_stack[] = array('listTD', array('icon' => 'TRUE','extra' => "onClick='event.cancelBubble=true;'")); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <a style="text-decoration:none" href="javascript: killUser('<?php echo $this->_tpl_vars['info_dic']['user_id']; ?>
','<?php echo $this->_tpl_vars['info_dic']['normal_username']; ?>
','<?php echo $this->_tpl_vars['info_dic']['ras_ip']; ?>
','<?php echo $this->_tpl_vars['info_dic']['unique_id_val']; ?>
',true);" <?php echo smarty_function_jsconfirm(array(), $this);?>
>
			<?php echo smarty_function_listTableBodyIcon(array('action' => 'kick','cycle_color' => 'TRUE'), $this);?>

		    </a>
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	    <?php $this->_tag_stack[] = array('listTD', array('icon' => 'TRUE','extra' => "onClick='event.cancelBubble=true;'")); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <a style="text-decoration:none" href="javascript: killUser('<?php echo $this->_tpl_vars['info_dic']['user_id']; ?>
','<?php echo $this->_tpl_vars['info_dic']['normal_username']; ?>
','<?php echo $this->_tpl_vars['info_dic']['ras_ip']; ?>
','<?php echo $this->_tpl_vars['info_dic']['unique_id_val']; ?>
',false);" <?php echo smarty_function_jsconfirm(array(), $this);?>
>
			<?php echo smarty_function_listTableBodyIcon(array('action' => 'clear'), $this);?>

		    </a>
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	    <?php $this->_tag_stack[] = array('listTD', array('icon' => 'TRUE','extra' => "onClick='event.cancelBubble=true;'")); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <a style="text-decoration:none" href="/IBSng/admin/graph/realtime/realtime.php?img_url=bw.php?username=<?php echo $this->_tpl_vars['info_dic']['normal_username']; ?>
%26user_id=<?php echo $this->_tpl_vars['info_dic']['user_id']; ?>
%26ras_ip=<?php echo $this->_tpl_vars['info_dic']['ras_ip']; ?>
%26unique_id_val=<?php echo $this->_tpl_vars['info_dic']['unique_id_val']; ?>
">
			<?php echo smarty_function_listTableBodyIcon(array('action' => 'graph'), $this);?>

		    </a>
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	    <?php $this->_tag_stack[] = array('listTD', array('icon' => 'TRUE','extra' => "onClick='event.cancelBubble=true;'")); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <a style="text-decoration:none" href="/IBSng/admin/report/realtime_web_analyzer.php?username=<?php echo $this->_tpl_vars['info_dic']['normal_username']; ?>
&user_id=<?php echo $this->_tpl_vars['info_dic']['user_id']; ?>
">
			<?php echo smarty_function_listTableBodyIcon(array('action' => 'history'), $this);?>

		    </a>
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	    <?php $this->_tag_stack[] = array('listTD', array('icon' => 'TRUE','extra' => "onClick='event.cancelBubble=true;'")); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    
		<a onClick="showReportLayer('<?php echo $this->_tpl_vars['info_dic']['ras_ip']; ?>
_<?php echo $this->_tpl_vars['info_dic']['unique_id_val']; ?>
',this); return false;" href="#">
		    <?php echo smarty_function_listTableBodyIcon(array('action' => 'details'), $this);?>

		</a>
		<?php $this->_tag_stack[] = array('reportDetailLayer', array('name' => ($this->_tpl_vars['info_dic']['ras_ip'])."_".($this->_tpl_vars['info_dic']['unique_id_val']),'title' => 'Report Details')); $_block_repeat=true;smarty_block_reportDetailLayer($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <?php $this->_tag_stack[] = array('layerTable', array()); $_block_repeat=true;smarty_block_layerTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <?php $_from = ($this->_tpl_vars['info_dic']['attrs']); if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['key'] => $this->_tpl_vars['item']):
?>
    			<?php $this->_tag_stack[] = array('layerTR', array('cycle_color' => 'TRUE')); $_block_repeat=true;smarty_block_layerTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
				<?php echo $this->_tpl_vars['key']; ?>

	    		    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
			    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
				<?php echo $this->_tpl_vars['item']; ?>

	    		    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
			<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_layerTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		    <?php endforeach; endif; unset($_from); ?>
		    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_layerTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_reportDetailLayer($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	
    <?php endforeach; endif; unset($_from); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>