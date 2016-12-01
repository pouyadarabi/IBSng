{listTable title="VoIP Online Users" cols_num=11}
    {listTableHeaderIcon action="kick"}
    {listTableHeaderIcon action="clear"}
    {listTableHeaderIcon action="details" close_tr=TRUE}
    {listTR type="header"}
	{listTD}
	    Row
	{/listTD}

	{listTD}
	    {sortableHeader order_by_key="voip_order_by" desc_key="voip_desc" name="user_id"} 
		User ID
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader order_by_key="voip_order_by" desc_key="voip_desc" name="voip_username"} 
		Username
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader order_by_key="voip_order_by" desc_key="voip_desc" name="login_time_epoch" default=TRUE default_desc=TRUE}
		Call Start Time
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader order_by_key="voip_order_by" desc_key="voip_desc" name="duration_secs"}
		Duration
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader order_by_key="voip_order_by" desc_key="voip_desc" name="current_credit"} 
		Credit
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader order_by_key="voip_order_by" desc_key="voip_desc" name="ras_description"} 
		Ras
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader order_by_key="voip_order_by" desc_key="voip_desc" name="unique_id_val"} 
	        Port/ID
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader order_by_key="voip_order_by" desc_key="voip_desc" name="called_number"} 
		Called Number
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader order_by_key="voip_order_by" desc_key="voip_desc" name="prefix_name"} 
		Prefix Name
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader order_by_key="voip_order_by" desc_key="voip_desc" name="owner_name"} 
		Owner
	    {/sortableHeader}
	{/listTD}
    {/listTR}
    {assign var="index" value=1}

    {foreach from=$voip_onlines item=info_dic}
	
	{listTR type="body" hover_location="/IBSng/admin/user/user_info.php?user_id=`$info_dic.user_id`"}
	    {listTD}
		{$index}
		{math equation="index+1" index=$index assign="index"}
	    {/listTD}

	    {listTD}
		<a href="/IBSng/admin/user/user_info.php?user_id={$info_dic.user_id}" class="link_in_body">
		    {$info_dic.user_id}
		</a>
	    {/listTD}

	    {listTD}
		{$info_dic.voip_username}
	    {/listTD}

	    {listTD}
		{$info_dic.login_time}
	    {/listTD}

	    {listTD}
		{$info_dic.duration_secs|duration}
	    {/listTD}

	    {listTD}
		{$info_dic.current_credit|price}
	    {/listTD}


	    {listTD}
		{$info_dic.ras_description}
	    {/listTD}

	    {listTD}
		{$info_dic.unique_id_val|truncate:20}
	    {/listTD}

	    {listTD}
		{$info_dic.called_number}
	    {/listTD}

	    {listTD}
		{$info_dic.prefix_name}
	    {/listTD}

	    {listTD}
		{$info_dic.owner_name}
	    {/listTD}

	    {listTD icon=TRUE extra="onClick='event.cancelBubble=true;'"}
		    <a style="text-decoration:none" href="javascript: killUser('{$info_dic.user_id}','{$info_dic.voip_username}','{$info_dic.ras_ip}','{$info_dic.unique_id_val}',true);" {jsconfirm}>
			{listTableBodyIcon action="kick" cycle_color="TRUE"}
		    </a>
	    {/listTD}

	    {listTD icon=TRUE extra="onClick='event.cancelBubble=true;'"}
		    <a style="text-decoration:none" href="javascript: killUser('{$info_dic.user_id}','{$info_dic.voip_username}','{$info_dic.ras_ip}','{$info_dic.unique_id_val}',false);" {jsconfirm}>
			{listTableBodyIcon action="clear" }
		    </a>
	    {/listTD}

	    {listTD icon=TRUE extra="onClick='event.cancelBubble=true;'"}
		    
		<a onClick="showReportLayer('{$info_dic.ras_ip}_{$info_dic.unique_id_val}',this); return false;" href="#">
		    {listTableBodyIcon action="details" }
		</a>
		{reportDetailLayer name=`$info_dic.ras_ip`_`$info_dic.unique_id_val` title="Report Details"}
		    {layerTable}
		    {foreach from=`$info_dic.attrs` key=key item=item}
    			{layerTR cycle_color=TRUE}
			    {listTD}
				{$key}
	    		    {/listTD}
			    {listTD}
				{$item}
	    		    {/listTD}
			{/layerTR}
		    {/foreach}
		    {/layerTable}
		{/reportDetailLayer}
	    {/listTD}
	{/listTR}
	
    {/foreach}

{/listTable}
