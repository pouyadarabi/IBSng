{* Credit Log

*}

{include file="user_header.tpl" title="Credit Log" selected="credit_log"}
{include file="err_head.tpl"}

{include file="util/calendar.tpl"}

<form method=POST action="credit_log.php#show_results" name="connections">
<input type=hidden name=show value=1>
<input type=hidden name=page value=1>

{addEditTable double=TRUE title="Credit Change Conditions"}

    {addEditTD type="left1" double=TRUE}
	Change Time From
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	{absDateSelect name="change_time_from" default_request="change_time_from"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Change Time To
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{absDateSelect name="change_time_to" default_request="change_time_to"}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	Show Total of Credit Changes
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	<input type=checkbox class=checktext name=show_total_per_user_credit {checkBoxValue name="show_total_per_user_credit"}>
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Result Per Page
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{reportRPP no_high=TRUE}
    {/addEditTD}


{/addEditTable}

</form>

{if isInRequest("show")}

<a name="show_results"></a>
{listTable title="Credit Changes" cols_num=5}
    {listTR type="header"}
	{listTD}
	    Date
	{/listTD}

	{listTD}
	    Credit Change
	{/listTD}

    {/listTR}

  {assign var="page_total_per_user_credit" value=0}

  {foreach from=$report item=row}
    {listTR type="body" cycle_color=TRUE}
	{listTD}
	    {$row.change_time_formatted}
	{/listTD}

	{listTD}
	    {$row.per_user_credit|price}
	    {math equation="x + y" assign=page_total_per_user_credit x=`$row.per_user_credit` y=$page_total_per_user_credit}
	{/listTD}

    {/listTR}
  {/foreach}
    
{/listTable}    

{listTable title=Totals cols_num=2}

    {if isInRequest("show_total_per_user_credit")}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		<b>Report</b> Total Credit Changes:
    	    {/listTD}
	    {listTD}
	        {$total_per_user_credit|price} {$MONEY_UNIT}
	    {/listTD}

	{/listTR}
    {/if}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		<b>Page</b> Total Credit Changes:
    	    {/listTD}
	    {listTD}
	        {$page_total_per_user_credit|price} {$MONEY_UNIT}
	    {/listTD}

	{/listTR}


	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		Total Number Of Rows:
    	    {/listTD}
	    {listTD}
	        {$total_rows} 
	    {/listTD}

	{/listTR}


{/listTable}

{reportPages total_results=$total_rows}

{/if}


{include file="user_footer.tpl"}