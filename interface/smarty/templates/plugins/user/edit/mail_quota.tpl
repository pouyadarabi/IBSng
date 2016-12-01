{attrUpdateMethod update_method="mailQuota"}
{userInfoTable title="Mail Quota" nofoot="TRUE"} 
    {userInfoTD type="user_left"}
	Has Mailbox
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_mail_quota" value="t" class=checkbox {if attrDefault($user_attrs,"mail_quota","has_mail_quota")!=""}checked{/if} onClick='mail_quota_select.toggle("mail_quota")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="mail_quota" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}


    {userInfoTD type="user_left"}
	Mail Quota:
    {/userInfoTD}

    {userInfoTD type="user_right"}
	{capture name="value"}{attrDefault default_request="mail_quota" default_var="mail_quota" target="user"}{/capture}
	<input id="mail_quota" type=text class=small_text name="mail_quota" value="{if isInRequest("mail_quota")}{$smarty.request.mail_quota}{else}{math equation="x/(1024*1024)" x=`$smarty.capture.value`}{/if}"> Mbytes
    {/userInfoTD}

    {userInfoTD type="group"}
	{ifHasAttr var_name="mail_quota" object="group"}
	    {$group_attrs.mail_quota|byte}
	{/ifHasAttr}
    {/userInfoTD}
{/userInfoTable}
<br>
<script language="javascript">
	mail_quota_select=new DomContainer();
	mail_quota_select.disable_unselected=true;
	mail_quota_select.addByID("mail_quota",[]);
{if attrDefault($user_attrs,"mail_quota","has_mail_quota")!=""}
    mail_quota_select.select("mail_quota");
{else}
    mail_quota_select.select(null);
{/if}
</script>
