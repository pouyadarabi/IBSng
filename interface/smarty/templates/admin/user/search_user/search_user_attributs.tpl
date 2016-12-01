{showAttributes form_name="search_user" always_in_form="search" cols=3 module="ALL"}

	{addAttribute name="Internet Username"
							value="show__attrs_normal_username"
							default_checked=TRUE}

	{addAttribute name = "VoIP Username"
						   value = "show__attrs_voip_username"
						   default_checked = TRUE
						   module = "VoIP"}
	
	{addAttribute name = "Credit"
						   value = "show__basic_credit|price"
						   default_checked = TRUE} 
	
	{addAttribute name = "Group"
						   value = "show__basic_group_name"
						   default_checked = TRUE} 
	
	{addAttribute name = "Owner"
						   value = "show__basic_owner_name"
						   default_checked = TRUE} 
	
	{addAttribute name = "Creation Date"
						   value = "show__basic_creation_date"
						   default_checked = FALSE} 
	
	{addAttribute name = "Relative ExpDate"
						   value = "show__attrs_rel_exp_date,show__attrs_rel_exp_date_unit"
						   default_checked = FALSE}
	
	{addAttribute name = "Absolute ExpDate"
						   value = "show__attrs_abs_exp_date"
						   default_checked = FALSE}
	
	{addAttribute name = "Multi Login"
						   value = "show__attrs_multi_login"
						   default_checked = FALSE}
	
	{addAttribute name = "Normal Charge"
						   value = "show__attrs_normal_charge"
						   default_checked = FALSE}
	
	{addAttribute name = "VoIP Charge"
						   value = "show__attrs_voip_charge"
						   default_checked = FALSE}
	
	{addAttribute name = "Lock"
						   value = "show__attrs_lock|lockFormat"
						   default_checked = FALSE}
{/showAttributes}
