{addEditTD type="left"}
    User ID
{/addEditTD}
{addEditTD type="right"}
    {op class="ltgteq" name="user_id_op" selected="user_id_op"} 
    <input class="text" type=text name=user_id value="{ifisinrequest name="user_id"}"> {multistr form_name="search_user" input_name="user_id"}
{/addEditTD}
