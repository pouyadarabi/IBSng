{addEditTD type="left1" double=TRUE}
	Date From
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	{absDateSelect name="date_from" default_request="date_from"}
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Date To
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{absDateSelect name="date_to" default_request="date_to"}
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	User IDs
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	<input type=text class=text name=user_ids value="{ifisinrequest name="user_ids"}"> {multistr input_name="user_ids" form_name="web_analyzer_logs"}
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	IP Address
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	<input type=text class=text name="ip_addr" value="{ifisinrequest name="ip_addr"}">
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	URL
{/addEditTD}

{addEditTD type="right1" double=TRUE}
    {op class="likestr" name="url_op" selected="url_op"} 
	<input type=text class=text name=url value="{ifisinrequest name="url"}">
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Time Elapsed
{/addEditTD}

{addEditTD type="right2" double=TRUE}
    {op class="ltgteq" name="elapsed_op" selected="elapsed_op"} 
	<input type=text class=text name=elapsed value="{ifisinrequest name="elapsed"}"> Seconds
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Transferred Bytes
{/addEditTD}

{addEditTD type="right1" double=TRUE}
    {op class="ltgteq" name="bytes_op" selected="bytes_op"} 
	<input type=text class=text name=bytes value="{ifisinrequest name="bytes"}"> Bytes
{/addEditTD}

{addEditTD type="left2" double=TRUE}
{/addEditTD}

{addEditTD type="right2" double=TRUE}
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Sort By
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	{html_options name="order_by" options=$order_bys selected=$order_by_default} 
	Desc <input name=desc type=checkbox {checkBoxValue name="desc" default_checked=TRUE always_in_form="web_analyzer_logs"}>
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Results Per Page
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{reportRPP}
	View : {html_options name="view_options" options=$view_options selected=$view_by_default}
{/addEditTD}
