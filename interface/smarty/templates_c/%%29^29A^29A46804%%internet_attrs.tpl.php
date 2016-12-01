<?php /* Smarty version 2.6.13, created on 2006-06-13 19:23:20
         compiled from admin/report/connection_logs/conditions/internet_attrs.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('function', 'multiTableTR', 'admin/report/connection_logs/conditions/internet_attrs.tpl', 1, false),array('function', 'reportToShowCheckBox', 'admin/report/connection_logs/conditions/internet_attrs.tpl', 2, false),)), $this); ?>
<?php echo smarty_function_multiTableTR(array(), $this);?>

    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Internet_Username','output' => 'Internet Username','default_checked' => 'FALSE','always_in_form' => 'search','value' => 'show__details_username','form_name' => 'connections','container_name' => 'internet_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Remote_IP','output' => 'Remote IP','default_checked' => 'FALSE','always_in_form' => 'connections','value' => 'show__details_remote_ip','form_name' => 'connections','container_name' => 'internet_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Station_IP','output' => 'Station IP','default_checked' => 'FALSE','always_in_form' => 'connections','value' => 'show__details_station_ip','form_name' => 'connections','container_name' => 'internet_selected'), $this);?>


<?php echo smarty_function_multiTableTR(array(), $this);?>

    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'MAC','output' => 'MAC','default_checked' => 'FALSE','always_in_form' => 'connections','value' => 'show__details_station_mac','form_name' => 'connections','container_name' => 'internet_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Bytes_IN','output' => 'Bytes IN','default_checked' => 'FALSE','always_in_form' => 'connections','value' => "show__details_bytes_in|byte",'form_name' => 'connections','container_name' => 'internet_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Bytes_OUT','output' => 'Bytes OUT','default_checked' => 'FALSE','always_in_form' => 'connections','value' => "show__details_bytes_out|byte",'form_name' => 'connections','container_name' => 'internet_selected'), $this);?>


<?php echo smarty_function_multiTableTR(array(), $this);?>

    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Assigned_IP','output' => 'IPpool Assigned IP','default_checked' => 'FALSE','always_in_form' => 'connections','value' => 'show__details_ippool_assigned_ip','form_name' => 'connections','container_name' => 'internet_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Port','output' => 'Port','default_checked' => 'FALSE','always_in_form' => 'connections','value' => 'show__details_port','form_name' => 'connections','container_name' => 'internet_selected'), $this);?>
