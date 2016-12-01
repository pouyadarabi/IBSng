{include file="user_header.tpl" title="BW Graph" selected="bw_graph"}
{include file="err_head.tpl"} 
{include file="util/calendar.tpl"} 

<form method="POST">
<input type=hidden name="show">
{addEditTable double=TRUE title="User BW Graph"}
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
{/addEditTable}
</form>

{if isset($img_path)}
    <img src="{$img_path}" border=0 align=center>
{/if}	

{include file="user_footer.tpl"}