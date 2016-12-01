{include file="header.tpl" title="Access Denied"}

<table align=center border=1>
<tr>
  <td align=center>
    <h2>
	<font color=red>
	    Access Denied
	</font>
    </h2>

    You must log in to access this page. <br>
    This page needs IBS authenticated <b>{$role|capitalize}</b>.<br>
    You can login <a href="{$url}"> here </a>
  </td>
</tr>
</table>