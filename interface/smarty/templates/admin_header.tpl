{include file="header.tpl"}
<body topmargin="0" leftmargin="0" rightmargin="0" bottommargin="0" marginwidth="0" marginheight="0">

<!-- Header -->
<table border="0" width="100%" cellspacing="0" cellpadding="0">
	<tr>
		<td rowspan="3" width="107"><img border="0" src="/IBSng/images/logo/logoibsng.gif"></td>
		<td rowspan="3" width="112" valign="top" class="Header_Color"><img border="0" src="/IBSng/images/logo/edition.gif">
		<br />&nbsp;Version {$IBSNG_VERSION}
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
				<td class="Page_Top_Link">Username:<font color="#FF9C00">{$auth_name|capitalize}</font></td>
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
				<td>{menuIcon name="home"}</td>
				<td>{menuIcon name="user"}</td>
				<td>{menuIcon name="group"}</td>
				<td>{menuIcon name="report"}</td>
				<td>{menuIcon name="graph"}</td>
				<td>{menuIcon name="admin"}</td>
				<td>{menuIcon name="setting"}</td>
			</tr>
		</table>
		<!-- End Links Button -->
		</td>
	</tr>
	<tr>
		<td align="right" colspan="5" class="Header_Submenu">
			<table align="right" border="0" cellspacing="0" cellpadding="0" class="Header_Submenu">
				<tr>{secondLvlMenu}
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
				<td class="Page_Title">{$title}</td>
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
			{$DATE_TYPE|capitalize}
		    </a>
		    {reportDetailLayer name="session_date_select" title="Select Date Type" width=150}

		    {menuTR}
			<a href="#" onClick="changeSessionDateType('gregorian'); return false;" class="page_menu">Gregorian</a>
		    {/menuTR}
		    {menuTR}
			<a href="#" onClick="changeSessionDateType('jalali'); return false;" class="page_menu">Jalali</a>
		    {/menuTR}
		    {menuTR}
			<a href="#" onClick="changeSessionDateType('relative'); return false;" class="page_menu">Relative</a>
		    {/menuTR}
		    {/reportDetailLayer}
		    &nbsp;|&nbsp;{"now"|date_format:"%A, %B %e, %Y"}&nbsp;&nbsp;
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
		<td align="center" {if isset($page_valign)} valign={$page_valign} {/if}>		

