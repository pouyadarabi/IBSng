{include file="admin_header.tpl" title="Onlines Graph" selected="Onlines Graph"} 
{include file="err_head.tpl"} 
{include file="util/calendar.tpl"} 

<form method="POST">
<input type=hidden name="show">
{addEditTable double=TRUE title="Online Users Graph"}
    {addEditTD type="left1" double=TRUE}
	Date From
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	{absDateSelect name="date_from" default_request="date_from" default="1"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Date To
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{absDateSelect name="date_to" default_request="date_to"}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	Type
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	Internet <input type=radio name=type value="internet" {radioButtonValue name="type" value="internet" default_checked="TRUE"}>
	VoIP <input type=radio name=type value="voip" {radioButtonValue name="type" value="voip"}>
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
    {/addEditTD}

    <td class="Form_Content_Row_right_Textarea_2col" valign="top" colspan="10">
    	{rasCheckBoxes prefix="ras"}
    </td></tr>
    <tr>
	<td colspan="9" class="Form_Content_Row_Space"></td>
    </tr>
{/addEditTable}
</form>

{if isset($img_path)}
    <img src="{$img_path}" border=0 align=center>
{/if}	


{addRelatedLink}
    <a href="/IBSng/admin/report/online_users.php" class="RightSide_links">
	Online Users
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php" class="RightSide_links">
	All RealTime Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php?internet=1" class="RightSide_links">
	Internet RealTime Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php?voip=1" class="RightSide_links">
	VoIP RealTime Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/realtime/realtime.php?img_url=bw.php" class="RightSide_links">
	BW RealTime Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/analysis/connection_analysis.php" class="RightSide_links">
	Connection Analysis
    </a>
{/addRelatedLink}


{setAboutPage title="Onlines Graph"}
    
{/setAboutPage}


{include file="admin_footer.tpl"}