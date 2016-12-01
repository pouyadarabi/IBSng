{multiTableTR}
    {reportToShowCheckBox name="Date" output="Date"
			  default_checked="TRUE" always_in_form="web_analyzer_logs"
			  value="show__date_formatted" form_name="web_analyzer_logs"
			  container_name="web_analyzer_logs_selected"}

    {reportToShowCheckBox name="User_ID" output="User ID"
			  default_checked="TRUE" always_in_form="web_analyzer_logs"
			  value="show__user_id" form_name="web_analyzer_logs"
			  container_name="web_analyzer_logs_selected"}

    {reportToShowCheckBox name="User_Name" output="User Name"
			  default_checked="TRUE" always_in_form="web_analyzer_logs"
			  value="show__username" form_name="web_analyzer_logs"
			  container_name="web_analyzer_logs_selected"}

{multiTableTR}
    {reportToShowCheckBox name="Target_URL" output="Target URL"
			  default_checked="TRUE" always_in_form="web_analyzer_logs"
			  value="show__url|formatWebAnalyzerLogsURL:60:true" form_name="web_analyzer_logs"
			  container_name="web_analyzer_logs_selected"}

    {reportToShowCheckBox name="Bytes" output="Bytes"
			  default_checked="TRUE" always_in_form="web_analyzer_logs"
			  value="show__bytes|byte" form_name="web_analyzer_logs"
			  container_name="web_analyzer_logs_selected"}

    {reportToShowCheckBox name="Miss_slash_Hit" output="Miss / Hit"
			  default_checked="TRUE" always_in_form="web_analyzer_logs"
			  value="show__miss,show__slash,show__hit" form_name="web_analyzer_logs"
			  container_name="web_analyzer_logs_selected"}

{multiTableTR}
    {reportToShowCheckBox name="Successe_slash_Fail" output="Success / Fail"
			  default_checked="TRUE" always_in_form="web_analyzer_logs"
			  value="show__successful,show__slash,show__failure" form_name="web_analyzer_logs"
			  container_name="web_analyzer_logs_selected"}
