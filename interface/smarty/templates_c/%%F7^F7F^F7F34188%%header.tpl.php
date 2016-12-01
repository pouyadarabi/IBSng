<?php /* Smarty version 2.6.13, created on 2006-06-13 19:23:06
         compiled from header.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('modifier', 'default', 'header.tpl', 4, false),)), $this); ?>
<html>
<head>
<title>
IBSng | <?php echo ((is_array($_tmp=@$this->_tpl_vars['title'])) ? $this->_run_mod_handler('default', true, $_tmp, "") : smarty_modifier_default($_tmp, "")); ?>

</title>
<meta content="text/html; charset=UTF-8" http-equiv="content-type">
<script language="javascript" src="/IBSng/js/lib.js" language="javascript"></script>
<script language="javascript" src="/IBSng/js/dom_container.js"></script>
<script language="javascript" src="/IBSng/js/tab.js"></script>
<script language="javascript">window.DATE_TYPE='<?php echo $this->_tpl_vars['DATE_TYPE']; ?>
';</script>
<link href="/IBSng/css/IBSng_style.css" type=text/css rel="stylesheet" />
</head>