<?php /* Smarty version 2.6.13, created on 2006-06-13 19:23:06
         compiled from err_head.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('modifier', 'escape', 'err_head.tpl', 10, false),)), $this); ?>
<?php if (isset ( $this->_tpl_vars['err_msgs'] ) || isInRequest ( 'err_msg' )): ?>
<table align=center border=0>
<?php if (isset ( $this->_tpl_vars['err_msgs'] )): ?>
    <?php $_from = $this->_tpl_vars['err_msgs']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }if (count($_from)):
    foreach ($_from as $this->_tpl_vars['err']):
?>
	<tr>
	    <td align=left>
		<img border="0" src="/IBSng/images/msg/before_error_message.gif">
	    </td>
	    <td align=left class="error_messages">	    
		<?php echo ((is_array($_tmp=$this->_tpl_vars['err'])) ? $this->_run_mod_handler('escape', true, $_tmp, 'html') : smarty_modifier_escape($_tmp, 'html')); ?>

	    </td>
	</tr>
    <?php endforeach; endif; unset($_from);  endif;  if (isInRequest ( 'err_msg' )): ?>
	<tr>
	    <td align=left>
		<img border="0" src="/IBSng/images/msg/before_error_message.gif">
	    </td>
	    <td align=left class="error_messages">	    
		<?php echo ((is_array($_tmp=$_REQUEST['err_msg'])) ? $this->_run_mod_handler('escape', true, $_tmp, 'html') : smarty_modifier_escape($_tmp, 'html')); ?>

	    </td>
	</tr>
<?php endif; ?>
</table>
<br>
<?php endif; ?>