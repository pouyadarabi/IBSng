{multiTableTR}
    {reportToShowCheckBox name="Internet_Username" output="Internet Username"
			  default_checked="FALSE" always_in_form="admin_connection_logs"
		    	  value="show__details_username" form_name="connections"
		          container_name="internet_selected"}

    {reportToShowCheckBox name="Remote_IP" output="Remote IP"
			  default_checked="FALSE" always_in_form="admin_connection_logs"
			  value="show__details_remote_ip" form_name="connections"
			  container_name="internet_selected"}

    {reportToShowCheckBox name="Station_IP" output="Station IP"
			  default_checked="FALSE" always_in_form="admin_connection_logs"
			  value="show__details_station_ip" form_name="connections"
			  container_name="internet_selected"}

{multiTableTR}
    {reportToShowCheckBox name="MAC" output="MAC"
			  default_checked="FALSE" always_in_form="admin_connection_logs"
			  value="show__details_station_mac" form_name="connections"
			  container_name="internet_selected"}

    {reportToShowCheckBox name="Bytes_IN" output="Bytes IN"
			  default_checked="FALSE" always_in_form="admin_connection_logs"
			  value="show__details_bytes_in|byte" form_name="connections"
			  container_name="internet_selected"}

    {reportToShowCheckBox name="Bytes_OUT" output="Bytes OUT"
			  default_checked="FALSE" always_in_form="admin_connection_logs"
			  value="show__details_bytes_out|byte" form_name="connections"
			  container_name="internet_selected"}

{multiTableTR}
    {reportToShowCheckBox name="Assigned_IP" output="IPpool Assigned IP"
			  default_checked="FALSE" always_in_form="admin_connection_logs"
			  value="show__details_ippool_assigned_ip" form_name="connections"
			  container_name="internet_selected"}

    {reportToShowCheckBox name="Port" output="Port"
			  default_checked="FALSE" always_in_form="admin_connection_logs"
			  value="show__details_port" form_name="connections"
			  container_name="internet_selected"}
