{multiTableTR}
    {reportToShowCheckBox name="From_Admin" output="From Admin"
			  default_checked="TRUE" always_in_form="deposit_change_logs"
			  value="show__from_admin_name" form_name="admin_deposit_change_logs"
			  container_name="change_deposit_logs_selected"}

    {reportToShowCheckBox name="To_Admin" output="To Admin"
			  default_checked="TRUE" always_in_form="deposit_change_logs"
			  value="show__to_admin_name" form_name="admin_deposit_change_logs"
			  container_name="change_deposit_logs_selected"}

    {reportToShowCheckBox name="Remote_Address" output="Remote Address"
			  default_checked="TRUE" always_in_form="deposit_change_logs"
			  value="show__remote_addr" form_name="admin_deposit_change_logs"
			  container_name="change_deposit_logs_selected"}

{multiTableTR}
    {reportToShowCheckBox name="Change_Time" output="Change Time"
			  default_checked="TRUE" always_in_form="deposit_change_logs"
			  value="show__change_time_formatted" form_name="admin_deposit_change_logs"
			  container_name="change_deposit_logs_selected"}

    {reportToShowCheckBox name="Deposit_Change" output="Deposit Change"
			  default_checked="TRUE" always_in_form="deposit_change_logs"
			  value="show__deposit_change|price" form_name="admin_deposit_change_logs"
			  container_name="change_deposit_logs_selected"}

    {reportToShowCheckBox name="Comment" output="Comment"
			  default_checked="TRUE" always_in_form="deposit_change_logs"
			  value="show__comment" form_name="admin_deposit_change_logs"
			  container_name="change_deposit_logs_selected"}
