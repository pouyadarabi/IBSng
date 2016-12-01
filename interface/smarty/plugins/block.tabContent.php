<?php

function smarty_block_tabContent($params,$content,&$smarty,&$repeat)
{
    require_once(IBSINC."tab.php");
/*
    create content of tabs
    parameter tab_name(string,required): name of tab title, that when it's selected, this content would be shown
    parameter add_table_tag(boolean,optional): optionally surrond content with a table tag
    parameter add_table_id(string,optional): optionally set id if add_table_tag is true

*/
    if(!is_null($content))
    {
        $table_id=getTabTableID(FALSE);
        $tab_id=tabName2TabID($params["tab_name"]);

        if(isset($params["add_table_tag"]) and $params["add_table_tag"]=="TRUE")
        {
            $add_table_id=isset($params["add_table_id"])?"id=".$params["add_table_id"]:"";
            $content=<<<END
                <table border="0" cellspacing="0" cellpadding="0" width="100%" {$add_table_id}>
                {$content}
                </table>
END;
        }
        
        
        return <<<END
        <div id="{$table_id}_{$tab_id}_content" align=center>
            {$content}
        </div>
        <script>
                {$table_id}.initContent("{$table_id}_{$tab_id}");
        </script>
END;
    }
        
}


?>