<?php /* Smarty version 2.6.13, created on 2006-06-13 19:23:16
         compiled from admin_header.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('modifier', 'capitalize', 'admin_header.tpl', 20, false),array('modifier', 'date_format', 'admin_header.tpl', 92, false),array('function', 'menuIcon', 'admin_header.tpl', 36, false),array('function', 'secondLvlMenu', 'admin_header.tpl', 51, false),array('block', 'reportDetailLayer', 'admin_header.tpl', 80, false),array('block', 'menuTR', 'admin_header.tpl', 82, false),)), $this); ?>
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
				<td class="Page_Top_Link">Admin</td>
				<td class="Page_Top_Link">&nbsp;</td>
				<td class="Page_Top_Link">Username:<font color="#FF9C00"><?php echo ((is_array($_tmp=$this->_tpl_vars['auth_name'])) ? $this->_run_mod_handler('capitalize', true, $_tmp) : smarty_modifier_capitalize($_tmp)); ?>
</font></td>
				<td class="Page_Top_Link"><img border="0" src="/IBSng/images/menu/line_between_topmenu.gif"></td>
				<td class="Page_Top_Link"><a class="Header_Top_links" href="/IBSng/admin/?logout=1">Logout</a></td>
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
				<td><?php echo smarty_function_menuIcon(array('name' => 'home'), $this);?>
</td>
				<td><?php echo smarty_function_menuIcon(array('name' => 'user'), $this);?>
</td>
				<td><?php echo smarty_function_menuIcon(array('name' => 'group'), $this);?>
</td>
				<td><?php echo smarty_function_menuIcon(array('name' => 'report'), $this);?>
</td>
				<td><?php echo smarty_function_menuIcon(array('name' => 'graph'), $this);?>
</td>
				<td><?php echo smarty_function_menuIcon(array('name' => 'admin'), $this);?>
</td>
				<td><?php echo smarty_function_menuIcon(array('name' => 'setting'), $this);?>
</td>
			</tr>
		</table>
		<!-- End Links Button -->
		</td>
	</tr>
	<tr>
		<td align="right" colspan="5" class="Header_Submenu">
			<table align="right" border="0" cellspacing="0" cellpadding="0" class="Header_Submenu">
				<tr><?php echo smarty_function_secondLvlMenu(array(), $this);?>

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
		<td class="Page_Header_Info">
		    <a style="font-weight: bold; color: black" href="#"
		    id="current_session_date_type" 
		    onClick="showReportLayer('session_date_select',this,'left'); return false;">
			<?php echo ((is_array($_tmp=$this->_tpl_vars['DATE_TYPE'])) ? $this->_run_mod_handler('capitalize', true, $_tmp) : smarty_modifier_capitalize($_tmp)); ?>

		    </a>
		    <?php $this->_tag_stack[] = array('reportDetailLayer', array('name' => 'session_date_select','title' => 'Select Date Type','width' => 150)); $_block_repeat=true;smarty_block_reportDetailLayer($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>

		    <?php $this->_tag_stack[] = array('menuTR', array()); $_block_repeat=true;smarty_block_menuTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			<a href="#" onClick="changeSessionDateType('gregorian'); return false;" class="page_menu">Gregorian</a>
		    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_menuTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		    <?php $this->_tag_stack[] = array('menuTR', array()); $_block_repeat=true;smarty_block_menuTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			<a href="#" onClick="changeSessionDateType('jalali'); return false;" class="page_menu">Jalali</a>
		    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_menuTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		    <?php $this->_tag_stack[] = array('menuTR', array()); $_block_repeat=true;smarty_block_menuTR($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
			<a href="#" onClick="changeSessionDateType('relative'); return false;" class="page_menu">Relative</a>
		    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_menuTR($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_reportDetailLayer($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
		    &nbsp;|&nbsp;<?php echo ((is_array($_tmp='now')) ? $this->_run_mod_handler('date_format', true, $_tmp, "%A, %B %e, %Y") : smarty_modifier_date_format($_tmp, "%A, %B %e, %Y")); ?>
&nbsp;&nbsp;
		</td>
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
		<td align="center" <?php if (isset ( $this->_tpl_vars['page_valign'] )): ?> valign=<?php echo $this->_tpl_vars['page_valign']; ?>
 <?php endif; ?>>		
