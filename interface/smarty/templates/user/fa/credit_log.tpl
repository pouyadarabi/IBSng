{* Credit Log

*}

{include file="user_header.tpl" title="تغییرات اعتبار کاربر" selected="credit_log"}
{include file="err_head.tpl"}

{include file="util/calendar.tpl"}

<form method=POST action="credit_log.php#show_results" name="connections">
<input type=hidden name=show value=1>
<input type=hidden name=page value=1>

{addEditTable double=TRUE title="شرایط نمایش"}

    {addEditTD type="left1" double=TRUE}
	از تاریخ
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	{absDateSelect name="change_time_from" default_request="change_time_from"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	تا تاریخ
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{absDateSelect name="change_time_to" default_request="change_time_to"}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	نمایش مجموع کل تغییرات اعتبار
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	<input type=checkbox class=checktext name=show_total_per_user_credit {checkBoxValue name="show_total_per_user_credit"}>
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	تعداد نتایج در هر صفحه
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{reportRPP no_high=TRUE}
    {/addEditTD}


{/addEditTable}

</form>

{if isInRequest("show")}

<a name="show_results"></a>
{listTable title="لیست تغییرات اعتبار" cols_num=5}
    {listTR type="header"}
	{listTD}
	    تاریخ
	{/listTD}

	{listTD}
	    تغییرات اعتبار
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

{listTable title=مجموع cols_num=2}

    {if isInRequest("show_total_per_user_credit")}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		<b> کل </b> مجموع تغییرات اعتبار:
    	    {/listTD}
	    {listTD}
	        {$total_per_user_credit|price} {$MONEY_UNIT}
	    {/listTD}

	{/listTR}
    {/if}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		</b> مجموع تغییرات اعتبار <b> در هر صفحه:
    	    {/listTD}
	    {listTD}
	        {$page_total_per_user_credit|price} {$MONEY_UNIT}
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
