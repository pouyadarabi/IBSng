{* Connection Log

*}

{include file="user_header.tpl" title="گزارش اتصالات" selected="connection_log"}
{include file="err_head.tpl"}

{include file="util/calendar.tpl"}

<form method=POST action="connection_log.php#show_results" name="connections">

<input type=hidden name=show_reports value=1>
<input type=hidden name=page value=1>
<input type=hidden name=search value=1>

{include file = "user/fa/conditions/connection_log.tpl"}

<input type="hidden" name="show_total_credit_used" value="1">
<input type="hidden" name="show_total_duration" value="1">

</form>
{if isInRequest("show_reports")}

<a name="show_results"></a>

{listTable title="لیست اتصالات" cols_num=$size}
	{listTableHeaderIcon action="details" close_tr=TRUE}
    {listTR type="header"}
    	{eval var=$generated_tpl_header}
    {/listTR}

	{assign var="page_total_credit" value=0}
	{assign var="page_total_duration" value=0}


    {foreach from=$reports item=row}
	{capture name="layer"}
		{layerTable}
		    {foreach from=`$row.other.details` item=tuple}
	    	        {layerTR cycle_color=TRUE}
			    {listTD}
			        {$tuple[0]}:
			    {/listTD}
			    {listTD}
				{if $tuple[0] == "bytes_in" or $tuple[0] == "bytes_out"}
				    {$tuple[1]|byte}
				{else}
				    {$tuple[1]} 
				{/if}
				
			    {/listTD}

			    {if $tuple[0] == "username"}
			        {assign var="username" value=`$tuple[1]`}
			    {elseif $tuple[0] == "voip_username"}
			        {assign var="username" value=`$tuple[1]`}
			    {elseif $tuple[0] == "persistent_lan"}
			        {assign var="username" value="_PLAN_"}
			    {/if}
				
			{/layerTR}
		    {/foreach}
		{/layerTable}
	{/capture}

	{listTR type="body"}
	    {eval var=$generated_tpl_body}
	    {listTD icon=TRUE}
    		<a onClick="showReportLayer('{$row.other.connection_log_id}',this); return false;" href="#">
		    {listTableBodyIcon cycle_color=TRUE action="details"}
		</a>
		    {reportDetailLayer name=`$row.other.connection_log_id` title="Report Details"}
			{$smarty.capture.layer}
		    {/reportDetailLayer}
	    {/listTD}
	
	{/listTR}
    {/foreach}


{/listTable}

{listTable title=مجموع cols_num=2}

    {if isInRequest("show_total_credit_used")}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		<b> مجموع کل </b> اعتبار استفاده شده:
    	    {/listTD}
	    {listTD}
	        {$total_credit|price} {$MONEY_UNIT}
	    {/listTD}

	{/listTR}
    {/if}

    {if isInRequest("show_total_duration")}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		<b> مجموع کل </b> زمان اتصال:
	    {/listTD}
	    {listTD}
	        {$total_duration|duration}
	    {/listTD}
	{/listTR}
    {/if}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		</b>مجموع اعتبار استفاده شده <b> درصفحه :
    	    {/listTD}
	    {listTD}
	        {$page_total_credit|price} {$MONEY_UNIT}
	    {/listTD}

	{/listTR}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		</b>مجموع زمان اتصالات <b> درصفحه :
    	    {/listTD}
	    {listTD}
	        {$page_total_duration|duration}
	    {/listTD}

	{/listTR}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		تعداد کل ردیف ها:
    	    {/listTD}
	    {listTD}
	        {$total_rows} 
	    {/listTD}

	{/listTR}

{/listTable}

{reportPages total_results=$total_rows}

{/if}

{include file="user_footer.tpl"}
