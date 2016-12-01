{attrUpdateMethod update_method="comment"}
{viewTable title="Comment" table_width="380" nofoot="TRUE"} 
    {addEditTD type="left"}
	Has comment
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_comment" value="t" class=checkbox {if attrDefault($user_attrs,"comment","has_comment")!=""}checked{/if} onClick='comment_select.toggle("comment")'>
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	Comment
    {/addEditTD}

    {addEditTD type="right" comment=TRUE}
	<textarea name=comment id=comment class=text>{attrDefault target="user" default_var="comment" default_request="comment"}</textarea>
	{helpicon subject="comment" category="user"}
    {/addEditTD}

{/viewTable}
<script language="javascript">
	comment_select=new DomContainer();
	comment_select.disable_unselected=true;
	comment_select.addByID("comment");
{if attrDefault($user_attrs,"comment","has_comment")!=""}
    comment_select.select("comment");
{else}
    comment_select.select(null);
{/if}
</script>