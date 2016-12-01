{listTable title="Internet Online Users" cols_num=13}
    {listTableHeaderIcon action="kick"}
    {listTableHeaderIcon action="clear"}
    {listTableHeaderIcon action="graph"}
    {listTableHeaderIcon action="history"}
    {listTableHeaderIcon action="details" close_tr=TRUE}
    {listTR type="header"}
	{listTD}
	    Row
	{/listTD}

	{listTD}
	    {sortableHeader name="user_id"} 
		User ID
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader name="normal_username"} 
		Username
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader name="login_time_epoch" default=TRUE default_desc=TRUE}
		Login Time
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader name="duration_secs"}
		Duration
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader name="current_credit"} 
		Credit
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader name="ras_description"} 
		Ras
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader name="unique_id_val"} 
	        Port/ID
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader name="in_bytes"} 
		In Bytes
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader name="out_bytes"} 
		Out Bytes
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader name="in_rate"} 
		In Rate
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader name="out_rate"} 
		Out Rate
	    {/sortableHeader}
	{/listTD}

	{listTD}
	    {sortableHeader name="owner_name"} 
		Owner
	    {/sortableHeader}
	{/listTD}
    {/listTR}
    {assign var="index" value=1}

    {foreach from=$internet_onlines item=info_dic}
	{listTR type="body" hover_location="/IBSng/admin/user/user_info.php?user_id=`$info_dic.user_id`" }

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
		{$info_dic.normal_username}
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
		{$info_dic.unique_id_val|truncate:8:"...":true}
	    {/listTD}

	    {listTD}
		{$info_dic.in_bytes|byte}
	    {/listTD}

	    {listTD}
		{$info_dic.out_bytes|byte}
	    {/listTD}


	    {listTD}
		{$info_dic.in_rate|byte}
	    {/listTD}

	    {listTD}
		{$info_dic.out_rate|byte}
	    {/listTD}

	    {listTD}
		{$info_dic.owner_name}
	    {/listTD}

	    {listTD icon=TRUE extra="onClick='event.cancelBubble=true;'"}
		    <a style="text-decoration:none" href="javascript: killUser('{$info_dic.user_id}','{$info_dic.normal_username}','{$info_dic.ras_ip}','{$info_dic.unique_id_val}',true);" {jsconfirm}>
			{listTableBodyIcon action="kick" cycle_color="TRUE"}
		    </a>
	    {/listTD}

	    {listTD icon=TRUE extra="onClick='event.cancelBubble=true;'"}
		    <a style="text-decoration:none" href="javascript: killUser('{$info_dic.user_id}','{$info_dic.normal_username}','{$info_dic.ras_ip}','{$info_dic.unique_id_val}',false);" {jsconfirm}>
			{listTableBodyIcon action="clear"}
		    </a>
	    {/listTD}

	    {listTD icon=TRUE extra="onClick='event.cancelBubble=true;'" }
		    <a style="text-decoration:none" href="/IBSng/admin/graph/realtime/realtime.php?img_url=bw.php?username={$info_dic.normal_username}%26user_id={$info_dic.user_id}%26ras_ip={$info_dic.ras_ip}%26unique_id_val={$info_dic.unique_id_val}">
			{listTableBodyIcon action="graph"}
		    </a>
	    {/listTD}

	    {listTD icon=TRUE extra="onClick='event.cancelBubble=true;'" }
		    <a style="text-decoration:none" href="/IBSng/admin/report/realtime_web_analyzer.php?username={$info_dic.normal_username}&user_id={$info_dic.user_id}">
			{listTableBodyIcon action="history"}
		    </a>
	    {/listTD}

	    {listTD icon=TRUE extra="onClick='event.cancelBubble=true;'" }
		    
		<a onClick="showReportLayer('{$info_dic.ras_ip}_{$info_dic.unique_id_val}',this); return false;" href="#">
		    {listTableBodyIcon action="details"}
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
