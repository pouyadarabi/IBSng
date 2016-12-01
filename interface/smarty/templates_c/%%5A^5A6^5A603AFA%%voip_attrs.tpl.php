<?php /* Smarty version 2.6.13, created on 2006-06-13 19:23:20
         compiled from admin/report/connection_logs/conditions/voip_attrs.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('function', 'multiTableTR', 'admin/report/connection_logs/conditions/voip_attrs.tpl', 1, false),array('function', 'reportToShowCheckBox', 'admin/report/connection_logs/conditions/voip_attrs.tpl', 2, false),)), $this); ?>
<?php echo smarty_function_multiTableTR(array(), $this);?>

    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'VoIP_Username','output' => 'VoIP Username','default_checked' => 'FALSE','always_in_form' => 'connections','value' => 'show__details_voip_username','form_name' => 'connections','container_name' => 'voip_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Called_Number','output' => 'Called Number','default_checked' => 'FALSE','always_in_form' => 'connections','value' => 'show__details_called_number','form_name' => 'connections','container_name' => 'voip_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Called_IP','output' => 'Called IP','default_checked' => 'FALSE','always_in_form' => 'connections','value' => 'show__details_called_ip','form_name' => 'connections','container_name' => 'voip_selected'), $this);?>


<?php echo smarty_function_multiTableTR(array(), $this);?>

    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Prefix_Name','output' => 'Prefix Name','default_checked' => 'FALSE','always_in_form' => 'connections','value' => 'show__details_prefix_name','form_name' => 'connections','container_name' => 'voip_selected'), $this);?>


    <?php echo smarty_function_reportToShowCheckBox(array('name' => 'Conf_ID','output' => 'Conf ID','default_checked' => 'FALSE','always_in_form' => 'connections','value' => 'show__details_conf_id','form_name' => 'connections','container_name' => 'voip_selected'), $this);?>
