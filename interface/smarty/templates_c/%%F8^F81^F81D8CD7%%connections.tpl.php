<?php /* Smarty version 2.6.13, created on 2006-07-18 14:41:46
         compiled from admin/report/connections.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('function', 'math', 'admin/report/connections.tpl', 22, false),array('function', 'listTableHeaderIcon', 'admin/report/connections.tpl', 25, false),array('function', 'eval', 'admin/report/connections.tpl', 27, false),array('function', 'listTableBodyIcon', 'admin/report/connections.tpl', 67, false),array('function', 'reportPages', 'admin/report/connections.tpl', 155, false),array('function', 'requestToUrl', 'admin/report/connections.tpl', 172, false),array('block', 'listTable', 'admin/report/connections.tpl', 24, false),array('block', 'listTR', 'admin/report/connections.tpl', 26, false),array('block', 'layerTable', 'admin/report/connections.tpl', 35, false),array('block', 'layerTR', 'admin/report/connections.tpl', 37, false),array('block', 'listTD', 'admin/report/connections.tpl', 38, false),array('block', 'reportDetailLayer', 'admin/report/connections.tpl', 69, false),array('block', 'addRelatedLink', 'admin/report/connections.tpl', 162, false),array('block', 'setAboutPage', 'admin/report/connections.tpl', 214, false),array('modifier', 'byte', 'admin/report/connections.tpl', 43, false),array('modifier', 'price', 'admin/report/connections.tpl', 85, false),array('modifier', 'duration', 'admin/report/connections.tpl', 95, false),array('modifier', 'truncate', 'admin/report/connections.tpl', 164, false),)), $this); ?>

<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_header.tpl", 'smarty_include_vars' => array('title' => 'Connection Logs','selected' => 'Connection Logs','page_valign' => 'top')));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?> 
<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "err_head.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?> 
<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "util/calendar.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>

<form method=POST action="connections.php#show_results" name="connections">
<input type=hidden name=show_reports value=1>
<input type=hidden name=page value=1>



<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin/report/connection_logs/conditions/conditions.tpl", 'smarty_include_vars' => array('title' => 'Attributes To Show')));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>

</form>
<?php if (isInRequest ( 'show_reports' )): ?>

<a name="show_results"></a>

<?php echo smarty_function_math(array('equation' => "x + y",'assign' => 'size','x' => $this->_tpl_vars['size'],'y' => 1), $this);?>


<?php $this->_tag_stack[] = array('listTable', array('title' => 'Connection Logs','cols_num' => $this->_tpl_vars['size'])); $_block_repeat=true;smarty_block_listTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <?php echo smarty_function_listTableHeaderIcon(array('action' => 'details','close_tr' => 'TRUE'), $this);?>

    <?php $this->_tag_stack[] = array('listTR', array('type' => 'header')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php echo smarty_function_eval(array('var' => $this->_tpl_vars['generated_tpl_header']), $this);?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

  <?php $this->assign('page_total_credit', 0); ?>
  <?php $this->assign('page_total_duration', 0); ?>

    <?php $_from = $this->_tpl_vars['reports']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['row']):
?>
		<?php ob_start(); ?>
			<?php $this->_tag_stack[] = array('layerTable', array()); $_block_repeat=true;smarty_block_layerTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			    <?php $_from = ($this->_tpl_vars['row']['other']['details']); if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['tuple']):
?>
	    	        <?php $this->_tag_stack[] = array('layerTR', array('cycle_color' => 'TRUE')); $_block_repeat=true;smarty_block_layerTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
					    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
					        <?php echo $this->_tpl_vars['tuple'][0]; ?>
:
					    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
					    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
						<?php if ($this->_tpl_vars['tuple'][0] == 'bytes_in' || $this->_tpl_vars['tuple'][0] == 'bytes_out'): ?>
						    <?php echo ((is_array($_tmp=$this->_tpl_vars['tuple'][1])) ? $this->_run_mod_handler('byte', true, $_tmp) : smarty_modifier_byte($_tmp)); ?>

						<?php else: ?>
						    <?php echo $this->_tpl_vars['tuple'][1]; ?>
 
						<?php endif; ?>
						
					    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		
					    <?php if ($this->_tpl_vars['tuple'][0] == 'username'): ?>
					        <?php $this->assign('username', ($this->_tpl_vars['tuple'][1])); ?>
					    <?php elseif ($this->_tpl_vars['tuple'][0] == 'voip_username'): ?>
					        <?php $this->assign('username', ($this->_tpl_vars['tuple'][1])); ?>
					    <?php elseif ($this->_tpl_vars['tuple'][0] == 'persistent_lan'): ?>
					        <?php $this->assign('username', '_PLAN_'); ?>
					    <?php endif; ?>
					
					<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_layerTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
			    <?php endforeach; endif; unset($_from); ?>
			<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_layerTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		<?php $this->_smarty_vars['capture']['layer'] = ob_get_contents(); ob_end_clean(); ?>
	
		<?php $this->_tag_stack[] = array('listTR', array('type' => 'body')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		    <?php echo smarty_function_eval(array('var' => $this->_tpl_vars['generated_tpl_body']), $this);?>

		    <?php $this->_tag_stack[] = array('listTD', array('icon' => 'TRUE')); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    		<a onClick="showReportLayer('<?php echo $this->_tpl_vars['row']['other']['connection_log_id']; ?>
',this); return false;" href="#">
			    	<?php echo smarty_function_listTableBodyIcon(array('cycle_color' => 'TRUE','action' => 'details'), $this);?>

				</a>
			    <?php $this->_tag_stack[] = array('reportDetailLayer', array('name' => ($this->_tpl_vars['row']['other']['connection_log_id']),'title' => 'Report Details')); $_block_repeat=true;smarty_block_reportDetailLayer($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
					<?php echo $this->_smarty_vars['capture']['layer']; ?>

			    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_reportDetailLayer($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		
		<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php endforeach; endif; unset($_from); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('listTable', array('title' => 'Totals','cols_num' => 2)); $_block_repeat=true;smarty_block_listTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $this->_tag_stack[] = array('listTR', array('type' => 'body','cycle_color' => 'TRUE')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			<b>Page</b> Total Credit Used:
    	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	        <?php echo ((is_array($_tmp=$this->_tpl_vars['page_total_credit'])) ? $this->_run_mod_handler('price', true, $_tmp) : smarty_modifier_price($_tmp)); ?>
 <?php echo $this->_tpl_vars['MONEY_UNIT']; ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $this->_tag_stack[] = array('listTR', array('type' => 'body','cycle_color' => 'TRUE')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<b>Page</b> Total Duration:
    	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	        <?php echo ((is_array($_tmp=$this->_tpl_vars['page_total_duration'])) ? $this->_run_mod_handler('duration', true, $_tmp) : smarty_modifier_duration($_tmp)); ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php if (isInRequest ( 'show_total_credit_used' )): ?>
	<?php $this->_tag_stack[] = array('listTR', array('type' => 'body','cycle_color' => 'TRUE')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<b>Report</b> Total Credit Used:
    	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	        <?php echo ((is_array($_tmp=$this->_tpl_vars['total_credit'])) ? $this->_run_mod_handler('price', true, $_tmp) : smarty_modifier_price($_tmp)); ?>
 <?php echo $this->_tpl_vars['MONEY_UNIT']; ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php endif; ?>

    <?php if (isInRequest ( 'show_total_duration' )): ?>
	<?php $this->_tag_stack[] = array('listTR', array('type' => 'body','cycle_color' => 'TRUE')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    		<b>Report</b> Total Duration: 
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	        <?php echo ((is_array($_tmp=$this->_tpl_vars['total_duration'])) ? $this->_run_mod_handler('duration', true, $_tmp) : smarty_modifier_duration($_tmp)); ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php endif; ?>

    <?php if (isInRequest ( 'show_total_inouts' )): ?>
	<?php $this->_tag_stack[] = array('listTR', array('type' => 'body','cycle_color' => 'TRUE')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    		<b>Report</b> Total In Bytes: 
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	        <?php echo ((is_array($_tmp=$this->_tpl_vars['total_in_bytes'])) ? $this->_run_mod_handler('byte', true, $_tmp) : smarty_modifier_byte($_tmp)); ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

	<?php $this->_tag_stack[] = array('listTR', array('type' => 'body','cycle_color' => 'TRUE')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    		<b>Report</b> Total Out Bytes: 
	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	    <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	        <?php echo ((is_array($_tmp=$this->_tpl_vars['total_out_bytes'])) ? $this->_run_mod_handler('byte', true, $_tmp) : smarty_modifier_byte($_tmp)); ?>

	    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php endif; ?>

    <?php $this->_tag_stack[] = array('listTR', array('type' => 'body','cycle_color' => 'TRUE')); $_block_repeat=true;smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
        <?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		Total Number Of Results:
    	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $this->_tag_stack[] = array('listTD', array()); $_block_repeat=true;smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo $this->_tpl_vars['total_rows']; ?>
 
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_listTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php echo smarty_function_reportPages(array('total_results' => $this->_tpl_vars['total_rows']), $this);?>



<?php endif; ?>


<?php if (requestVal ( 'user_ids' ) != ""): ?>
    <?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<a href="/IBSng/admin/user/user_info.php?user_id_multi=<?php echo $_REQUEST['user_ids']; ?>
" class="RightSide_links">
	    User <b><?php echo ((is_array($_tmp=$_REQUEST['user_ids'])) ? $this->_run_mod_handler('truncate', true, $_tmp, 15) : smarty_modifier_truncate($_tmp, 15)); ?>
</b> Info
        </a>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php endif; ?>


<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="<?php echo smarty_function_requestToUrl(array(), $this);?>
&Internet_Username=show__details_username&Bytes_IN=show__details_bytes_in|byte&Bytes_OUT=show__details_bytes_out|byte&search=1&Login_Time=show__login_time_formatted&Logout_Time=show__logout_time_formatted&Duration=show__duration_seconds|duration&Successful=show__successful|formatBoolean&Service=show__service_type|formatServiceType&Credit=show__credit_used|price" class="RightSide_links">
	Internet Connections
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="<?php echo smarty_function_requestToUrl(array(), $this);?>
&VoIP_Username=show__details_voip_username&Called_Number=show__details_called_number&Prefix_Name=show__details_prefix_name&search=1&Login_Time=show__login_time_formatted&Logout_Time=show__logout_time_formatted&Duration=show__duration_seconds|duration&Successful=show__successful|formatBoolean&Service=show__service_type|formatServiceType&Credit=show__credit_used|price" class="RightSide_links">
	VoIP Connections
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/report/connection_usage.php" class="RightSide_links">
	Connection Usages
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/graph/analysis/connection_analysis.php" class="RightSide_links">
	Connections Analysis
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/report/online_users.php" class="RightSide_links">
	Online Users
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/report/credit_change.php" class="RightSide_links">
	Credit Changes
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/report/user_audit_logs.php" class="RightSide_links">
	User Audit Logs
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


<?php $this->_tag_stack[] = array('setAboutPage', array('title' => 'Connection Log')); $_block_repeat=true;smarty_block_setAboutPage($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start();  $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_setAboutPage($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_footer.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>