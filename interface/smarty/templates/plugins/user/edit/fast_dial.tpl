{attrUpdateMethod update_method="fastDial"}
{viewTable title="Fast Dial" table_width="380" nofoot="TRUE"} 
    {addEditTD type="left"}
	Has Fast Dial
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_fast_dial" value="t" class=checkbox onClick='fast_dial_select.toggle("fast_dial0")'>
	{helpicon subject="fast dial" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	Index 0
    {/addEditTD}

    {addEditTD type="right"}
	<input id="fast_dial0" type=text class=text name="fast_dial0" value="{if isInRequest("fast_dial0")}{$smarty.request.fast_dial0}{elseif isset($user_attrs.fast_dial)}{$user_attrs.fast_dial[0]}{/if}">
    {/addEditTD}

    {addEditTD type="left"}
	Index 1
    {/addEditTD}

    {addEditTD type="right"}
	<input id="fast_dial1" type=text class=text name="fast_dial1" value="{if isInRequest("fast_dial1")}{$smarty.request.fast_dial1}{elseif isset($user_attrs.fast_dial)}{$user_attrs.fast_dial[1]}{/if}">
    {/addEditTD}

    {addEditTD type="left"}
	Index 2
    {/addEditTD}

    {addEditTD type="right"}
	<input id="fast_dial2" type=text class=text name="fast_dial2" value="{if isInRequest("fast_dial2")}{$smarty.request.fast_dial2}{elseif isset($user_attrs.fast_dial)}{$user_attrs.fast_dial[2]}{/if}">
    {/addEditTD}

    {addEditTD type="left"}
	Index 3
    {/addEditTD}

    {addEditTD type="right"}
	<input id="fast_dial3" type=text class=text name="fast_dial3" value="{if isInRequest("fast_dial3")}{$smarty.request.fast_dial3}{elseif isset($user_attrs.fast_dial)}{$user_attrs.fast_dial[3]}{/if}">
    {/addEditTD}

    {addEditTD type="left"}
	Index 4
    {/addEditTD}

    {addEditTD type="right"}
	<input id="fast_dial4" type=text class=text name="fast_dial4" value="{if isInRequest("fast_dial4")}{$smarty.request.fast_dial4}{elseif isset($user_attrs.fast_dial)}{$user_attrs.fast_dial[4]}{/if}">
    {/addEditTD}

    {addEditTD type="left"}
	Index 5
    {/addEditTD}

    {addEditTD type="right"}
	<input id="fast_dial5" type=text class=text name="fast_dial5" value="{if isInRequest("fast_dial5")}{$smarty.request.fast_dial5}{elseif isset($user_attrs.fast_dial)}{$user_attrs.fast_dial[5]}{/if}">
    {/addEditTD}

    {addEditTD type="left"}
	Index 6
    {/addEditTD}

    {addEditTD type="right"}
	<input id="fast_dial6" type=text class=text name="fast_dial6" value="{if isInRequest("fast_dial6")}{$smarty.request.fast_dial6}{elseif isset($user_attrs.fast_dial)}{$user_attrs.fast_dial[6]}{/if}">
    {/addEditTD}

    {addEditTD type="left"}
	Index 7
    {/addEditTD}

    {addEditTD type="right"}
	<input id="fast_dial7" type=text class=text name="fast_dial7" value="{if isInRequest("fast_dial7")}{$smarty.request.fast_dial7}{elseif isset($user_attrs.fast_dial)}{$user_attrs.fast_dial[7]}{/if}">
    {/addEditTD}

    {addEditTD type="left"}
	Index 8
    {/addEditTD}

    {addEditTD type="right"}
	<input id="fast_dial8" type=text class=text name="fast_dial8" value="{if isInRequest("fast_dial8")}{$smarty.request.fast_dial8}{elseif isset($user_attrs.fast_dial)}{$user_attrs.fast_dial[8]}{/if}">
    {/addEditTD}

    {addEditTD type="left"}
	Index 9
    {/addEditTD}

    {addEditTD type="right"}
	<input id="fast_dial9" type=text class=text name="fast_dial9" value="{if isInRequest("fast_dial9")}{$smarty.request.fast_dial9}{elseif isset($user_attrs.fast_dial)}{$user_attrs.fast_dial[9]}{/if}">
    {/addEditTD}
    
{/viewTable}
<script language="javascript">
	fast_dial_select=new DomContainer();
	fast_dial_select.disable_unselected=true;
	fast_dial_select.addByID("fast_dial0",["fast_dial1","fast_dial2","fast_dial3","fast_dial4","fast_dial5","fast_dial6","fast_dial7","fast_dial8","fast_dial9"]);
{if attrDefault($user_attrs,"fast_dial","has_fast_dial")!=""}
    fast_dial_select.select("fast_dial0");
    document.user_edit.has_fast_dial.checked = true;
{else}
    fast_dial_select.select(null);
{/if}
</script>