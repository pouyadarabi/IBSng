{include file="header.tpl"}

<body topmargin="0" leftmargin="0" rightmargin="0" bottommargin="0" marginwidth="0" marginheight="0">

<!-- Header -->
<table border="0" width="100%" cellspacing="0" cellpadding="0">
	<tr>
		<td width="107"><img border="0" src="/IBSng/images/logo/logoibsng.gif"></td>

		<td rowspan="3" width="112" valign="top" class="Header_Color"><img border="0" src="/IBSng/images/logo/edition.gif">
		<br />&nbsp;Version {$IBSNG_VERSION}
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
				<td class="Page_Title">{$title}</td>
				<td width="27" ><img border="0" src="/IBSng/images/arrow/arrow_after_page_title.gif"></td>
			</tr>
		</table>
		</td>
		<td class="Page_Header_Line"></td>
	</tr>
	<tr>
		<td class="Page_Header_Info">{$smarty.now|date_format:"%A, %B %e, %Y"}&nbsp;&nbsp;</td>
	</tr>
	<tr>
		<td colspan="2" class="Page_Top_Space"></td>
	</tr>
</table>
<!-- End Page title & Info -->
