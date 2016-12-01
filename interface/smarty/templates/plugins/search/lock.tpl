{addEditTD type="left"}
    User is Locked
{/addEditTD}
{addEditTD type="right"}
    <input type=checkbox name=lock value=t {checkBoxValue name="lock"}>
{/addEditTD}

{addEditTD type="left" comment=TRUE}
    Lock reason
{/addEditTD}
{addEditTD type="right" comment=TRUE}
    {op class="likestr" name="lock_reason_op" selected="lock_reason_op"} 
    <textarea class="text" style="height:47" name="lock_reason">{ifisinrequest name="lock_reason"}</textarea>
{/addEditTD}


