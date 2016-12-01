//given an xml of rows, convert them to an array of dictionaries
function convertXMLToArrayOfDics(rows)
{
    var arr=[];
    for(var i=0;i<rows.length;i++)
    {
	var row=rows[i];
	arr.push(convertElementsToDic(row));
    }
    return arr;
}


//convert  All child elements to a dictionary
function convertElementsToDic(element)
{
    var dic={}
    for(var i=0;i<element.childNodes.length;i++)
    {
        var attr_obj=element.childNodes[i];
        var attr_name=attr_obj.tagName;
	var attr_value;

	if(!attr_obj.childNodes[0])
	    attr_value="";
	else if (attr_obj.childNodes.length>1 || !attr_obj.childNodes[0].nodeValue)
	    attr_value=convertElementsToDic(attr_obj);
	else
	    attr_value=attr_obj.childNodes[0].nodeValue;

	dic[attr_name]=attr_value;
    }
    return dic;

}


////////////////////////////////////////////// Error Handlings
// Display an error message on top of mesage
function showError(msg)
{
    document.getElementById("error_message").innerHTML = msg;
    document.getElementById("error_table").style.display='';
}

//clear error message
function clearError()
{
    document.getElementById("error_table").style.display = 'none';
}

////////////////////////////////////////////
function getTRColor(cycle_color, var_name)
{
    if(!var_name)
	var_name="tr_color";
    if(cycle_color || !window.tr_color)
    {
	if(eval("window."+var_name))
	    if(eval("window."+var_name)=="dark")
		eval("window."+var_name+"='light'");
	    else
		eval("window."+var_name+"='dark'");
	else
	    eval("window."+var_name+"='light'");
    }
    
    return eval("window."+var_name);
}

//////////////////////////////////////////////// Timer handlings
/////

//Change timer string to "state"
function changeTimerState(state)
{
    span_obj=document.getElementById("timer");
    span_obj.childNodes[0].nodeValue=String(state);
}

//this function calls in 1 seconds periods and update timer value
//if timer is expired it will call doRequest function
function updateTimer()
{
    var span_obj=document.getElementById("timer");
    var timer=span_obj.childNodes[0].nodeValue;

    if(timer == "_Loading_")
	timer=getRefreshInterval();
    else if (window.reset_timer)
    {
	timer=getRefreshInterval();
	window.reset_timer=false;
    }
    else if (window.refresh_timer_status && window.refresh_timer_status == "pause")
	timer=parseInt(timer);
    else
	timer=parseInt(timer)-1;

    if(timer==0 || window.do_refresh)
    {
	doRequest();
	window.do_refresh=false;
    }
    else
    {
	changeTimerState(timer);
        window.timer_timeout=setTimeout("updateTimer()",1000);
    }
}

//get currently selected refresh interval
function getRefreshInterval()
{
    select_obj=document.getElementById("refresh_interval");
    return parseInt(select_obj.options[select_obj.selectedIndex].text);
}



//////////////////////////////// Layer Table
function LayerTable()
{}

LayerTable.prototype.createDetailLayer=function(row, title)
{
    content="";
    for(attr_name in row["attrs"])
	content+=this.createLayerTR(this.createTD(attr_name)+this.createTD(row["attrs"][attr_name]), true);

    content=this.createLayerTable(content);
    

    return this.createReportDetailLayer(row["ras_ip"]+"_"+row["unique_id_val"], title, content);
}

LayerTable.prototype.createReportDetailLayer=function(name, title, content)
{
    layer='<table border="0" width=300 bgcolor="#757575" cellspacing="0" cellpadding="1"> \
	    <tr> \
		<td width="100%"> \
		     <table border="0" width="100%" bgcolor="#ff9c00" cellspacing="0" cellpadding="1"> \
    			 <tr> \
			 <td width="100%"> \
			     <table border="0" width="100%" bgcolor="#ff9c00" cellspacing="0" cellpadding="0" style="cursor:hand; cursor:pointer;"> \
				<tr><td width=265 onMouseDown="startMove(event,document.getElementById(\''+name+'\')); return false;" onMouseUp="stopMove(); return false;" > \
				     <font face="tahoma" color="#FFFFFF" style="font-size:8pt"><B>&nbsp;&nbsp;'+title+'</b></font> \
				    </td> \
			    <td width="35"> \
				<a href="#" onClick="document.getElementById(\''+name+'\').style.display=\'none\';return false"> \
				    <nobr><img src="/IBSng/images/icon/close.gif" border=0 width=32 height=16></a></td> \
		     </tr> \
		     </table> \
		     </td> \
		     </tr> \
		     <tr> \
			 <td width="100%" style="padding:2px"> \
			    <table border="0" width="100%" bgcolor="#FFFFFF" cellspacing="0" cellpadding="0"> \
			    <tr><td>		\
	    			'+content+' \
			    </td></tr> \
			    </table> \
			 </td> \
		     </tr> \
	    	    </table> \
		</td> \
	    </tr> \
	</table> ';
    return layer;
}

LayerTable.prototype.createLayerTable=function(content)
{
    return '<table width=100% border=0 cellspacing=0 cellpadding=0>' +
	    content +
	    '</table>';
}

LayerTable.prototype.createLayerTR=function(content, cycle_color)
{
    color=getTRColor(cycle_color,"layer");
    
    return '<tr class="Layer_Row_'+color+'Color">'+
		content+
	    '</tr>';
}

LayerTable.prototype.createTD=function(content,extra)
{
    if(!extra)
	extra="";
	
    return '<td class="list_col" valign="Middle" '+extra+'>'+content+'</td>';
}

////////////////////////////////////////////////////////// List Table
function ListTable()
{}

ListTable.prototype.createTable=function(title, cols_num,content)
{
    return '<table border="0"  class="List_Main" cellspacing="1" bordercolor="#FFFFFF" cellpadding="0"> \
	<tr> \
		<td colspan="'+cols_num+'" valign="bottom"> \
		<!-- List Title Table --> \
		<table border="0" cellspacing="0" cellpadding="0" class="List_Title"> \
			<tr> \
				<td class="List_Title_Begin" rowspan="2"><img border="0" src="/IBSng/images/form/begin_form_title_red.gif"></td> \
				<td class="List_Title" rowspan="2">'+title+'<img border="0" src="/IBSng/images/arrow/arrow_orange_on_red.gif" width="10" height="10"></td> \
				<td class="List_Title_End" rowspan="2"><img border="0" src="/IBSng/images/list/end_of_list_title_red.gif" width="5" height="20"></td> \
				<td class="List_Title_Top_Line">&nbsp;</td> \
			</tr> \
			<tr> \
				<td class="List_Title_End_Line"></td> \
			</tr> \
		</table> \
		<!-- End List Title Table --> \
		</td> \
    ' + content + '	<!-- List Foot --> \
	<tr class="List_Foot_Line_red"> \
		<td colspan=30></td> \
	</tr> \
	<!-- End List Foot--> \
	</table>';
}

ListTable.prototype.createHeaderTR=function(content)
{
    return '<tr class="List_Head">'+content+'</tr>';
}

ListTable.prototype.createHeaderIcon=function(action, close_tr)
{
    link="/IBSng/images/list/list_header_" + action + ".gif";

    ret='<td valign="bottom" Rowspan=2 class="List_Title_Icon"> \
         <img border="0" src="'+link+'" title="'+ action +'"></td>';
    
    if (close_tr)
	ret += "</tr>";
    
    return ret;
}

ListTable.prototype.createBodyTR=function(content,hover_location,hover_color)
{
    hover="";
    if(hover_location && hover_color)
    {
	hover='onMouseover="changeTRColor(this,\''+hover_color+'\');" \
	       onMouseout="changeTRColor(this,null);" \
	       style="cursor: pointer;" \
	       onClick="window.location=\''+hover_location+'\'';

    }
    tr_color=getTRColor();
    return '<tr class="List_Row_'+tr_color+'Color" '+hover+'>'+content+'</tr>';
}

ListTable.prototype.createTD=function(content,extra)
{
    if(!extra)
	extra="";
	
    return '<td class="list_col" valign="Middle" '+extra+'>'+content+'</td>';
}

ListTable.prototype.createBodyIconTD=function(content)
{
    return '<td class="List_col_Body_Icon" valign="Top">'+content+'</td>';
}

ListTable.prototype.createBodyIcon=function(action, cycle_color)
{
    color=getTRColor(cycle_color);
    link="/IBSng/images/list/list_body_"+action+"_"+color+".gif";
    
    return '<img border="0" src="'+link+'" width="25" height="20" title="'+action+'"';
}
