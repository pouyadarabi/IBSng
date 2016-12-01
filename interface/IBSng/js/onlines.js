//given all rows of onlines, convert them to an array of dictionaries
function convertOnlinesToArray(rows)
{
    return convertXMLToArrayOfDics(rows);
}

//////////////////////////////////////////// Check Box Handlings
function resetCheckBoxes()
{
    window.check_box_containers=[];
    window.check_boxes=[];
    window.last_check_box_id=0;
}

function createCheckBoxContainers()
{
    for(var i=0;i<window.check_boxes.length;i++)
    {
	var table_info=window.check_boxes[i];
	var form_name=table_info[0]+"_onlines";
		
	container=new CheckBoxContainer(i);
	container.setCheckAll(form_name,table_info[1]);
	for(var j=0;j<table_info[2].length;j++)
	    container.addByName(form_name,table_info[2][j]);
	window.check_box_containers.push(container);
    }
}

//////////////////////////////////////////// Display Onlines
function displayOnlines()
{
    initVars();
    if(window.separate_by_ras)
	displayOnlinesByRas();
    else
	displayOnlinesByType();
    finalizeVars();
}

function initVars()
{
    resetCheckBoxes();
    document.getElementById("msg").src="/IBSng/util/empty.php";
    window.online_tables=[];
}

function finalizeVars()
{
    createCheckBoxContainers();
}


function displayOnlinesByType()
{
    var internet=new OnlinesTable("Internet Onlines",getChildCheckBoxItems("internet_select",true),window.internet_onlines,"internet");
    document.getElementById("internet_onlines").innerHTML=internet.createTable();

    var voip=new OnlinesTable("VoIP Onlines",getChildCheckBoxItems("voip_select",true),window.voip_onlines,"voip");
    document.getElementById("voip_onlines").innerHTML=voip.createTable();
}

function displayOnlinesByRas()
{
    var internet_table=createByRasTables("Internet Onlines",
					     getChildCheckBoxItems("internet_select",true),
					     window.internet_onlines,
					     "internet");
    document.getElementById("internet_onlines").innerHTML=internet_table;

    var voip_table=createByRasTables("VoIP Onlines",
					 getChildCheckBoxItems("voip_select",true),
					 window.voip_onlines,
					 "voip");
    document.getElementById("voip_onlines").innerHTML=voip_table;
}

function createByRasTables(title, selected_attrs, onlines, type)
{//create table for each ras
    var tables="";	
    var ras_onlines=getOnlinesByRas(onlines);
    for(var ras_desc in ras_onlines)
    {
	var online_table=new OnlinesTable(ras_desc + " " + title,
					  selected_attrs,
					  ras_onlines[ras_desc],	
					  type);
	tables+=online_table.createTable() + "<br />";
    }
    return tables;
}

function getOnlinesByRas(onlines)
{//seperate onlines by ras and return a dic in format {ras_description:onlines_list,...}
    var ras_onlines={};
    for (var i in onlines)
    {
	var ras_desc=onlines[i]["ras_description"];
	if(ras_onlines[ras_desc]==undefined)
	    ras_onlines[ras_desc]=[];

	ras_onlines[ras_desc].push(onlines[i]);
    }
    return ras_onlines;
}


///////////////////////////////////////////

//return an array of selected check boxes in child node of id
function getChildCheckBoxItems(id,only_checked)
{
    var selected=new Array();
    var stack=new Array();
    var obj=document.getElementById(id);
    stack.push(obj);

    while(stack.length)
    {
	obj=stack.pop();
	if(obj.tagName=="INPUT" && (!only_checked || obj.checked))
	    selected.push(obj); // return format is [obj,obj,...]
	else
	    for(var i in obj.childNodes)
		stack.unshift(obj.childNodes[i]);
    }
    return selected;    
}

function setCheckBoxesOnclick(id, method)
{
    var objs=getChildCheckBoxItems(id);
    for(var i in objs)
	objs[i].onclick=method;
}

////////////////////////////////////////////////////////// Attr Conversions

window.attr_conversion={"duration_secs":formatDuration,
			"current_credit":formatPrice,
			"in_bytes":formatByte,
			"out_bytes":formatByte,
			"in_rate":formatByte,
			"out_rate":formatByte,
			"normal_username":linkNormalUsername,
			"voip_username":linkVoIPUsername}

function linkNormalUsername(normal_username)
{
    return '<a href="/IBSng/admin/user/user_info.php?normal_username='+normal_username+'" class="link_in_body" target="_blank">'+normal_username+'</a>';
}

function linkVoIPUsername(voip_username)
{
    return '<a href="/IBSng/admin/user/user_info.php?voip_username='+voip_username+'" class="link_in_body" target="_blank">'+voip_username+'</a>';
}

//////////////////////////////////////////////////////////
//Onlines Table

function OnlinesTable(title,selected_attrs,onlines,type)
{
    this.title=title;
    this.selected_attrs=selected_attrs;
    this.list_table=new ListTable();
    this.onlines=onlines;
    this.type=type
    this.online_table_id=window.online_tables.length;
    window.online_tables.push(this);
}

OnlinesTable.prototype.createHeader=function()
{
    var tds = this.createCheckAllCheckBox() + this.list_table.createTD("row");
    var cur_sort = getCurSort(this.type);
    var cur_desc = getCurDesc(this.type);

    for(var i in this.selected_attrs)
    {
	var obj = this.selected_attrs[i];
	var content;
	if(cur_sort == obj.name)
	{
	    var img;
	    if(cur_desc)
		img="up";
	    else
		img="down";
	    
	    content='<img src="/IBSng/images/arrow/sort_'+img+'.gif" border=0>' + obj.value;
	}
	else
	    content=obj.value;
	
	tds += this.list_table.createTD('<a href="#" id="'+obj.name+'" onClick="headerClicked(event,\''+this.type+'\')" class="Header_Top_links">'+content+'</a>');
    }
    return this.createHeaderIcons() + this.list_table.createHeaderTR(tds);
}

OnlinesTable.prototype.createHeaderIcons=function()
{
    ret="";
    ret+=this.list_table.createHeaderIcon("details");
    if(this.type=="internet")
    {
	ret+=this.list_table.createHeaderIcon("graph");
	ret+=this.list_table.createHeaderIcon("history");
    }
    return ret;
}

OnlinesTable.prototype.createBodyIcons=function(row_id, row)
{
    var ret="";

    var detail_layer_name=row["ras_ip"]+'_'+row["unique_id_val"];
    var details='<a onClick="return createReportLayer(\''+detail_layer_name+'\', this, '+this.online_table_id+','+row_id+'); " href="#">';
    details+=this.list_table.createBodyIcon("details", true);
    details+='</a> <div id="'+detail_layer_name+'" style="position:absolute;display:none"></div>';
    
    ret+=this.list_table.createBodyIconTD(details);
    
    if(this.type=="internet")
    {
	var graph_layer_name=detail_layer_name+'_graph';
	var graph='<a onClick="return createGraphLayer(\''+graph_layer_name+'\', this, \''+row['normal_username']+'\','+row['user_id']+',\''+row['ras_ip']+'\',\''+row['unique_id_val']+'\'); " href="#">';
//	var graph='<a style="text-decoration:none" target="_blank" href="/IBSng/admin/graph/realtime/realtime.php?img_url=bw.php?username='+row["normal_username"]+'%26user_id='+row["user_id"]+'%26ras_ip='+row["ras_ip"]+'%26unique_id_val='+row["unique_id_val"]+'">';
	graph+=this.list_table.createBodyIcon("graph");
	graph+='</a> <div id="'+graph_layer_name+'" style="position:absolute;display:none"></div>';

	ret+=this.list_table.createBodyIconTD(graph);
	
	var web_analyzer="<a target='_blank' href='/IBSng/admin/report/realtime_web_analyzer.php?user_id="+row["user_id"]+"&username="+row["normal_username"]+"'>";
	web_analyzer += this.list_table.createBodyIcon("history")+"</a>";

	ret+=this.list_table.createBodyIconTD(web_analyzer);

    }
    return ret;
}


OnlinesTable.prototype.createBody=function()
{
    var row_no=1;
    var trs = "";
    for(var i=0;i<this.onlines.length;i++)
    {
	var tds = this.createBodyCheckBox(this.onlines[i]) + this.list_table.createTD(row_no++);
	for(var j in this.selected_attrs)
	{
	    var obj = this.selected_attrs[j];
	    var value = this.prepareValue(this.onlines[i], obj.name);
	    tds += this.list_table.createTD(value);
	}
	tds += this.createBodyIcons(i,this.onlines[i]);
	trs += this.list_table.createBodyTR(tds);
	
    }
    return trs;
}

OnlinesTable.prototype.prepareValue=function(row,key)
{
    if (key.substr(0,6) == "attrs_")
    {
	key=key.substr(6);
	value=row["attrs"][key]?row["attrs"][key]:"N/A";
    }
    else
    	value=row[key];

    if (window.attr_conversion[key])
	return eval('window.attr_conversion[key]("'+value+'")');
    else
	return value;
}

OnlinesTable.prototype.createTable=function()
{
    html=this.createHeader();
    html+=this.createBody();
    return this.list_table.createTable(this.title,this.selected_attrs.length+2,html);    
}


OnlinesTable.prototype.createCheckAllCheckBox=function()
{
    this.check_box_id=window.check_boxes.length;
    this.minor_check_box_id=0;

    window.check_boxes.push([this.type,"check_all"+this.check_box_id,[]]);

    content="<input type=checkbox name=check_all"+this.check_box_id+">";
    return this.list_table.createTD(content);
}

OnlinesTable.prototype.createBodyCheckBox=function(row_arr)
{
    if(this.type=="internet")
	username=row_arr["normal_username"];
    else
	username=row_arr["voip_username"];
    
    check_box_value=row_arr["user_id"]+"__"+username+"__"+row_arr["ras_ip"]+"__"+row_arr["unique_id_val"];
    check_box_name="check_box"+this.check_box_id+"_"+this.minor_check_box_id++;
    
    window.check_boxes[this.check_box_id][2].push(check_box_name);
    content="<input type=checkbox name='"+check_box_name+"' value='"+check_box_value+"'>";
    return this.list_table.createTD(content);
}

////////////////////////////////////////////////// header sorting functions
/////////////
function headerClicked(evt, type)
{
    var id;
    if (evt && evt.target)
	id=evt.target.id;
    else if (window.event && window.event.srcElement)
	id=window.event.srcElement.id;

    sortBy(id, type);
}

//get current sort for "type" 
function getCurSort(type)
{
    var cur_sort=eval("window."+type+"_sort");
    if (!cur_sort)
	cur_sort="login_time";
    return cur_sort;    
}

function getCurDesc(type)
{
    var cur_desc=eval("window."+type+"_desc");
    if (cur_desc==undefined)
	cur_desc=false
    return cur_desc;    
}

function sortBy(id, type)
{
    var cur_sort=getCurSort(type)    
    if (cur_sort == id)
    {
	var desc=!getCurDesc(type);
	setDesc(id,type,desc);
    }
    else
    {
	setSort(id,type);
	setDesc(id,type,false);
    }
    window.do_refresh=true;
}

function setSort(id, type)
{
    eval('window.'+type+'_sort="'+id+'"');
}

function setDesc(id, type, desc)
{
    eval('window.'+type+'_desc='+(desc?'true':'false'));
}

/////////////////////////////////////// Separate By  functions
function separateByChanged(separate_by_ras)
{
    window.separate_by_ras=separate_by_ras;
    displayOnlines();
}
///////////////////////////////////// action icon functions
function actionIconClicked(action)
{
    if ((action == "kick" || action == "clear") && !confirm("Are you sure?"))
	return;

    var selected=getSelectedUsers();

    user_ids=selected[0].join(",");
    usernames=selected[1].join(",");
    ras_ips=selected[2].join(",");
    unique_ids=selected[3].join(",");
    
    if(action == "kick")
	killUser(user_ids,usernames,ras_ips,unique_ids,true);

    else if(action == "clear")
	killUser(user_ids,usernames,ras_ips,unique_ids,false);

    else if(action == "message")
	window.open("/IBSng/admin/message/post_message_to_user.php?user_id="+user_ids,null);
}

function getSelectedUsers()
{
    var user_ids=[],usernames=[],ras_ips=[],unique_ids=[];
    for(var i=0;i<window.check_box_containers.length;i++)
    {
	var container=window.check_box_containers[i];
	for(var j=0;j<container.check_box_objs.length;j++)
	    if(container.check_box_objs[j].checked)
	    {
	        var sp=container.check_box_objs[j].value.split("__");
		user_ids.push(sp[0]);
		usernames.push(sp[1]);
		ras_ips.push(sp[2]);
		unique_ids.push(sp[3]);
	    }
    }
    return [user_ids,usernames,ras_ips,unique_ids];
}


///////////////////////////////////////////// Detail Layer
function createReportLayer(detail_layer_name, link_obj, online_table_id, row_id)
{
    if(!document.getElementById(detail_layer_name).innerHTML)
    {
	var layer=new LayerTable();
	var online_table=window.online_tables[online_table_id];
        var username_key;
    
	if (online_table.type=="internet")
	    username_key="normal_username";
	else
	    username_key="voip_username";
    
	var username=online_table.onlines[row_id][username_key];	
    
	document.getElementById(detail_layer_name).innerHTML=layer.createDetailLayer(online_table.onlines[row_id], username + " Details");
    }
    showReportLayer(detail_layer_name, link_obj);
    return false;
}

function createGraphLayer(graph_layer_name, link_obj, username, user_id, ras_ip, unique_id_val)
{
    if(!document.getElementById(graph_layer_name).innerHTML)
    {
	var layer=new LayerTable();
    
	var content='<table><tr><td> \
		    <img width=400 border=0 src="/IBSng/admin/graph/realtime/bw.php?username='+username+'&user_id='+user_id+'&ras_ip='+ras_ip+'&unique_id_val='+unique_id_val+'" > \
		    </td></tr> <tr><td align=center>\
		    <a class="link_in_body" target="_blank"\
		    href="/IBSng/admin/graph/realtime/realtime.php?img_url=bw.php?username='+username+'%26user_id='+user_id+'%26ras_ip='+ras_ip+'%26unique_id_val='+unique_id_val+'"> \
		    Show Real Size</a> \
		    </td></tr></table>';
    
	document.getElementById(graph_layer_name).innerHTML=layer.createReportDetailLayer(graph_layer_name, username + 'BW Graph', content);
    }
    showReportLayer(graph_layer_name, link_obj);
    return false;

}


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
 

//************************* Filter Functions

function getFiltersURL()
{
    var url_params = new Array();

    var selected_filters = getChildCheckBoxItems("ras_filter_select", true);
    selected_filters = selected_filters.concat(getChildCheckBoxItems("username_filter_select", true));
    
    for(var i=0; i<selected_filters.length; i++)
    {
	obj = selected_filters[i];
	url_params.push(obj.name+"="+obj.value);

	if(obj.name.substr(0,"username".length) == "username")
	{
	    _char = obj.name.substr("username".length+1).toLowerCase();
	    url_params.push("username_"+_char+"="+_char);
	}
    }
    return url_params.join("&");
}
