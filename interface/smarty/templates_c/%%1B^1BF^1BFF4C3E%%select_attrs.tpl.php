<?php /* Smarty version 2.6.13, created on 2006-06-17 13:10:52
         compiled from admin/user/search_user/select_attrs.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('function', 'multiTableTR', 'admin/user/search_user/select_attrs.tpl', 1, false),array('function', 'reportToShowCheckBox', 'admin/user/search_user/select_attrs.tpl', 2, false),)), $this); ?>
 <?php echo smarty_function_multiTableTR(array(), $this);?>

	<?php echo smarty_function_reportToShowCheckBox(array('name' => 'Internet_Username','output' => 'Internet Username','default_checked' => 'TRUE','always_in_form' => 'search','value' => 'show__attrs_normal_username','form_name' => 'search_user','container_name' => 'attrs_selected'), $this);?>


	<?php echo smarty_function_reportToShowCheckBox(array('name' => 'VoIP_Username','output' => 'VoIP Username','default_checked' => 'TRUE','always_in_form' => 'search','value' => 'show__attrs_voip_username','form_name' => 'search_user','container_name' => 'attrs_selected'), $this);?>


	<?php echo smarty_function_reportToShowCheckBox(array('name' => 'Credit','output' => 'Credit','default_checked' => 'TRUE','always_in_form' => 'search','value' => "show__basic_credit|price",'form_name' => 'search_user','container_name' => 'attrs_selected'), $this);?>


<?php echo smarty_function_multiTableTR(array(), $this);?>

    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Group','output' => 'Group','default_checked' => 'TRUE','always_in_form' => 'search','value' => 'show__basic_group_name','form_name' => 'search_user','container_name' => 'attrs_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Owner','output' => 'Owner','default_checked' => 'TRUE','always_in_form' => 'search','value' => 'show__basic_owner_name','form_name' => 'search_user','container_name' => 'attrs_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Creation_Date','output' => 'Creation Date','default_checked' => 'FALSE','always_in_form' => 'search','value' => 'show__basic_creation_date','form_name' => 'search_user','container_name' => 'attrs_selected'), $this);?>


<?php echo smarty_function_multiTableTR(array(), $this);?>

	<?php echo smarty_function_reportToShowCheckBox(array('name' => 'Relative_ExpDate','output' => 'Relative ExpDate','default_checked' => 'FALSE','always_in_form' => 'search','value' => "show__attrs_rel_exp_date,show__attrs_rel_exp_date_unit",'form_name' => 'search_user','container_name' => 'attrs_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Absolute_ExpDate','output' => 'Absolute ExpDate','default_checked' => 'FALSE','always_in_form' => 'search','value' => 'show__attrs_abs_exp_date','form_name' => 'search_user','container_name' => 'attrs_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Multi_Login','output' => 'Multi Login','default_checked' => 'FALSE','always_in_form' => 'search','value' => 'show__attrs_multi_login','form_name' => 'search_user','container_name' => 'attrs_selected'), $this);?>


<?php echo smarty_function_multiTableTR(array(), $this);?>

    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Normal_Charge','output' => 'Normal Charge','default_checked' => 'FALSE','always_in_form' => 'search','value' => 'show__attrs_normal_charge','form_name' => 'search_user','container_name' => 'attrs_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'VoIP_Charge','output' => 'VoIP Charge','default_checked' => 'FALSE','always_in_form' => 'search','value' => 'show__attrs_voip_charge','form_name' => 'search_user','container_name' => 'attrs_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Lock','output' => 'Lock Status','default_checked' => 'FALSE','always_in_form' => 'search','value' => "show__attrs_lock|lockFormat",'form_name' => 'search_user','container_name' => 'attrs_selected'), $this);?>
