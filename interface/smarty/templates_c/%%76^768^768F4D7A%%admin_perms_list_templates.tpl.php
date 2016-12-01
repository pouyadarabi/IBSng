<?php /* Smarty version 2.6.13, created on 2006-06-17 12:51:29
         compiled from admin/admins/admin_perms_list_templates.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'addEditTable', 'admin/admins/admin_perms_list_templates.tpl', 2, false),array('block', 'addEditTD', 'admin/admins/admin_perms_list_templates.tpl', 3, false),array('function', 'html_options', 'admin/admins/admin_perms_list_templates.tpl', 28, false),)), $this); ?>
<form method=POST action="admin_perms_list.php">
    <?php $this->_tag_stack[] = array('addEditTable', array('title' => 'Save Permission Template','table_width' => '400','action_icon' => 'save')); $_block_repeat=true;smarty_block_addEditTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?> 
        <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    Save This Admin Permissions into template:
        <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $this->_tag_stack[] = array('addEditTD', array('type' => 'right')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <input class="text" type=text name=template_name>
	    <input type=hidden name=action value=save>
	    <input type=hidden name=admin_username value=<?php echo $this->_tpl_vars['admin_username']; ?>
>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
</form>
<form method=POST action="admin_perms_list.php" name="load_template">
    <?php $this->_tag_stack[] = array('addEditTable', array('title' => "Load Permission Template Into ".($this->_tpl_vars['admin_username']),'table_width' => '400','action_icon' => 'load')); $_block_repeat=true;smarty_block_addEditTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
        <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    Load Permission Template into admin:
        <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $this->_tag_stack[] = array('addEditTD', array('type' => 'right')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <?php echo '
	    <script language="javascript">
		function showTemplatePerms(){
		    selected=getSelectedOption("load_template","template_name");
		    open("show_permtemplate_perms.php?template_name="+selected,"template_perms","width=500,height=400,scrollbars=yes");
		}
	    </script>
	    '; ?>

	    <select name=template_name>
		<?php echo smarty_function_html_options(array('values' => $this->_tpl_vars['templates_list'],'output' => $this->_tpl_vars['templates_list']), $this);?>

	    </select> <a class="link_in_body" href="javascript:showTemplatePerms();">Show Permissions</a>
	    <input type=hidden name=action value=load>
	    <input type=hidden name=admin_username value=<?php echo $this->_tpl_vars['admin_username']; ?>
>

	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
</form>
<form method=POST action="admin_perms_list.php" name="del_template">
    <?php $this->_tag_stack[] = array('addEditTable', array('title' => 'Delete Permission Template','table_width' => '400','action_icon' => 'delete')); $_block_repeat=true;smarty_block_addEditTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
        <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    Delete Permission Template
        <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
	<?php $this->_tag_stack[] = array('addEditTD', array('type' => 'right')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	    <select name=template_name>
		<?php echo smarty_function_html_options(array('values' => $this->_tpl_vars['templates_list'],'output' => $this->_tpl_vars['templates_list']), $this);?>

	    </select>
	    <input type=hidden name=action value=delete>
	    <input type=hidden name=admin_username value=<?php echo $this->_tpl_vars['admin_username']; ?>
>
	<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?> 
</form>

	    