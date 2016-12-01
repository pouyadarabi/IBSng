<?php /* Smarty version 2.6.13, created on 2006-06-14 18:37:34
         compiled from admin/report/realtime_log_console.tpl */ ?>
<?php require_once(SMARTY_CORE_DIR . 'core.load_plugins.php');
smarty_core_load_plugins(array('plugins' => array(array('block', 'viewTable', 'admin/report/realtime_log_console.tpl', 21, false),array('block', 'addEditTD', 'admin/report/realtime_log_console.tpl', 22, false),array('block', 'addRelatedLink', 'admin/report/realtime_log_console.tpl', 154, false),array('block', 'setAboutPage', 'admin/report/realtime_log_console.tpl', 173, false),)), $this); ?>

<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_header.tpl", 'smarty_include_vars' => array('title' => 'Log Console','selected' => 'Log Console')));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?> 

<script type="text/javascript" src="/IBSng/js/libface.js"></script>
<script type="text/javascript" src="/IBSng/js/log_console.js"></script>

<table align=center border=0 style="display: none" id="error_table"> 
<tr> 
<td align=left>
    <img border="0" src="/IBSng/images/msg/before_error_message.gif">
</td>
    <td align=left class="error_messages">
	<span id="error_message">&nbsp;</span>
    </td>
</tr>
</table>


<?php $this->_tag_stack[] = array('viewTable', array('title' => 'Log Console')); $_block_repeat=true;smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	Refresh Every 
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'right')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<select name=refresh_interval id=refresh_interval onChange="window.reset_timer=true;">
	    <option>5</option>
	    <option selected>10</option>
	    <option>20</option>
	    <option>30</option>
	</select>

	Seconds <font size=1>
	(<a href="#" onClick="window.do_refresh=true" id="timer" class=link_in_body>_Loading_</a></span> 

	<a href="#" onClick="playPauseOnClick(this); return false;" style="text-decoration:none">
	    <img src="/IBSng/images/icon/pause.gif" border=0 id="refresh_play_pause" style="position: relative; top: 3">
	</a>

	seconds remaining)</font>
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'left')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	Rows Per Page
    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>
    <?php $this->_tag_stack[] = array('addEditTD', array('type' => 'right')); $_block_repeat=true;smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
	<select name=row_per_page id=row_per_page>
	    <option>50</option>
	    <option selected>100</option>
	    <option>200</option>
	</select>

    <?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addEditTD($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_viewTable($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


<br />

<span id="logs" name="logs"></span>
<script>

<?php echo '

window.logs=[];
window.last_log_time=0;
window.new_rows_count=0;
window.logs_table=new LogsTable();

requestLogs();

function doRequest()
{
    requestLogs();
}

function getLogsHandler(http_request)
{
    if (http_request.readyState == 4) 
    {    
	if (http_request.status == 200) 
	{
	    document.getElementById("request_time").innerHTML=(new Date().getTime() - window.request_send)/1000
	    
    	    clearError();
	    try
	    {
	        if(!http_request.responseXML.getElementsByTagName("result"))
		    showError("Invalid Response");		
	        else if(http_request.responseXML.getElementsByTagName("result")[0].childNodes[0].nodeValue!="SUCCESS")
		    showError(http_request.responseXML.getElementsByTagName("reason")[0].childNodes[0].nodeValue);
    	        else
		{
		    var parser_start=new Date().getTime();

		    var new_rows=http_request.responseXML.getElementsByTagName("REPORT");
		
	    	    appendToLogs(convertXMLToArrayOfDics(new_rows[0].childNodes));
		
		    document.getElementById("parser_time").innerHTML=(new Date().getTime() - parser_start)/1000
		
	    	    var render_start=new Date().getTime();
		
		    displayLogs();
		
	    	    document.getElementById("render_time").innerHTML=(new Date().getTime() - render_start)/1000
		}
	    }
	    catch(e)
	    {
		showError("Internal Error<br /> " + e.fileName + ":" + e.lineNumber +" Name: "+e.name + " Message:" + e.message);
	    }
	}
	else
	    showError("Internal Error");
	
	updateTimer();

    }

}


function requestLogs()
{
    var http_request;
    changeTimerState("_Loading_");
    
    if (window.XMLHttpRequest)
	http_request = new XMLHttpRequest();
    else if (window.ActiveXObject) 
	http_request = new ActiveXObject("Microsoft.XMLHTTP");

    if(http_request)
    {
	window.request_send=new Date().getTime();
	http_request.onreadystatechange = function() { getLogsHandler(http_request) };
	var url=\'/IBSng/admin/report/realtime_log_console.php?last_log_time=\'+window.last_log_time;
	http_request.open(\'GET\', url, true);
	http_request.send(null);	
    }
    else
	showError("Browser doesn\'t support xmlhttp");
}


</script>

'; ?>


<br />
<p align=right style="font-family: tahoma; font-size:6pt"> Request: <span id=request_time></span> Parser: <span id=parser_time></span> Render: <span id=render_time></span> Seconds</font>

<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/report/connections.php" class="RightSide_links">
	Connection Logs
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/report/online_users.php" class="RightSide_links">
	Online Users
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $this->_tag_stack[] = array('addRelatedLink', array()); $_block_repeat=true;smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start(); ?>
    <a href="/IBSng/admin/graph/onlines.php" class="RightSide_links">
	Onlines Graph
    </a>
<?php $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_addRelatedLink($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>


<?php $this->_tag_stack[] = array('setAboutPage', array('title' => 'RealTime Web Analyzer Logs')); $_block_repeat=true;smarty_block_setAboutPage($this->_tag_stack[count($this->_tag_stack)-1][1], null, $this, $_block_repeat);while ($_block_repeat) { ob_start();  $_block_content = ob_get_contents(); ob_end_clean(); $_block_repeat=false;echo smarty_block_setAboutPage($this->_tag_stack[count($this->_tag_stack)-1][1], $_block_content, $this, $_block_repeat); }  array_pop($this->_tag_stack); ?>

<?php $_smarty_tpl_vars = $this->_tpl_vars;
$this->_smarty_include(array('smarty_include_tpl_file' => "admin_footer.tpl", 'smarty_include_vars' => array()));
$this->_tpl_vars = $_smarty_tpl_vars;
unset($_smarty_tpl_vars);
 ?>