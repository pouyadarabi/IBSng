<?php /* Smarty version 2.6.13, created on 2006-06-13 19:23:06
         compiled from stripped_header.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('modifier', 'date_format', 'stripped_header.tpl', 43, false),)), $this); ?>
<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "header.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>

<body topmargin="0" leftmargin="0" rightmargin="0" bottommargin="0" marginwidth="0" marginheight="0">

<!-- Header -->
<table border="0" width="100%" cellspacing="0" cellpadding="0">
	<tr>
		<td width="107"><img border="0" src="/IBSng/images/logo/logoibsng.gif"></td>

		<td rowspan="3" width="112" valign="top" class="Header_Color"><img border="0" src="/IBSng/images/logo/edition.gif">
		<br />&nbsp;Version <?php echo $this->_tpl_vars['IBSNG_VERSION']; ?>

		</td>

		<td width="100%" class="Header_color"></td>
	</tr>
	<tr>
		<td align="right" colspan="3" class="Header_Submenu">
			<table align="right" border="0" cellspacing="0" cellpadding="0" class="Header_Submenu">
				<tr>
				    <td>
				    </td>
				</tr>
			</table>
		</td>
	</tr>
</table>
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
		<td class="Page_Header_Info"><?php echo ((is_array($_tmp=time())) ? $this->_run_mod_handler('date_format', true, $_tmp, "%A, %B %e, %Y") : smarty_modifier_date_format($_tmp, "%A, %B %e, %Y")); ?>
&nbsp;&nbsp;</td>
	</tr>
	<tr>
		<td colspan="2" class="Page_Top_Space"></td>
	</tr>
</table>
<!-- End Page title & Info -->