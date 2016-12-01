{addEditTD type="left"}
    Relative Expiration Date
{/addEditTD}
{addEditTD type="right"}
    {op class="ltgteq" name="rel_exp_date_op" selected="rel_exp_date_op"}
    {absDateSelect name="rel_exp_date" default_request="rel_exp_date"}

{/addEditTD}

{addEditTD type="left"}
    Relative Expiration Value
{/addEditTD}
{addEditTD type="right"}
    {op class="ltgteq" name="rel_exp_value_op" selected="rel_exp_value_op"} 
    <input class="text" type=text name=rel_exp_value value="{ifisinrequest name="rel_exp_value"}"> 
    {relative_units name="rel_exp_value_unit" default_request="rel_exp_value_unit"}
{/addEditTD}
