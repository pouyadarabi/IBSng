{* Charge Info
    Shows one charge information, including charge rules
    on fatal errors that no info can be shown, client is redirected to admin_list
    else error is shown on top of page
    
    Variables:
    $is_editing
    
    $charge_name
    $charge_id
    $charge_types
    $charge_type
    $visible_to_all_checked
    $visible_to_all
    $creator
    $comment
    
*}
{include file="admin_header.tpl" title="Charge Information" selected="Charge"}
{include file="err_head.tpl"}

{headerMsg var_name="update_success"}
	Charge Updated Successfully.
{/headerMsg}

{headerMsg var_name="del_charge_rule_success"}
	Charge Rule Deleted Successfully.
{/headerMsg}

{headerMsg var_name="update_charge_rule_success"}
	Charge Rule Updated Successfully.
{/headerMsg}

{if $is_editing}
    <form action="/IBSng/admin/charge/charge_info.php" method=POST>
    <input name=charge_id value="{$charge_id}" type=hidden>
    <input name=old_charge_name value="{$charge_name}" type=hidden>
    	{addEditTable title="Charge Information" double="TRUE"}
	    {addEditTD type="left1" double="TRUE"}
		    Charge Name
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
		<input class="text" type=text name=charge_name value="{$charge_name}">
	    {/addEditTD}
	    {addEditTD type="left2" double="TRUE"}
	    	    Charge ID
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
		    {$charge_id}
	    {/addEditTD}
	    {addEditTD type="left1" double="TRUE"}
		    Charge Type
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
		    {$charge_type}
	    {/addEditTD}
	    {addEditTD type="left2" double="TRUE"} 
	    	    Visible To All
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
		    <input class="checkbox" type=checkbox name=visible_to_all {$visible_to_all_checked}>{/addEditTD}
	    {addEditTD type="left1" double="TRUE"}
		    Creator Admin
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
		    {$creator}
	    {/addEditTD}
	    {addEditTD type="left2"  double="TRUE"}
		    
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
		    
	    {/addEditTD}
	    {addEditTD type="left" comment="TRUE" double="TRUE"}
	    	    Comment
	    {/addEditTD}
	    {addEditTD type="right" comment="TRUE" double="TRUE"}
		    <textarea class="text" name=comment>{$comment|strip}</textarea>
	    {/addEditTD}
	{/addEditTable}
</form>
{else}
	{viewTable title="Charge Information" double="TRUE"}
	    {addEditTD type="left1" double="TRUE"}
		    Charge Name
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
		{$charge_name}
	    {/addEditTD}
	    {addEditTD type="left2" double="TRUE"}
	    	    Charge ID
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
		    {$charge_id}
	    {/addEditTD}
	    {addEditTD type="left1" double="TRUE"}
		    Charge Type
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
		    {$charge_type}
	    {/addEditTD}
	    {addEditTD type="left2" double="TRUE"} 
	    	    Visible To All
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
		    {$visible_to_all}
	    {/addEditTD}
	    {addEditTD type="left1" double="TRUE"}
		    Creator Admin
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
		    {$creator}
	    {/addEditTD}
	    {addEditTD type="left2"  double="TRUE"}
		    
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
		    
	    {/addEditTD}
	    {addEditTD type="left" comment="TRUE" double="TRUE"}
	    	    Comment
	    {/addEditTD}
	    {addEditTD type="right" comment="TRUE" double="TRUE"}
		    {$comment}
	    {/addEditTD}
	{/viewTable}
{/if}
{if $charge_type eq "Internet"}
	{include file="admin/charge/internet_charge_rule_list.tpl"}
    {else}
	{include file="admin/charge/voip_charge_rule_list.tpl"}
{/if}

{if !$is_editing and  $can_change}
    {addRelatedLink}
	{if $charge_type eq "Internet"}
    	    <a href="/IBSng/admin/charge/{if $charge_type eq "Internet"}add_internet_charge_rule{else}add_voip_charge_rule{/if}.php?charge_name={$charge_name|escape:"url"}" class="RightSide_links">
        	Add Internet Charge Rule
    	    </a>
	{else}
    	    <a href="/IBSng/admin/charge/{if $charge_type eq "Internet"}add_internet_charge_rule{else}add_voip_charge_rule{/if}.php?charge_name={$charge_name|escape:"url"}" class="RightSide_links">
        	Add VoIP Charge Rule
    	    </a>
	{/if}

    {/addRelatedLink}

    {addRelatedLink}
        <a href="/IBSng/admin/charge/charge_info.php?charge_name={$charge_name|escape:"url"}&edit=1" class="RightSide_links">
        	Edit Charge Information
        </a>
    {/addRelatedLink}

    {addRelatedLink}
        <a href="/IBSng/admin/charge/charge_info.php?delete_charge=1&charge_name={$charge_name|escape:"url"}" 
		{jsconfirm msg="Are you sure you want to delete Charge?\\n Warning: You should remove charge from groups and users attributes first"}
		 class="RightSide_links">
	    Delete Charge <b>{$charge_name}</b>
	</a>
    {/addRelatedLink}


{/if}
    {addRelatedLink}
        <a href="/IBSng/admin/charge/charge_list.php" class="RightSide_links">
        	Charge List
        </a>
    {/addRelatedLink}

    {addRelatedLink}
        <a href="/IBSng/admin/charge/add_new_charge.php" class="RightSide_links">
        	Add New Charge 
        </a>
    {/addRelatedLink}

    {addRelatedLink}
	{if $charge_type eq "Internet"}
		<a href="/IBSng/admin/user/search_user.php?search=1&show_defaults=1&normal_charge_{$charge_name}={$charge_name}&tab1_selected=Charge" class="RightSide_links">
		    Users With Charge <b>{$charge_name}</b>
		</a>
	{else}
		<a href="/IBSng/admin/user/search_user.php?search=1&show_defaults=1&voip_charge_{$charge_name}={$charge_name}&tab1_selected=Charge" class="RightSide_links">
		    Users With Charge <b>{$charge_name}</b>
		</a>
	{/if}

    {/addRelatedLink}




{setAboutPage title="Charge Information"}

{/setAboutPage}

{include file="admin_footer.tpl"}
