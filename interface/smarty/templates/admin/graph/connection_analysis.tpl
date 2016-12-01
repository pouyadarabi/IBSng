{include file="admin_header.tpl" title="Connections Analysis" selected="Connections Analysis"}
{include file="err_head.tpl"} 

<form method=POST action="connection_analysis.php" name="connection_analysis">
<input type=hidden name=show value=1>

{include file="util/calendar.tpl"}
{addEditTable double=TRUE title="Connections Analysis Conditions"}
    {addEditTD type="left1" double=TRUE}
	Analysis Type
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	{html_options name="analysis_type" options=$analysis_types selected=$analysis_type_default} 
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	User IDs
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	<input type=text class=text name=user_ids value="{ifisinrequest name="user_ids"}"> {multistr input_name="user_ids" form_name="connections"}
    {/addEditTD}


    {addEditTD type="left1" double=TRUE}
	Login Time From
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	{absDateSelect name="login_time_from" default_request="login_time_from"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Login Time To
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{absDateSelect name="login_time_to" default_request="login_time_to"}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	Logout Time From
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	{absDateSelect name="logout_time_from" default_request="logout_time_from"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Logout Time To
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{absDateSelect name="logout_time_to" default_request="logout_time_to"}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	Successful Logins
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	Yes <input type=checkbox class=checktext name="successful_yes" {checkBoxValue name="successful_yes" always_in_form="show" default_checked="TRUE"}>
	No <input type=checkbox class=checktext name="successful_no" {checkBoxValue name="successful_no" always_in_form="show" default_checked="TRUE"}>
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Service
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	Internet <input type=checkbox class=checktext name="service_internet" {checkBoxValue name="service_internet" always_in_form="show" default_checked="TRUE"}>
	VoIP <input type=checkbox class=checktext name="service_voip" {checkBoxValue name="service_voip" always_in_form="show" default_checked="TRUE"}>
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	Credit Used
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	{op class="ltgteq" name="credit_used_op" selected="credit_used_op"}
	<input type=text class=text name=credit_used value="{ifisinrequest name="credit_used"}"> {$MONEY_UNIT}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Owner
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{admin_names_select name="owner" default="All" default_request="owner" add_all=TRUE}
    {/addEditTD}


    {addEditTD type="left" double=TRUE comment=TRUE}
	Rases
    {/addEditTD}

    <td class="Form_Content_Row_right_Textarea_2col" valign="top" colspan="7">
    	{rasCheckBoxes prefix="ras"}
    </td></tr>
    <tr>
	<td colspan="9" class="Form_Content_Row_Space"></td>
    </tr>


{/addEditTable}


</form>

{if isInRequest("show")}
    <img src="connection_analysis_img.php?{requestToUrl}">
{/if}

{if requestVal("user_ids") ne ""}
    {addRelatedLink}
	<a href="/IBSng/admin/user/user_info.php?user_id_multi={$smarty.request.user_ids}" class="RightSide_links">
	    User <b>{$smarty.request.user_ids|truncate:15}</b> Info
        </a>
    {/addRelatedLink}

{/if}

{addRelatedLink}
    <a href="/IBSng/admin/report/online_users.php" class="RightSide_links">
	Online Users
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/connections.php" class="RightSide_links">
	Connection Logs
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/onlines.php" class="RightSide_links">
	Onlines Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php" class="RightSide_links">
	All RealTime Graph
    </a>
{/addRelatedLink}

{include file="admin_footer.tpl"}
