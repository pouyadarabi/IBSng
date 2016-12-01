{addEditTD type="left" comment=TRUE}
    Comment
{/addEditTD}
{addEditTD type="right" comment=TRUE}
    {op class="likestr" name="comment_op" selected="comment_op"}
    <textarea class="text" style="height:47" name="comment">{ifisinrequest name="comment"}</textarea>
{/addEditTD}

{addEditTD type="left"}
    Name
{/addEditTD}
{addEditTD type="right"}
    {op class="likestr" name="name_op" selected="name_op"}
    <input class="text" type=text name="name" value="{ifisinrequest name="name"}">
{/addEditTD}

{addEditTD type="left"}
    Phone
{/addEditTD}
{addEditTD type="right"}
    {op class="likestr" name="phone_op" selected="phone_op"}
    <input class="text" type=text name="phone" value="{ifisinrequest name="phone"}">
{/addEditTD}



