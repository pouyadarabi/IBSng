function displayLogs()
{
    updateReport();
}

//append new rows to logs that will be shown by displayLogs
function appendToLogs(new_rows)
{
    var row_per_page = getRowPerPage();

    window.logs = window.logs.concat(new_rows);

    if(window.logs.length > row_per_page)
	window.logs = window.logs.slice(Math.min(window.logs.length-row_per_page, window.logs.length-new_rows.length));

    if (new_rows.length)
	updateLastLogTime(new_rows[new_rows.length-1]["e"]); //epoch
    
    window.new_rows_count = new_rows.length;
}

//update last log id
function updateLastLogTime(last_log_time)
{
    window.last_log_time=last_log_time;
}

function getRowPerPage()
{
    var select_obj = document.getElementById("row_per_page");
    return parseInt(select_obj.options[select_obj.selectedIndex].text);
}

function LogsTable() 
{
    this.list_table=new ListTable();
}

LogsTable.prototype.createHeader=function() 
{
    var tds="";
    tds += this.list_table.createTD("Date");
    tds += this.list_table.createTD("Username");    
    tds += this.list_table.createTD("Action");
    tds += this.list_table.createTD("Message");
    return this.list_table.createHeaderTR(tds);
}


LogsTable.prototype.createBody=function()
{
    var trs="";
    for(var i=window.logs.length-1;i>=0;i--)
    {
	var row = window.logs[i];
	var tds = "";
	
	if(window.new_rows_count && i == window.logs.length - window.new_rows_count - 1)
	    trs += "<tr height=1><td colspan=20><hr></td></tr>";
	
	tds += this.list_table.createTD(row["df"]); //date formatted
	tds += this.list_table.createTD(row["u"]); //username
	tds += this.list_table.createTD(row["a"]); //action
	tds += this.list_table.createTD(this.createMessage(row["avpairs"]),"align='left'"); //message
	trs += this.list_table.createBodyTR(tds);
    }
    
    return trs;
}

LogsTable.prototype.createMessage=function(avpairs)
{
    var message=new Array();
    for(i in avpairs)
    {
	name = avpairs[i]["n"];
	value = avpairs[i]["v"];
	
	if ( name == "Status" )
	    value = "<font color=#990000>" + value + "</font>";
	
	message.push("<b>" + name + "</b>:" + value);
    }
    return message.join(", ");
}

LogsTable.prototype.createTable=function()
{
    html=this.createHeader();
    html+=this.createBody();
    return this.list_table.createTable("Log Console",4,html);    
}

function updateReport()
{
    document.getElementById("logs").innerHTML=window.logs_table.createTable();
}
