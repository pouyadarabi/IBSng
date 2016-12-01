<?php /* Smarty version 2.6.13, created on 2006-06-13 19:33:26
         compiled from refresh_header.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('function', 'requestToUrl', 'refresh_header.tpl', 1, false),array('function', 'html_options', 'refresh_header.tpl', 7, false),array('block', 'addEditTable', 'refresh_header.tpl', 2, false),array('block', 'addEditTD', 'refresh_header.tpl', 3, false),)), $this); ?>
<form method=get action="<?php echo smarty_function_requestToUrl(array('ignore' => 'refresh'), $this);?>
" name="refresh_form">
<?php $this->_tag_stack[] = array('addEditTable', array('title' => $this->_tpl_vars['title'],'action_icon' => 'ok','action_onclick' => "updateRefresh()")); $_block_repeat=true;smarty_block_addEditTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	Refresh Every 
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'right')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<?php echo smarty_function_html_options(array('name' => 'refresh','values' => $this->_tpl_vars['refresh_times'],'output' => $this->_tpl_vars['refresh_times'],'selected' => $this->_tpl_vars['refresh_default']), $this);?>

	Seconds <font size=1>
	(<span id="timer">_Loading_</span>
	    <a href="#" onClick="playPauseOnClick(); return false;" style="text-decoration:none">
		<img src="/IBSng/images/icon/pause.gif" border=0 id="refresh_play_pause" style="position: relative; top: 3">
	    </a>
	 seconds remaining)</font>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack);  $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
</form>

<script language=javascript>
<?php if (isInRequest ( 'refresh' )): ?>
    window.refresh=<?php echo $_REQUEST['refresh']; ?>
;
<?php else: ?>
    window.refresh=20;
<?php endif; ?>
    window.url_without_refresh='<?php echo smarty_function_requestToUrl(array('ignore' => 'refresh'), $this);?>
';
<?php echo '
	    
    addToWindowOnloads( setupRefreshCounter );

    function setupRefreshCounter()
    {
	window.refresh_timer_status="play";
	updateTimer();
    }
    
    function updateTimer()
    {
	if (window.refresh_timer_status == "play")
	{
	    window.refresh-=1;
	    span_obj=document.getElementById("timer");
    	    span_obj.childNodes[0].nodeValue=refresh;
	    if(window.refresh==0)
		window.location = window.location;
	    else	    
		setTimeout("updateTimer()",1000);
	}
	else
	    setTimeout("updateTimer()",1000);
    }

    function updateRefresh()
    {
	window.location=url_without_refresh+"&refresh="+document.refresh_form.refresh.value;
	return false;
    }

'; ?>


</script>