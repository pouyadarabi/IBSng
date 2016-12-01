{if isset($approx_duration) }

{listTable title="مدت زمان تقریبی برای هر قانون" cols_num=6}
	{listTR type="header" close_tr=TRUE}
	    {listTD}
		ردیف
	    {/listTD}

	    {listTD}
		روزهای هفته
	    {/listTD}

	    {listTD}
		از
	    {/listTD}

	    {listTD}
		تا
	    {/listTD}

	    {listTD}
		مدت زمان
	    {/listTD}
	{/listTR}
	{foreach from=$approx_duration item=rule}
	{listTR type="body"}
	    {listTD}
		{counter name="approx_duration_counter"}
	    {/listTD}
	    {listTD}
		{if sizeof($rule[2])==7}
		    _ALL_
		{else}
		    {arrayJoin array=`$rule[2]` glue=", " truncate_each=3} 
		{/if}
	    {/listTD}

	    {listTD}
		{$rule[3]}
	    {/listTD}

	    {listTD}
		{$rule[4]}
	    {/listTD}

	    {listTD}
		{$rule[0]|duration}
	    {/listTD}
	{/listTR}
	{/foreach}
{/listTable}		
{/if}
