{attrUpdateMethod update_method="mailQuota"}

  {viewTable title="Mailbox" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Mail Quota
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_mail_quota" value="t" class=checkbox {if attrDefault($group_attrs,"mail_quota","has_mail_quota")!=""}checked{/if} onClick='mail_quota_select.toggle("mail_quota")'>
    {/addEditTD}

    {addEditTD type="left"}
	Mailbox Quota
    {/addEditTD}

    {addEditTD type="right"}
	{capture name="value"}{attrDefault default_request="mail_quota" default_var="mail_quota" target="group"}{/capture}
	<input id="mail_quota" type=text class=small_text name="mail_quota" value="{math equation="x/(1024*1024)" x=`$smarty.capture.value`}"> Mbytes
    {/addEditTD}

  {/viewTable}
<script language="javascript">
	mail_quota_select=new DomContainer();
	mail_quota_select.disable_unselected=true;
	mail_quota_select.addByID("mail_quota");
{if attrDefault($group_attrs,"mail_quota","has_mail_quota")!=""}
    mail_quota_select.select("mail_quota");
{else}
    mail_quota_select.select(null);
{/if}
</script>


