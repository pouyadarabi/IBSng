{* 
    Add New or edit Internet Charge Rule
    
    Success: client will be redirected to the charge information page
    Failure: this page is shown again with error message at top of the page

*}
{include file="admin_header.tpl" title="Internet Charge Rule" selected="Charge"}
{include file="err_head.tpl"}

<form method=POST name=add_internet_rule>
{addEditTable title="Internet Charge Rule" double="TRUE" table_width=580}
	    {include file="admin/charge/add_charge_rule_top.tpl"}
    	    {addEditTD type="left1" double="TRUE" err="cpm_err"}
		Charge Per Minute
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
		<input class="medium_text" type=text name=cpm value="{ifisinrequest name="cpm" default_var="cpm" }"> {$MONEY_UNIT}
	    <input type=hidden name=charge_name value="{$charge_name}">
	    {/addEditTD}
	    {addEditTD type="left2" double="TRUE" err="cpk_err"}
	    	Charge Per KiloByte
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
		<input class="medium_text" type=text name=cpk value="{ifisinrequest name="cpk" default_var="cpk" }"> {$MONEY_UNIT}
	    {/addEditTD}
    
    	    {addEditTD type="left1" double="TRUE" err="assumed_kps_err"}
		Max BW KBytes/Sec
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
		<input class="medium_text" type=text name=assumed_kps value="{ifisinrequest name="assumed_kps" default_var="assumed_kps" default=8}"> <FONT SIZE=1>KBytes/S</FONT>
		<input type=hidden name=charge_name value="{$charge_name}">
	    {/addEditTD}
	    {addEditTD type="left2" double="TRUE" err="bw_limit_err"}
		    Bandwidth Limit
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
		<input class="medium_text" type=text name=bandwidth_limit_kbytes value="{ifisinrequest name="bandwidth_limit_kbytes" default_var="bandwidth_limit" default=0}"> <FONT SIZE=1>KBytes/S</FONT>
	    {/addEditTD}

    	    {addEditTD type="left1" double="TRUE" err="tx_leaf_err"}
		BW Manager Send Leaf
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
	    	{html_options name="tx_leaf_name" output=$leaf_names values=$leaf_names selected=$tx_leaf_selected}
	    {/addEditTD}
	    {addEditTD type="left2" double="TRUE" err="rx_leaf_err"}
		BW Manager Receive Leaf
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
	    	{html_options name="rx_leaf_name" output=$leaf_names values=$leaf_names selected=$rx_leaf_selected}
	    {/addEditTD}

    <tr>
    <tr>
	<td colspan=9 height=9></td>
    </tr>	    
    <tr>
	<td colspan=9>
	    {include file="admin/charge/day_of_week_select.tpl" form_name="add_internet_rule"}
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
    <a href="/IBSng/admin/charge/add_internet_charge_rule.php?charge_name={$charge_name}" class="RightSide_links">
	Add Internet Charge Rule
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
{setAboutPage title="Internet Charge Rule"}

{/setAboutPage}


{include file="admin_footer.tpl"}
