<?php /* Smarty version 2.6.13, created on 2006-07-19 12:12:21
         compiled from user_header.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('modifier', 'capitalize', 'user_header.tpl', 22, false),array('modifier', 'date_format', 'user_header.tpl', 85, false),array('function', 'userMenuIcon', 'user_header.tpl', 38, false),array('block', 'ifUserHasAttr', 'user_header.tpl', 50, false),)), $this); ?>
<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "header.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>
<body topmargin="0" leftmargin="0" rightmargin="0" bottommargin="0" marginwidth="0" marginheight="0">

<!-- Header -->
<table border="0" width="100%" cellspacing="0" cellpadding="0">
	<tr>
		<td rowspan="3" width="107"><img border="0" src="/IBSng/images/logo/logoibsng.gif"></td>

		<td rowspan="3" width="112" valign="top" class="Header_Color"><img border="0" src="/IBSng/images/logo/edition.gif">
		<br />&nbsp;Version <?php echo $this->_tpl_vars['IBSNG_VERSION']; ?>

		</td>
		
		<td rowspan="3" width="100%" class="Header_Color"></td>
		<!-- Top right Link -->
		<td class="Header_Color" width="204"></td>
		<td width="180" height="19">
		<table height="19" border="0" width="100%" cellspacing="0" cellpadding="0">
			<tr class="Header_Top_link">
				<td width="7"><img border="0" src="/IBSng/images/header/top_right_links_begin.gif"></td>
				<td class="Page_Top_Link">User</td>
				<td class="Page_Top_Link">&nbsp;</td>
				<td class="Page_Top_Link">Username:<font color="#FF9C00"><?php echo ((is_array($_tmp=$this->_tpl_vars['auth_name'])) ? $this->_run_mod_handler('capitalize', true, $_tmp) : smarty_modifier_capitalize($_tmp)); ?>
</font></td>
				<td class="Page_Top_Link"><img border="0" src="/IBSng/images/menu/line_between_topmenu.gif"></td>
				<td class="Page_Top_Link"><a class="Header_Top_links" href="/IBSng/user/?logout=1">Logout</a></td>
			</tr>
		</table>
		</td>
		<!-- End Top right Link-->
	</tr>
	<tr>
		<td colspan="3" width="384" height="18" class="Header_Color"></td>
	</tr>
	<tr>
		<td colspan="3" width="384" height="24">
		<!-- Links Button -->
		<table border="0" width="384" cellspacing="0" height="24" cellpadding="0">
			<tr>
			    <td><?php echo smarty_function_userMenuIcon(array('name' => 'home'), $this);?>
</td>
			    <td><?php echo smarty_function_userMenuIcon(array('name' => 'change_pass'), $this);?>
</td>

			    <td>
			<?php if ($this->_tpl_vars['auth_type'] == 'NORMAL_USER'): ?>			    
			    <?php echo smarty_function_userMenuIcon(array('name' => 'connection_log','url_params' => "show_reports=1&rpp=20&page=1&order_by=login_time&desc=1&show_total_credit_used=1&show_total_duration=1&set_defaults=1&Username=show__details_username&Login_Time=show__login_time_formatted&Logout_Time=show__logout_time_formatted&Duration=show__duration_seconds|duration&Successful=show__successful|formatBoolean&Credit_Used=show__credit_used|price&Successful=show__successful|formatBoolean&Service=show__service_type|formatServiceType&Caller_ID=show__details_caller_id&Bytes_OUT=show__details_bytes_out|byte&Bytes_IN=show__details_bytes_out|byte#show_results"), $this);?>

			<?php else: ?>
				<?php echo smarty_function_userMenuIcon(array('name' => 'connection_log','url_params' => "show_reports=1&rpp=20&page=1&order_by=login_time&desc=1&show_total_credit_used=1&show_total_duration=1&set_defaults=1&Username=show__details_username&Login_Time=show__login_time_formatted&Logout_Time=show__logout_time_formatted&Duration=show__duration_seconds|duration&Successful=show__successful|formatBoolean&Credit_Used=show__credit_used|price&Successful=show__successful|formatBoolean&Service=show__service_type|formatServiceType&Caller_ID=show__details_caller_id&Called_Number=show__details_called_number&Prefix_Name=show__details_prefix_name#show_results"), $this);?>

			<?php endif; ?>
			    </td>
    	    		    <td><?php echo smarty_function_userMenuIcon(array('name' => 'credit_log','url_params' => "show=1&rpp=20&page=1&show_total_per_user_credit=1#show_results"), $this);?>
</td>
    	    		    <td><?php echo smarty_function_userMenuIcon(array('name' => 'view_messages','url_params' => "show=1&rpp=20&page=1&order_by=message_id&desc=1#show_results"), $this);?>
</td>
			    <?php $this->_tag_stack[] = array('ifUserHasAttr', array('user_id' => -1,'attr_name' => 'save_bw_usage')); $_block_repeat=true;smarty_block_ifUserHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
				<td><?php echo smarty_function_userMenuIcon(array('name' => 'bw_graph'), $this);?>
</td>
			    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_ifUserHasAttr($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

			</tr>
		</table>
		<!-- End Links Button -->
		</td>
	</tr>
	<tr>
		<td align="right" colspan="5" class="Header_Submenu">
			<table align="right" border="0" cellspacing="0" cellpadding="0" class="Header_Submenu">
				<tr>
				<td width=10></td>
				</tr>
			</table>
		</td>
	</tr>
<tr><td colspan=5 valign=top height=25>
<!-- End Header -->
<!-- Page title & Info -->
<table border="0" width="100%" cellspacing="0" cellpadding="0">
	<tr>
		<td width="200" rowspan="2">
		<table border="0" width="100%" cellspacing="0" cellpadding="0">
			<tr>
				<td width="22"><img border="0" src="/IBSng/images/arrow/arrow_before_page_title.gif"></td>
				<td class="Page_Title"><?php echo $this->_tpl_vars['title']; ?>
</td>
				<td width="27" ><img border="0" src="/IBSng/images/arrow/arrow_after_page_title.gif"></td>
			</tr>
		</table>
		</td>
		<td class="Page_Header_Line"></td>
	</tr>
	<tr>
		<td class="Page_Header_Info"><?php echo ((is_array($_tmp='now')) ? $this->_run_mod_handler('date_format', true, $_tmp, "%A, %B %e, %Y") : smarty_modifier_date_format($_tmp, "%A, %B %e, %Y")); ?>
&nbsp;&nbsp;</td>
	</tr>
	<tr>
		<td colspan="2" class="Page_Top_Space"></td>
	</tr>
</table>
<!-- End Page title & Info -->
</td></tr>
</table>
<!-- Main Table -->
<table border="0" cellspacing="0" cellpadding="0" class="Main_Page">
	<tr>
		<td align="center">		
