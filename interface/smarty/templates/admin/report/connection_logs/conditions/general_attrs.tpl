{multiTableTR}
    {reportToShowCheckBox name="Username" output="Username"
			  default_checked="TRUE" always_in_form="admin_connection_logs"
			  value="show__details_any_username" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="Credit" output="Credit"
			  default_checked="TRUE" always_in_form="admin_connection_logs"
			  value="show__credit_used|price" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="Login_Time" output="Login Time"
			  default_checked="TRUE" always_in_form="admin_connection_logs"
			  value="show__login_time_formatted" form_name="connections"
			  container_name="general_selected"}


{multiTableTR}
    {reportToShowCheckBox name="Logout_Time" output="Logout Time"
			  default_checked="TRUE" always_in_form="admin_connection_logs"
			  value="show__logout_time_formatted" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="Duration" output="Duration"
			  default_checked="TRUE" always_in_form="admin_connection_logs"
			  value="show__duration_seconds|duration" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="Successful" output="Successful"
			  default_checked="TRUE" always_in_form="admin_connection_logs"
			  value="show__successful|formatBoolean" form_name="connections"
			  container_name="general_selected"}

{multiTableTR}
    {reportToShowCheckBox name="Service" output="Service"
			  default_checked="TRUE" always_in_form="admin_connection_logs"
			  value="show__service_type|formatServiceType" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="RAS" output="RAS"
			  default_checked="TRUE" always_in_form="admin_connection_logs"
			  value="show__ras_description" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="Caller_ID" output="Caller ID"
			  default_checked="FALSE" always_in_form="admin_connection_logs"
			  value="show__details_caller_id" form_name="connections"
			  container_name="general_selected"}
