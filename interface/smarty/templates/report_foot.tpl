{multiTable}
    {multiTableTR}
	    {multiTableTD type="left"}
		    <nobr>Order By:
	    {/multiTableTD}
	    {multiTableTD type="right"}
			{html_options name="order_by" selected=$order_by_default options=$order_by_options}
	    {/multiTableTD}
	    {multiTableTD type="left"}
			Desc
	    {/multiTableTD}
	    {multiTableTD type="right"}
			<input style="height:12" type=checkbox name="desc" {ifisinrequest name="desc" value="checked"}>
	    {/multiTableTD}
	    {multiTableTD type="left"}
	    	<nobr>Result Per Page:
	    {/multiTableTD}
	    {multiTableTD type="right"}
			{reportRPP}
	    {/multiTableTD}
	
	    {multiTableTD type="left"}
		    <nobr>View:
	    {/multiTableTD}
	    {multiTableTD type="right"}
			{html_options name="view_options" options=$view_options selected=$view_by_default}
		{/multiTableTD}

{/multiTable}
