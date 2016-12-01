<?php /* Smarty version 2.6.13, created on 2006-06-13 19:23:20
         compiled from admin/report/connection_logs/conditions/general_attrs.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('function', 'multiTableTR', 'admin/report/connection_logs/conditions/general_attrs.tpl', 1, false),array('function', 'reportToShowCheckBox', 'admin/report/connection_logs/conditions/general_attrs.tpl', 2, false),)), $this); ?>
<?php echo smarty_function_multiTableTR(array(), $this);?>

    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Username','output' => 'Username','default_checked' => 'TRUE','always_in_form' => 'search','value' => 'show__details_any_username','form_name' => 'connections','container_name' => 'general_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Credit','output' => 'Credit','default_checked' => 'TRUE','always_in_form' => 'search','value' => "show__credit_used|price",'form_name' => 'connections','container_name' => 'general_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Login_Time','output' => 'Login Time','default_checked' => 'TRUE','always_in_form' => 'search','value' => 'show__login_time_formatted','form_name' => 'connections','container_name' => 'general_selected'), $this);?>



<?php echo smarty_function_multiTableTR(array(), $this);?>

    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Logout_Time','output' => 'Logout Time','default_checked' => 'TRUE','always_in_form' => 'search','value' => 'show__logout_time_formatted','form_name' => 'connections','container_name' => 'general_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Duration','output' => 'Duration','default_checked' => 'TRUE','always_in_form' => 'search','value' => "show__duration_seconds|duration",'form_name' => 'connections','container_name' => 'general_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Successful','output' => 'Successful','default_checked' => 'TRUE','always_in_form' => 'search','value' => "show__successful|formatBoolean",'form_name' => 'connections','container_name' => 'general_selected'), $this);?>


<?php echo smarty_function_multiTableTR(array(), $this);?>

    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Service','output' => 'Service','default_checked' => 'TRUE','always_in_form' => 'search','value' => "show__service_type|formatServiceType",'form_name' => 'connections','container_name' => 'general_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'RAS','output' => 'RAS','default_checked' => 'TRUE','always_in_form' => 'connections','value' => 'show__ras_description','form_name' => 'connections','container_name' => 'general_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Caller_ID','output' => 'Caller ID','default_checked' => 'FALSE','always_in_form' => 'connections','value' => 'show__details_caller_id','form_name' => 'connections','container_name' => 'general_selected'), $this);?>
