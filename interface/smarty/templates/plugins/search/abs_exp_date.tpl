{include file="util/calendar.tpl"}
{addEditTD type="left"}
    Absolute Expiration Date
{/addEditTD}
{addEditTD type="right"}
    {op class="ltgteq" name="abs_exp_date_op" selected="abs_exp_date_op"}
    {absDateSelect name="abs_exp_date" default_request="abs_exp_date"}
{/addEditTD}
