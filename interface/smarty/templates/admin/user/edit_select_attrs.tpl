{multiTableTR}
    {reportToShowCheckBox name="edit__normal_username" output="Internet Username"
    				default_checked=`$normal_username_checked` always_in_form="submit_form"
    				value="normal_username" form_name="edit_user" container_name="edit_attrs_selected"}

    {reportToShowCheckBox name="edit__voip_username" output="VoIP Username"
    				default_checked=`$voip_username_checked` always_in_form="submit_form"
    				value="voip_username" form_name="edit_user" container_name="edit_attrs_selected"}

    {reportToShowCheckBox name="edit__lock" output="Lock Status"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="lock" form_name="edit_user" container_name="edit_attrs_selected"}

{multiTableTR}
    {reportToShowCheckBox name="edit__rel_exp_date" output="Relative ExpDate"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="rel_exp_date" form_name="edit_user" container_name="edit_attrs_selected"}

    {reportToShowCheckBox name="edit__abs_exp_date" output="Absolute ExpDate"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="abs_exp_date" form_name="edit_user" container_name="edit_attrs_selected"}

    {reportToShowCheckBox name="edit__multi_login" output="Multi Login"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="multi_login" form_name="edit_user" container_name="edit_attrs_selected"}

{multiTableTR}
    {reportToShowCheckBox name="edit__normal_charge" output="Normal Charge"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="normal_charge" form_name="edit_user" container_name="edit_attrs_selected"}

    {reportToShowCheckBox name="edit__voip_charge" output="VoIP Charge"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="voip_charge" form_name="edit_user" container_name="edit_attrs_selected"}

    {reportToShowCheckBox name="edit__comment" output="Comment"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="comment" form_name="edit_user" container_name="edit_attrs_selected"}

{multiTableTR}
    {reportToShowCheckBox name="edit__ippool" output="IPpool"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="ippool" form_name="edit_user" container_name="edit_attrs_selected"}

    {reportToShowCheckBox name="edit__assign_ip" output="Assign IP"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="assign_ip" form_name="edit_user" container_name="edit_attrs_selected"}

    {reportToShowCheckBox name="edit__session_timeout" output="Session Timeout"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="session_timeout" form_name="edit_user" container_name="edit_attrs_selected"}

{multiTableTR}
    {reportToShowCheckBox name="edit__limit_mac" output="Limit Mac"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="limit_mac" form_name="edit_user" container_name="edit_attrs_selected"}

    {reportToShowCheckBox name="edit__limit_caller_id" output="Limit CallerID"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="limit_caller_id" form_name="edit_user" container_name="edit_attrs_selected"}

    {reportToShowCheckBox name="edit__limit_station_ip" output="Limit Station IP"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="limit_station_ip" form_name="edit_user" container_name="edit_attrs_selected"}

{multiTableTR}
    {reportToShowCheckBox name="edit__persistent_lan" output="Persistent Lan"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="persistent_lan" form_name="edit_user" container_name="edit_attrs_selected"}

    {reportToShowCheckBox name="edit__caller_id" output="VoIP CallerID"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="caller_id" form_name="edit_user" container_name="edit_attrs_selected"}

    {reportToShowCheckBox name="edit__email_address" output="Email Address"
    				default_checked="FALSE" always_in_form="submit_form"
    				value="email_address" form_name="edit_user" container_name="edit_attrs_selected"}

{if isset($user_search)}
	{multiTableTR}
	    {reportToShowCheckBox name="edit__group" output="Group"
	    			default_checked="FALSE" always_in_form="submit_form"
	    			value="group_name" form_name="edit_user" container_name="edit_attrs_selected"}

	    {reportToShowCheckBox name="edit__owner" output="Owner"
	    			default_checked="FALSE" always_in_form="submit_form"
	    			value="owner_name" form_name="edit_user" container_name="edit_attrs_selected"}

	    {multiTableTD type="left"}
	    {/multiTableTD}

	    {multiTableTD type="right"}
	    {/multiTableTD}
{/if}	
