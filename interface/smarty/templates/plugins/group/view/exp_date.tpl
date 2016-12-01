{viewTable title="Expiration Date" nofoot="TRUE"}
    {addEditTD type="left" open_tr="FALSE"}
	{if $can_change}{editCheckBox edit_tpl_name="rel_exp_date"}{/if}Relative Expiration Date 
    {/addEditTD}
    {addEditTD type="right"}
		{ifHasAttr object="group" var_name="rel_exp_date"}
		    {$group_attrs.rel_exp_date} {$group_attrs.rel_exp_date_unit} 
		{/ifHasAttr}
		{helpicon subject="relative expiration date" category="user"}		
    {/addEditTD}

    {addEditTD type="left" open_tr="FALSE"}
	{if $can_change}{editCheckBox edit_tpl_name="abs_exp_date"}{/if}Absolute Expiration Date 
    {/addEditTD}
    {addEditTD type="right"}
		{ifHasAttr object="group" var_name="abs_exp_date"}
		    {$group_attrs.abs_exp_date}
		{/ifHasAttr}
		{helpicon subject="absolute expiration date" category="user"}		
    {/addEditTD}
{/viewTable}

