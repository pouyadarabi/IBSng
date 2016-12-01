{multiTableTR}
    {reportToShowCheckBox name="Username" output="نام کاربر"
			  default_checked="FALSE" always_in_form="search"
			  value="show__details_username" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="Login_Time" output="زمان شروع اتصال"
			  default_checked="FALSE" always_in_form="search"
			  value="show__login_time_formatted" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="Logout_Time" output="زمان خاتمه اتصال"
			  default_checked="FALSE" always_in_form="search"
			  value="show__logout_time_formatted" form_name="connections"
			  container_name="general_selected"}

{multiTableTR}
    {reportToShowCheckBox name="Duration" output="مدت زمان اتصال"
			  default_checked="FALSE" always_in_form="search"
			  value="show__duration_seconds|duration" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="Credit_Used" output="اعتبار استفاده شده"
			  default_checked="FALSE" always_in_form="search"
			  value="show__credit_used|price" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="Successful" output="موفقیت اتصال"
			  default_checked="FALSE" always_in_form="search"
			  value="show__successful|formatBoolean" form_name="connections"
			  container_name="general_selected"}

{multiTableTR}
    {reportToShowCheckBox name="Service" output="نوع سرویس"
			  default_checked="FALSE" always_in_form="search"
			  value="show__service_type|formatServiceType" form_name="connections"
			  container_name="general_selected"}

   	{reportToShowCheckBox name="Bytes_IN" output="بایت های خروجی"
			  default_checked="FALSE" always_in_form="search"
			  value="show__details_bytes_out|byte" form_name="connections"
			  container_name="general_selected"}

    {reportToShowCheckBox name="Bytes_OUT" output="بایت های ورودی"
			  default_checked="FALSE" always_in_form="search"
			  value="show__details_bytes_in|byte" form_name="connections"
			  container_name="general_selected"}

{multiTableTR}
    {reportToShowCheckBox name="Caller_ID" output="شماره گیرنده"
			  default_checked="FALSE" always_in_form="search"
			  value="show__details_caller_id" form_name="connections"
			  container_name="general_selected"}

   	{reportToShowCheckBox name="Prefix_Name" output="نام پیشوند"
			  default_checked="FALSE" always_in_form="search"
			  value="show__details_prefix_name" form_name="connections"
			  container_name="general_selected"}

	{reportToShowCheckBox name="Called_Number" output="شماره مقصد"
			  default_checked="FALSE" always_in_form="search"
			  value="show__details_called_number" form_name="connections"
			  container_name="general_selected"}
