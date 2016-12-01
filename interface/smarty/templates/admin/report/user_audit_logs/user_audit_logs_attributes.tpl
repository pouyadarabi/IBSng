{showAttributes form_name="user_audit_log" always_in_form="user_audit_log_in_form"}
	{addAttribute name="Date"
				  value="show__change_time_formatted"
				  default_checked=TRUE}

	{addAttribute name="Issuer Admin"
				  value="show__admin_name|linkAdminNameToAdminInfo"
				  default_checked=TRUE}

	{addAttribute name="User/Group"
				  value="show__user_group_type"
				  default_checked=TRUE}

	{addAttribute name="ID"
				  value="show__name"
				  default_checked=TRUE}

	{addAttribute name="Attr Name"
				  value="show__attr_name"
				  default_checked=TRUE}

	{addAttribute name="Old Value"
				  value="show__old_value"
				  default_checked=TRUE}

	{addAttribute name="New Value"
				  value="show__new_value"
				  default_checked=TRUE}

{/showAttributes}
