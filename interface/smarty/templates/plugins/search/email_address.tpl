{addEditTD type="left"}
    Email Address
{/addEditTD}
{addEditTD type="right"}
    {op class="likestr" name="email_address_op" selected="email_address_op"} 
    <input class="text" type=text name=email_address value="{ifisinrequest name="email_address"}"> {multistr form_name="search_user" input_name="email_address"}
{/addEditTD}
