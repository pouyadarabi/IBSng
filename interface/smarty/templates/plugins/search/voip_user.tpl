{addEditTD type="left"}
    VoIP Username
{/addEditTD}
{addEditTD type="right"}
    {op class="likestr" name="voip_username_op" selected="voip_username_op"} 
    <input class="text" type=text name=voip_username value="{ifisinrequest name="voip_username"}"> {multistr form_name="search_user" input_name="voip_username"}
{/addEditTD}
