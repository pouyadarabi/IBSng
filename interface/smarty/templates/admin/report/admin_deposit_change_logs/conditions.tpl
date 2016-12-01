{addEditTD type="left1" double=TRUE}
	From Admin
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	{admin_names_select name="from_admin" default="All" default_request="from_admin" add_all=TRUE}
{/addEditTD}


{addEditTD type="left2" double=TRUE}
	To Admin
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{admin_names_select name="to_admin" default="All" default_request="to_admin" add_all=TRUE}
{/addEditTD}

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
	Sort By
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	{html_options name="order_by" options=$order_bys selected=$order_by_default} 
	Desc <input name=desc type=checkbox {checkBoxValue name="desc" default_checked=TRUE always_in_form="show"}>
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	show totals of
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	Deposit Change <input name=show_total_deposit_change type=checkbox {checkBoxValue name="show_total_deposit_change" default_checked=FALSE always_in_form="admin_deposit_change_logs"}>
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Results Per Page
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	{reportRPP}
	View : {html_options name="view_options" options=$view_options selected=$view_by_default}
{/addEditTD}
