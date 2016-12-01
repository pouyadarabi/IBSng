{tabTable tabs="Conditions,Attributes" content_height=50 table_width=675 action_icon="search" form_name="connections"}

    {tabContent add_table_tag=TRUE tab_name="Conditions"}
		{include file		= "user/en/conditions/conditions.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="Attributes"}
		{include file		= "admin/report/skel_conditions.tpl"
				 name		= "general"
				 title		= "Attributes To Show"
				 form_name	= "connections"
				 inc		= "user/en/conditions/general_attrs.tpl"}
    {/tabContent}

{/tabTable}
