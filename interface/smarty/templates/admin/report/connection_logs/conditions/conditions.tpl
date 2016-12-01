{tabTable tabs="Conditions,General,Internet,VoIP,Rases" content_height=50 table_width=675 action_icon="search" form_name="connections"}

    {tabContent add_table_tag=TRUE tab_name="Conditions"}
		{include file = "admin/report/connection_logs/conditions/search_options.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="General"}
	{include file	= "admin/report/skel_conditions.tpl"
		 name		= "general"
		 form_name	= "connections"
		 inc 		= "admin/report/connection_logs/conditions/general_attrs.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="Internet"}
	{include file	= "admin/report/skel_conditions.tpl"
		 name		= "internet"
 		 form_name	= "connections"
		 inc  		= "admin/report/connection_logs/conditions/internet_attrs.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="VoIP"}
	{include file	= "admin/report/skel_conditions.tpl"
		 name		= "voip"
 		 form_name	= "connections"
		 inc  		= "admin/report/connection_logs/conditions/voip_attrs.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="Rases"}
		 {include file="admin/report/connection_logs/conditions/rases_attrs.tpl"}
    {/tabContent}

{/tabTable}
