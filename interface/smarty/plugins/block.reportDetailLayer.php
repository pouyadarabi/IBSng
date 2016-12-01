<?php

function smarty_block_reportDetailLayer($params,$content,&$smarty)
{
/*      create a layer window, that is hide by default, and can be shown on click of user
    parameter name(string,required): dom id of this layer
    parameter title(string,required): title of layer window
    parameter width(string,optional): optionally set the width of layer
*/
    if(!is_null($content))
    {
        $width=isset($params["width"])?$params["width"]:300;
        $ret=<<<END
        <div id="{$params["name"]}" style="position:absolute;display:none">
        <table border="0" width={$width} bgcolor="#757575" cellspacing="0" cellpadding="1">
            <tr>
                <td width="100%">
                     <table border="0" width="100%" bgcolor="#ff9c00" cellspacing="0" cellpadding="1">
                         <tr>
                         <td width="100%">
                             <table border="0" width="100%" bgcolor="#ff9c00" cellspacing="0" cellpadding="0" style="cursor:hand; cursor:pointer;">
                                <tr><td width=265 onMouseDown="startMove(event,document.getElementById('{$params["name"]}')); return false;" onMouseUp="stopMove(); return false;">
                                     <font face="tahoma" color="#FFFFFF" style="font-size:8pt"><B>&nbsp;&nbsp;{$params["title"]}</b></font>
                                    </td>
                            <td width="35">
                                <a href="#" onClick="document.getElementById('{$params["name"]}').style.display='none';return false">
                                    <nobr><img src="/IBSng/images/icon/close.gif" border=0 width=32 height=16></a></td>
                     </tr>
                     </table>
                     </td>
                     </tr>
                     <tr>
                         <td width="100%" style="padding:2px">
                            <table border="0" width="100%" bgcolor="#FFFFFF" cellspacing="0" cellpadding="0">
                            <tr><td>            
                                {$content}
                            </td></tr>
                            </table>    
                         </td>
                     </tr>
                    </table> 
                </td>
            </tr>
        </table>
        </div>
END;
        return $ret;

    }
}

?>