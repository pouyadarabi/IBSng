{addEditTD type="left1" double=TRUE}
	User IDs
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	<input type=text class=text name=user_ids value="{ifisinrequest name="user_ids"}"> {multistr input_name="user_ids" form_name="user_audit_log"}
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Group Name
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{group_names_select name="group_name" default="All" default_request="group_name" add_all=TRUE}
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Attribute Names
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	<input type=text class=text name=attr_names value="{ifisinrequest name="attr_names"}"> {multistr input_name="attr_names" form_name="user_audit_log"}
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Issuer Admin
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{admin_names_select name="admin" default="All" default_request="admin" add_all=TRUE}
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
	Results Per Page
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{reportRPP}
	View : {html_options name="view_options" options=$view_options selected=$view_by_default}
{/addEditTD}
