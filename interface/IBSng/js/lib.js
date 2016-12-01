function getSelectedOption(form_name,select_name)
{
    select_obj=eval("document."+form_name+"."+select_name);
    if (select_obj.selectedIndex<0) //select is empty
	return "";
    return select_obj.options[select_obj.selectedIndex].text;
}

function showHelp(subject,category)
{
    subject=escape(subject);
    category=escape(category);
    open("/IBSng/help/show_help.php?subject="+subject+"&category="+category,"","width=500,height=300,scrollbars=yes,alwaysRaised=yes,dependent=yes,resizable=yes");
}

function showMultiStr(form_name,input_name,left_pad)
{
    input_obj=eval("document."+form_name+"."+input_name);
    open("/IBSng/util/show_multistr.php?str="+input_obj.value+"&left_pad="+left_pad,"","width=500,height=300,scrollbars=yes,alwaysRaised=yes,dependent=yes,resizable=yes");
}

function updateUserAddCheckImage(user_type,current_username,update_timer)
{//user_type can be 'normal' or 'voip' used to select image and pass to user_exists.php
 //update_timer: tell the timer to update the image in seconds. if set to zero, update immediately
//    alert(window.user_add_check_timer);
//    alert(update_timer);
    if(update_timer>=0)
    {
	if ((window.user_add_check_timer && window.user_add_check_timer<=0) || !window.user_add_check_timer)
	    setTimeout("updateUserAddCheckImage('"+user_type+"','"+current_username+"',-1)",500);
	window.user_add_check_timer=update_timer*1000+500;

    }
    else if (update_timer<0)
    {
	if (window.user_add_check_timer==0)
	{
	    img_obj=eval("document."+user_type+"_user_exists");
	    username=eval("document.user_edit."+user_type+"_username");
	    img_obj.src="/IBSng/admin/user/check_user_for_add.php?image=t&username="+username.value+"&type="+user_type+"&current_username="+current_username;
	}
	else
	{
	    window.user_add_check_timer-=500;
	    setTimeout("updateUserAddCheckImage('"+user_type+"','"+current_username+"',-1)",500);
	}
    }
}

function showUserAddCheckWindow(user_type,current_username)
{
    username=eval("document.user_edit."+user_type+"_username");
    open("/IBSng/admin/user/check_user_for_add.php?image=f&username="+username.value+"&type="+user_type+"&current_username="+current_username,"user_check","width=500,height=300,scrollbars=yes,alwaysRaised=yes,dependent=yes");
}

function changeTRColor(obj,color)
{
    if(color==null)
    {
    	if(obj.original_color)
    	    obj.style.backgroundColor=obj.original_color;
    }
    else
    {
	obj.original_color=getObjCurrentStyle(obj).backgroundColor;
    	obj.style.backgroundColor=color;
    }
}

function getObjCurrentStyle(obj)
{
    if(window.getComputedStyle)
	return window.getComputedStyle(obj,null);
    else if (obj.currentStyle)
	return obj.currentStyle;
}

function showReportLayer(layer_id,show_obj,hpos)
{
    layer_obj=document.getElementById(layer_id)
    layer_obj.style.left=0;
    toggleDisplay(layer_obj);
    obj_top=findPosY(show_obj) + show_obj.offsetTop;
//    if(show_obj.firstChild.height) //ie
//	obj_top+=show_obj.firstChild.height;
    layer_obj.style.top=obj_top;
    
    obj_left=findPosX(show_obj);
    if(!hpos || hpos=="left")
	obj_left -= layer_obj.offsetWidth;
    else if(hpos=="right") 
	obj_left += show_obj.offsetWidth;
    
    layer_obj.style.left=obj_left;
}
/////////////////////////// layer move
function moveLayer(evt,layer_obj)
{
    if(!window.start_move)
	return;
	
    if (window.event)
	evt=window.event;
	
    layer_obj.style.left=window.now_x+evt.clientX-window.offset_x;
    layer_obj.style.top=window.now_y+evt.clientY-window.offset_y;
    return false;
}

function startMove(evt, layer_obj)
{
    if (window.event)
	evt=window.event;

    window.start_move=true;
    window.offset_x=evt.clientX;
    window.offset_y=evt.clientY;
    window.now_x=parseInt(layer_obj.style.left);
    window.now_y=parseInt(layer_obj.style.top);
    document.onmousemove=function(evt) { moveLayer(evt, layer_obj); }
}

function stopMove(evt)
{
    window.start_move=false;
    document.onmousemove=null;
}
/////////////////////////// Session Date Type handlings
function sessionDateTypeChanged(http_request)
{// if request was successfull, hide the date_type select layer and change current date type
    if (http_request.readyState == 4 && http_request.status == 200) 
    {
	document.getElementById('session_date_select').style.display='none';
	document.getElementById('current_session_date_type').innerHTML=http_request.responseText;
    }    
}

function changeSessionDateType(date_type)
{// change session date_type to "date_type"
    var http_request;
    
    if (window.XMLHttpRequest)
	http_request = new XMLHttpRequest();
    else if (window.ActiveXObject) 
	http_request = new ActiveXObject("Microsoft.XMLHTTP");

    if(http_request)
    {
	window.request_send=new Date().getTime();
	http_request.onreadystatechange = function() { sessionDateTypeChanged(http_request) };
	var url='/IBSng/util/session_date_type.php?date_type='+date_type;
	http_request.open('GET', url, true);
	http_request.send(null);	
    }
    else
	alert("Browser doesn't support xmlhttp");
}


//////////////////////////
function toggleDisplay(obj)
{
    if(obj.style.display=='none')
	obj.style.display='';
    else
	obj.style.display='none';
}

function toggleShowHide(show_hide_id, target_id)
{
    show_hide_obj=document.getElementById(show_hide_id);
    target=document.getElementById(target_id);
    if(target.style.display=='none')
    {
	target.style.display='';
	show_hide_obj.innerHTML="Hide";
    }
    else
    {
	target.style.display='none';
	show_hide_obj.innerHTML="Show";
    }
    
}

function toggleVisibility(obj)
{
    if(obj.style.visibility=='hidden')
	obj.style.visibility='visible';
    else
	obj.style.visibility='hidden';
}

/*function absDateSelectChanged(select_obj,calendar_id)
{
    calendar_obj=document.getElementById(calendar_id);
    if(select_obj.value=="gregorian")
    {
	calendar_obj.date_type="G";
	calendar_obj.disabled=false;
    }
    else if (select_obj.value=="jalali")
    {
	calendar_obj.date_type="J";
	calendar_obj.disabled=false;
    }
    else
	calendar_obj.disabled=true;
}*/

function ibs_setup_calendar(input_id, trigger_id, select_id)
{
    select_obj=document.getElementById(select_id);
    if(select_obj.value=="gregorian")
	setup_calendar(input_id,trigger_id, "G");
    else if (select_obj.value=="jalali")
	setup_calendar(input_id,trigger_id, "J");
    else
    {
	if (window.DATE_TYPE == "jalali")
	    select_obj.value="jalali";
	else
	    select_obj.value="gregorian";
	
	ibs_setup_calendar(input_id, trigger_id, select_id);    
    }
}

function findPosX(obj)
{
	var curleft = 0;
	if (obj.offsetParent)
	{
		while (obj.offsetParent)
		{
			curleft += obj.offsetLeft
			obj = obj.offsetParent;
		}
	}
	else if (obj.x)
		curleft += obj.x;
	return curleft;
}

function findPosY(obj)
{
	var curtop = 0;
	if (obj.offsetParent)
	{
		while (obj.offsetParent)
		{
			curtop += obj.offsetTop
			obj = obj.offsetParent;
		}
	}
	else if (obj.y)
		curtop += obj.y;
	return curtop;
}

var window_onloads = [];

function windowOnload()
{
    for(idx in window_onloads)
    {
	window_onloads[idx]();
    }
}	

function addToWindowOnloads(method)
{ // add method to run on window onload. this overrides previous onload, 
  // all methods should use this function to be loaded on startup
    window_onloads.push(method);
    window.onload = windowOnload;
}

//Display message in message box
function showMessage(message_id)
{
    toggleDisplay(document.getElementById("message_text_truncated_"+message_id));
    toggleDisplay(document.getElementById("message_text_"+message_id));
    return false;
}

function isArray(check)
{
    if(typeof check == "object")
       return(check.constructor.toString().match(/array/i) != null);
    return false;
}



function formatPrice(price)
{//put comma between each 3 digits of price and return formatted string
    precision=2;
    var price=parseFloat(price);
    var sign=price<0?-1:1;
    price*=sign;
    if(precision)
    {
        var int_price=Math.floor(price);
	var float_part=Math.round((price-int_price)*Math.pow(10,precision));
    }
    else
    {
        var int_price=Math.round(price);
	var float_part=0;
    }
	
    int_part=String(int_price);
    var str="";
    while(int_part.length>3)
    {
        var part=int_part.substr(int_part.length-3,3);
	int_part=int_part.substr(0,int_part.length-3);
	str="," + part + str;
    }

    str=int_part+str;
    if(float_part>0)
        str+="."+float_part;
    if(sign==-1)
        str="-"+str;
    return str;
}

function formatDuration(seconds)
{ //return seconds in format HH:MM:SS
    var hours=parseInt(seconds/3600);
    if(hours<10)
	hours="0"+hours;
    var rest=seconds%3600;
    var mins=parseInt(rest/60);
    if(mins<10)
	mins="0"+mins;
    var secs=parseInt(rest%60);
    if(secs<10)
	secs="0"+secs;

    return hours+":"+mins+":"+secs;
}

function formatByte(bytes)
{
    var units=["B","K","M","G"];
    for(var i in units)
    {
	if(bytes<1024)
	{
	    return String(Math.round(bytes))+units[i];
	}
	bytes/=1024;
    }
    return String(Math.round(bytes))+units[i];
}


//break string into multiple lines with length not more than length
function breakString(str, length, glue)
{
    var broken_str = "";
    while(str.length > length)
    {
	broken_str += str.substr(0, length) + glue;
	str = str.substr(length);
    }
    return broken_str + str;
}

/*
    handle onclick of play/pause button on refresh headers
    the play_pause image should have id "refresh_play_pause"
    
    window.refresh_timer_status is used for current state
*/
function playPauseOnClick()
{

    img_obj = document.getElementById("refresh_play_pause");
	
    switch(window.refresh_timer_status)
    {
	case "play":
	case undefined:
	    window.refresh_timer_status = "pause";
	    img_obj.src = "/IBSng/images/icon/play.gif";
	    break;
	
	case "pause":
	    window.refresh_timer_status = "play";
	    img_obj.src = "/IBSng/images/icon/pause.gif"
	    break;
//		if(window.refresh==0) //window.location stopped by user click
//		    window.location = window.location;

    }
}