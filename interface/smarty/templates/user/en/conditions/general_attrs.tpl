{multiTableTR}
    {reportToShowCheckBox name="Username" output="Username"
			  default_checked="TRUE" always_in_form="search"
			  value="show__details_username" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="Login_Time" output="Login Time"
			  default_checked="FALSE" always_in_form="search"
			  value="show__login_time_formatted" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="Logout_Time" output="Logout Time"
			  default_checked="FALSE" always_in_form="search"
			  value="show__logout_time_formatted" form_name="connections"
			  container_name="general_selected"}

{multiTableTR}
    {reportToShowCheckBox name="Duration" output="Duration"
			  default_checked="FALSE" always_in_form="search"
			  value="show__duration_seconds|duration" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="Credit_Used" output="Credit Used"
			  default_checked="FALSE" always_in_form="search"
			  value="show__credit_used|price" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="Successful" output="Successful"
			  default_checked="FALSE" always_in_form="search"
			  value="show__successful|formatBoolean" form_name="connections"
			  container_name="general_selected"}

{multiTableTR}
	    {reportToShowCheckBox name="Service" output="Service"
			  default_checked="FALSE" always_in_form="search"
			  value="show__service_type|formatServiceType" form_name="connections"
			  container_name="general_selected"}

    	{reportToShowCheckBox name="Bytes_OUT" output="Bytes OUT"
			  default_checked="FALSE" always_in_form="search"
			  value="show__details_bytes_out|byte" form_name="connections"
			  container_name="general_selected"}

	    {reportToShowCheckBox name="Bytes_IN" output="Bytes IN"
			  default_checked="FALSE" always_in_form="search"
			  value="show__details_bytes_in|byte" form_name="connections"
			  container_name="general_selected"}
	
	{multiTableTR}
		{reportToShowCheckBox name="Caller_ID" output="Caller ID"
			  default_checked="FALSE" always_in_form="search"
			  value="show__details_caller_id" form_name="connections"
			  container_name="general_selected"}

  	    {reportToShowCheckBox name="Prefix_Name" output="Prefix Name"
			  default_checked="FALSE" always_in_form="search"
			  value="show__details_prefix_name" form_name="connections"
			  container_name="general_selected"}

		{reportToShowCheckBox name="Called_Number" output="Called Number"
			  default_checked="FALSE" always_in_form="search"
			  value="show__details_called_number" form_name="connections"
			  container_name="general_selected"}
