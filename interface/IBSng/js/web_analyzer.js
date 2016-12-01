function displayLogs(totals)
{
    updateTotals(totals);
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
	updateLastLogID(new_rows[new_rows.length-1]["log_id"]);

    window.new_rows_count = new_rows.length;
}

//update last log id
function updateLastLogID(last_log_id)
{
    window.last_log_id=last_log_id;
}

function getRowPerPage()
{
    var select_obj = document.getElementById("row_per_page");
    return parseInt(select_obj.options[select_obj.selectedIndex].text);
}

//return query that will be appeneded to url when requesting logs
function generateURLQuery()
{
    var url=window.default_query + "&xml=1&order_by=log_id";
    if (window.last_log_id != -1)
	url += "&log_id_op=>&log_id="+window.last_log_id;
    else
	url += "&date_from="+window.start_date+"&date_from_unit=gregorian";

    if(window.user_id)
	url += "&user_id="+window.user_id;

    return url;
}

// add new fetched totals to page totals
function updateTotals(totals)
{
    for(total_name in totals)
    {
	if(total_name != "total_rows")
	{
	    var new_total_val=parseInt(totals[total_name]);
	    window.totals[total_name] += new_total_val;

	    var total_face = "";
	    switch(total_name)
	    {
		case "total_bytes":
		    total_face=formatByte(window.totals["total_bytes"]);
		    break;
		case "total_elapsed":
		    total_face=formatDuration(window.totals["total_elapsed"]);
		    break;
		default:
		    total_face=formatPrice(window.totals[total_name]);
	    }
	    document.getElementById(total_name).innerHTML = total_face;
	}
    }
}

function LogsTable() 
{
    this.list_table=new ListTable();
}

LogsTable.prototype.createHeader=function() 
{
    var tds="";
    tds += this.list_table.createTD("UserID");    
    tds += this.list_table.createTD("Date");
    tds += this.list_table.createTD("Username");    
    tds += this.list_table.createTD("Target URL");
    tds += this.list_table.createTD("Bytes");
    tds += this.list_table.createTD("Miss/Hit");
    tds += this.list_table.createTD("Success/Fail");
    tds += this.list_table.createTD("Elapsed");
    return this.list_table.createHeaderTR(tds);
}


LogsTable.prototype.createBody=function()
{
    var trs="";
    for(var i=window.logs.length-1;i>=0;i--)
    {
	var row=window.logs[i];
	var tds="";

	if(window.new_rows_count && i == window.logs.length - window.new_rows_count - 1)
	    trs += "<tr height=1><td colspan=20><hr></td></tr>";
	
	tds += this.list_table.createTD('<a class="link_in_body" href="/IBSng/admin/user/user_info.php?user_id='+row["user_id"]+'">'+row["user_id"]+'</a>');
	tds += this.list_table.createTD(row["date_formatted"]);
	tds += this.list_table.createTD(row["username"]);
	tds += this.list_table.createTD(breakString(row["url"], 60, "<br />"));
	tds += this.list_table.createTD(formatByte(row["bytes"]));
	tds += this.list_table.createTD(row["miss"]+"/"+row["hit"]);
	tds += this.list_table.createTD(row["successful"]+"/"+row["failure"]);
	tds += this.list_table.createTD(formatDuration(row["elapsed"]));
	
	trs += this.list_table.createBodyTR(tds);
    }
    
    return trs;
}

LogsTable.prototype.createTable=function()
{
    html=this.createHeader();
    html+=this.createBody();
    return this.list_table.createTable("Web Analyzer Logs",9,html);    
}

function updateReport()
{
    document.getElementById("logs").innerHTML=window.logs_table.createTable();
}
