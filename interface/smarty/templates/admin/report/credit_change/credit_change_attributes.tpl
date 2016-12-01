{showAttributes form_name="credit_change" always_in_form="credit_change"}
	{addAttribute name="Date"
				  value="show__change_time_formatted"
				  default_checked=TRUE}

	{addAttribute name="Action"
				  value="show__action_text"
				  default_checked=TRUE}

	{addAttribute name="Issuer Admin"
				  value="show__admin_name|linkAdminNameToAdminInfo"
				  default_checked=TRUE}

	{addAttribute name="Per User Credit"
				  value="show__per_user_credit|price"
				  default_checked=TRUE}

	{addAttribute name="Admin Credit Consumed"
				  value="show__admin_credit|price"
				  default_checked=TRUE}

	{addAttribute name="IP Address"
				  value="show__remote_addr"
				  default_checked=FALSE}

	{addAttribute name="User IDs"
				  value="show__user_ids"
				  default_checked=FALSE}

	{addAttribute name="Comment"
				  value="show__comment"
				  default_checked=FALSE}

{/showAttributes}
