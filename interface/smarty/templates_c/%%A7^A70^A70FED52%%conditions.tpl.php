<?php /* Smarty version 2.6.13, created on 2006-07-18 14:41:46
         compiled from admin/report/connection_logs/conditions/conditions.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'tabTable', 'admin/report/connection_logs/conditions/conditions.tpl', 1, false),array('block', 'tabContent', 'admin/report/connection_logs/conditions/conditions.tpl', 3, false),)), $this); ?>
<?php $this->_tag_stack[] = array('tabTable', array('tabs' => "Conditions,General,Internet,VoIP,Rases",'content_height' => 50,'table_width' => 675,'action_icon' => 'search','form_name' => 'connections')); $_block_repeat=true;smarty_block_tabTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>

    <?php $this->_tag_stack[] = array('tabContent', array('add_table_tag' => 'TRUE','tab_name' => 'Conditions')); $_block_repeat=true;smarty_block_tabContent($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin/report/connection_logs/conditions/search_options.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_tabContent($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('tabContent', array('add_table_tag' => 'TRUE','tab_name' => 'General')); $_block_repeat=true;smarty_block_tabContent($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin/report/skel_conditions.tpl", 'smarty_include_vars' => array('name' => 'general','form_name' => 'connections','inc' => "admin/report/connection_logs/conditions/general_attrs.tpl")));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_tabContent($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('tabContent', array('add_table_tag' => 'TRUE','tab_name' => 'Internet')); $_block_repeat=true;smarty_block_tabContent($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin/report/skel_conditions.tpl", 'smarty_include_vars' => array('name' => 'internet','form_name' => 'connections','inc' => "admin/report/connection_logs/conditions/internet_attrs.tpl")));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_tabContent($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('tabContent', array('add_table_tag' => 'TRUE','tab_name' => 'VoIP')); $_block_repeat=true;smarty_block_tabContent($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin/report/skel_conditions.tpl", 'smarty_include_vars' => array('name' => 'voip','form_name' => 'connections','inc' => "admin/report/connection_logs/conditions/voip_attrs.tpl")));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_tabContent($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('tabContent', array('add_table_tag' => 'TRUE','tab_name' => 'Rases')); $_block_repeat=true;smarty_block_tabContent($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
		 <?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin/report/connection_logs/conditions/rases_attrs.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_tabContent($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_tabTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>