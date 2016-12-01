<?php
$GLOBALS["IBSngMenu"]=Array(
                "user"=>array("User Information"=>"/IBSng/admin/user/user_info.php",
                              "Search User"=>"/IBSng/admin/user/search_user.php",
                              "Add New User"=>"/IBSng/admin/user/add_new_users.php",
                              "Add User Saves"=>"/IBSng/admin/user/search_add_user_saves.php"),
                              
                "group"=>array("Group List"=>"/IBSng/admin/group/group_list.php",
                               "Add New Group"=>"/IBSng/admin/group/add_new_group.php"),
                               
                "report"=>array("Online Users"=>"/IBSng/admin/report/online_users.php",
                                "Connection Logs"=>"/IBSng/admin/report/connections.php",
                                "Connection Usages"=>"/IBSng/admin/report/connection_usages.php",
                                "Credit Changes"=>"/IBSng/admin/report/credit_changes.php",
                                "Deposit Changes"=>"/IBSng/admin/report/admin_deposit_change_logs/admin_deposit_change_logs.php",
                                "User Audit Logs"=>"/IBSng/admin/report/user_audit_logs.php",
                                "Log Console"=>"/IBSng/admin/report/realtime_log_console.php",
                                "Web Analyzer Logs"=>"/IBSng/admin/report/web_analyzer_logs.php",
                                "Top Visited URLs"=>"/IBSng/admin/report/top_visited.php",
                                "RealTime Web Analyzer"=>"/IBSng/admin/report/realtime_web_analyzer.php"),

                "graph"=>array("Real Time Graphs"=>"/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php",
                                "Internet BW RealTime Graph"=>"/IBSng/admin/graph/realtime/realtime.php?img_url=bw.php",
                                "Onlines Graph"=>"/IBSng/admin/graph/onlines.php",
                                "Connections Analysis"=>"/IBSng/admin/graph/analysis/connection_analysis.php"),

                "admin"=>array("Admin List"=>"/IBSng/admin/admins/admin_list.php",
                               "Add Admin"=>"/IBSng/admin/admins/add_new_admin.php",
                               "Admin Messages"=>"/IBSng/admin/message/view_messages.php"),
                               
                "setting"=>array("Charge"=>"/IBSng/admin/charge/charge_list.php",
                                "RAS"=>"/IBSng/admin/ras/ras_list.php",
                                "IPPool"=>"/IBSng/admin/ippool/ippool_list.php",
                                "Bandwidth"=>"/IBSng/admin/bw/interface_list.php",
                                "VoIP Tariff"=>"/IBSng/admin/charge/voip_tariff/tariff_list.php",
                                "Clean Reports"=>"/IBSng/admin/report/clean_reports.php",
                                "Core Statistics"=>"/IBSng/admin/misc/core_statistics.php",
                                "Advanced Configuration"=>"/IBSng/admin/misc/show_ibs_defs.php"
                                ),
                                
                "home"=>array(""=>"/IBSng/admin/admin_index.php"),                     
                );

$GLOBALS["IBSngMenuLinks"]=Array("user"=>"/IBSng/admin/user/user_info.php",
                      "group"=>"/IBSng/admin/group/group_list.php",
                      "report"=>"/IBSng/admin/report",
                      "graph"=>"/IBSng/admin/graph",
                      "admin"=>"/IBSng/admin/admins/admin_list.php",
                      "setting"=>"/IBSng/admin/setting",
                      "home"=>"/IBSng/admin/admin_index.php"
                      );


function get1stLvlLink($menu_name)
{/*
    return link of 1st level menu icon for "menu_name";
*/
    global $IBSngMenuLinks;
    return $IBSngMenuLinks[$menu_name];
}

function get1stLvlSelected($second_lvl_selected)
{/*     return 1st level selected tag based on second level selected
*/
    global $menu_selected;
    if(!isset($menu_selected))
        $menu_selected=find1stLvlSelected($second_lvl_selected);
    return $menu_selected;
}

function find1stLvlSelected($second_lvl_selected)
{/*     finds 1st level selected tag based on second level selected
*/
    global $IBSngMenu;
    foreach($IBSngMenu as $first_lvl_name=>$second_lvl_arr)
        foreach($second_lvl_arr as $second_lvl_name=>$link)
            if ($second_lvl_name == $second_lvl_selected)
                return $first_lvl_name;
}

function get2ndLvlMenu($first_lvl_name)
{/* return second level menu array from first level selected */
    global $IBSngMenu;
    return $IBSngMenu[$first_lvl_name];
}

?>