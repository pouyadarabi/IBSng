{* 
    Add New or edit VoIP Charge Rule
    
    Success: client will be redirected to the charge information page
    Failure: this page is shown again with error message at top of the page

*}
{include file="admin_header.tpl" title="VoIP Charge Rule" selected="Charge"}
{include file="err_head.tpl"}

<form method=POST name=add_voip_rule>
{addEditTable title="VoIP Charge Rule" double="TRUE" table_width=580}
    {include file="admin/charge/add_charge_rule_top.tpl"}
    {addEditTD type="left1" double="TRUE"}
	Tariff Name
    {/addEditTD}
    {addEditTD type="right1" double="TRUE" err="tariff_err"}
	{html_options name="tariff_name" output=$tariff_names values=$tariff_names selected=$tariff_name_selected}
    {/addEditTD}

    {addEditTD type="left2" double="TRUE"}
    {/addEditTD}
    {addEditTD type="right2" double="TRUE"}
    {/addEditTD}
    <tr>    
    <tr>
	<td colspan=9 height=9></td>
    </tr>	    
    <tr>
	<td colspan=9>
	    {include file="admin/charge/day_of_week_select.tpl" form_name="add_voip_rule"}
	</td>
    </tr>	    
    <tr>
	<td colspan=9 height=9></td>
    </tr>	    
	
    <td colspan=9>
	    {include file="admin/charge/ras_select.tpl"}
	</td>
    </tr>
{/addEditTable}
{addRelatedLink}
    <a href="/IBSng/admin/charge/add_voip_charge_rule.php?charge_name={$charge_name}" class="RightSide_links">
	Add VoIP Charge Rule
    </a>
{/addRelatedLink}
{addRelatedLink}
    <a href="/IBSng/admin/charge/add_new_charge.php" class="RightSide_links">
	Add New Charge 
    </a>
{/addRelatedLink}
{addRelatedLink}
    <a href="/IBSng/admin/charge/charge_list.php" class="RightSide_links">
	 Charge List
    </a>
{/addRelatedLink}
{setAboutPage title="VoIP Charge Rule"}

{/setAboutPage}


{include file="admin_footer.tpl"}
