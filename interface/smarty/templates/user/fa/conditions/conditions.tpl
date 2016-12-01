
{addEditTD type="left1" double=TRUE}
	از تاریخ
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	{absDateSelect name="login_time_from" default_request="login_time_from"}
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	تا تاریخ
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{absDateSelect name="login_time_to" default_request="login_time_to"}
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	اتصالات موفق
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	{html_options name="successful" values=$successful_options output=$successful_options selected=$successful_default}
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	نوع سرویس
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{html_options name="service" values=$services output=$services selected=$services_default}
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	مرتب بر اساس
{/addEditTD}

    {addEditTD type="right1" double=TRUE}
{html_options name="order_by" options=$order_bys selected=$order_by_default} 
	نزولی 
	<input name=desc type=checkbox {checkBoxValue name="desc" default_checked=TRUE always_in_form="show"}>
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	تعداد نتایج در هر صفحه
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{reportRPP no_high=TRUE}
	نمایش بر اساس : {html_options name="view_options" options=$view_options selected=$view_by_default}
{/addEditTD}
