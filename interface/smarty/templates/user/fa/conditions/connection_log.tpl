{tabTable tabs="شرایط,متغییرها" content_height=50 table_width=675 action_icon="search" form_name="connections"}

    {tabContent add_table_tag=TRUE tab_name="شرایط"}
		{include file = "user/fa/conditions/conditions.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="متغییرها"}
		{include file		= "admin/report/skel_conditions.tpl"
				 name		= "general"
				 title		= "متغییر های نمایش"
				 form_name	= "connections"
				 inc		= "user/fa/conditions/general_attrs.tpl"}
    {/tabContent}

{/tabTable}
