    {addEditTD type="left"}
	Refresh Every 
    {/addEditTD}
    {addEditTD type="right"}
	<select name=refresh_interval id=refresh_interval onChange="window.reset_timer=true;">
	    <option>5</option>
	    <option>10</option>
	    <option selected>20</option>
	    <option>30</option>
	    <option>60</option>
	</select>

	Seconds <font size=1>
	(<a href="#" onClick="window.do_refresh=true" id="timer" class=link_in_body title="Refresh">_Loading_</a></span> 

	<a href="#" onClick="playPauseOnClick(this); return false;" style="text-decoration:none">
	    <img src="/IBSng/images/icon/pause.gif" border=0 id="refresh_play_pause" style="position: relative; top: 3">
	</a>

	seconds remaining)</font>
    {/addEditTD}

    {addEditTD type="left"}
	Separate By
    {/addEditTD}
    {addEditTD type="right"}
	<input type=radio name=separate_by value=type checked onClick='separateByChanged(false)'> Service
	<input type=radio name=separate_by value=ras onClick='separateByChanged(true)'> Ras
    {/addEditTD}

    {addEditTD type="left"}
	Show
    {/addEditTD}
    {addEditTD type="right"}
	<input type=checkbox name=internet checked onClick='toggleDisplay(document.getElementById("all_internet"))'> Internet
	<input type=checkbox name=voip checked onClick='toggleDisplay(document.getElementById("all_voip"))'> VoIP
    {/addEditTD}

