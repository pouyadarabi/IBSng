{* Online Users By Type : Show a list of online users, seperated by their type(eg. Internet or VoIP)
*}

{include file="admin_header.tpl" title="Online Users" selected="Online Users"} 
{include file="err_head.tpl"} 
<iframe name=msg id=msg border=0 FRAMEBORDER=0 SCROLLING=NO height=50 valign=top src="/IBSng/util/empty.php"></iframe>

<div align=center><a href="online_users.php?js" class="page_menu" style="font-weight: bold; font-size: 11; font-family: tahoma;">Switch to Advanced Mode</a></div>
<br>

{include file="refresh_header.tpl" title="Online Users"}

{include file="admin/report/internet_onlines.tpl"}
{include file="admin/report/voip_onlines.tpl"}

{include file="admin/report/online_users_footer.tpl"}


