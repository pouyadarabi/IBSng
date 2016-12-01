{include file="admin_header.tpl" title="Graphs" selected="Onlines Graph"}

<table border=0 width="100%" height="100%" cellspacing=0 cellpadding=0>
    <tr>
	<td colspan=2 height=30>
	</td>
    </tr>	
    <tr>
	<td valign="center" align="center"> 
		{viewTable title="Graphs" table_width="200" nofoot="TRUE" color="brown" arrow_color="white"}
		    {menuTR}
			<a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php" class="page_menu">All Onlines RealTime Graph</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php?internet=1" class="page_menu">Internet Onlines RealTime Graph</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php?voip=1" class="page_menu">VoIP Onlines RealTime Graph</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/graph/realtime/realtime.php?img_url=bw.php" class="page_menu">Internet BW RealTime Graph</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/graph/onlines.php" class="page_menu">Onlines Graph</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/graph/analysis/connection_analysis.php" class="page_menu">Connections Analysis</a>
		    {/menuTR}

		    
		{/viewTable}

	</td>
    </tr>
</table>

{addRelatedLink}
    <a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php" class="RightSide_links">
	All RealTime Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php?internet=1" class="RightSide_links">
	Internet RealTime Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php?voip=1" class="RightSide_links">
	VoIP RealTime Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/realtime/realtime.php?img_url=bw.php" class="RightSide_links">
	BW RealTime Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/onlines.php" class="RightSide_links">
	Onlines Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/analysis/connection_analysis.php" class="RightSide_links">
	Connection Analysis
    </a>
{/addRelatedLink}


{setAboutPage title="Graph"}

{/setAboutPage}

{include file="admin_footer.tpl"}

