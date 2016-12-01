<?php

function smarty_block_userInfoTD($params,$content,&$smarty,&$repeat)
{/*     Create an userinfo style column. Also TR s are created when needed
        parameter comment(boolean,optional): if set to "TRUE", create a td suitable for comments, both
                                            "user_left" and "user_right" and "group" tds should have this flag set
        parameter type("string",required): can be one of "user_left" , "user_right" and "group"
                                           
*/
    
    if(!is_null($content))
    {
        $type=$params["type"];
        if(isset($params["comment"]) and $params["comment"]=="TRUE")
        {
            if($type=="user_left")
            {
                $color=getTRColor(TRUE);
                return <<<END
        <tr>
                <!-- Form Text Area userinfo -->
                <td class="Form_Content_Row_Left_textarea_userinfo" colspan="2" valign="Top">
                <table border="0" width="100%" cellspacing="0" cellpadding="0">
                        <tr>
                                <td class="Form_Content_Row_Begin"><img border="0" src="/IBSng/images/row/begin_of_row_{$color}.gif"></td>
                                <td class="Form_Content_Row_Left_Textarea_Td_{$color}"><nobr>{$content}</nobr></td>
                                <td class="Form_Content_Row_End"><img border="0" src="/IBSng/images/row/end_of_row_{$color}.gif"></td>
                        </tr>
                </table>
                </td>
                
END;
            }
            else if($type=="user_right")
            {
                $color=getTRColor();
                return <<<END
                <td class="Form_Content_Row_Right_textarea_userinfo" colspan="2">
                <table border="0" width="100%" cellspacing="0" cellpadding="0" height="100%">
                                
                        <tr>
                                <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/top_left_of_comment_{$color}.gif"></td>
                                <td class="Form_Content_Row_Top_textarea_line_{$color}"></td>
                                <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/top_right_of_comment_{$color}.gif"></td>
                                <td width=1 rowspan=3><font style="font-size:8pt">&nbsp;</font></td>
                        </tr>
                        </tr>
                        <tr>
                                <td colspan="3" class="Form_Content_Row_Right_textarea_td_{$color}" style="height: 100%">
                                {$content}</td>
                        </tr>
                        
                        <tr>
                                <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/bottom_left_of_comment_{$color}.gif"></td>
                                <td class="Form_Content_Row_Bottom_textarea_line_{$color}">&nbsp;</td>
                                <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/bottom_right_of_comment_{$color}.gif"></td>
                        </tr>
                                
                </table>
                </td>
    
END;
            }
            else  if($type=="group")
            {
                $color=getTRColor();
                return <<<END
                <td class="Form_Content_Row_Right_textarea_groupinfo" colspan="3" valign="top">
                        <table border="0" width="100%" height="100%" cellspacing="0" cellpadding="0" >
                <tr>
                                <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/top_left_of_comment_{$color}.gif"></td>
                                <td class="Form_Content_Row_Top_textarea_line_{$color}"></td>
                                <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/top_right_of_comment_{$color}.gif"></td>
                        </tr>
                        <tr>
                                <td colspan="3" class="Form_Content_Row_Right_textarea_td_{$color}"><nobr>{$content}</td>
                        </tr>
                        <tr>
                        <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/bottom_left_of_comment_{$color}.gif"></td>
                        <td class="Form_Content_Row_Bottom_textarea_line_{$color}">&nbsp;</td>
                        <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/bottom_right_of_comment_{$color}.gif"></td>
                        </tr>
                </table>
                <!-- End Form Text Area userinfo-->
</td>
        </tr>
    <tr>
                <td colspan="7" class="Form_Content_Row_Space"></td>
        </tr>
END;
            
            }

        }
        else //Normal (Not comment) style)
        {
            if($type=="user_left")
            {
                $color=getTRColor(TRUE);
                return <<<END
        <tr>
                <td class="Form_Content_Row_Begin"><img border="0" src="/IBSng/images/row/begin_of_row_{$color}.gif"></td>
                <td class="Form_Content_Row_Left_userinfo_{$color}"><nobr>{$content}</nobr></td>
END;
            }
            else if($type=="user_right")
            {
                $color=getTRColor();
                return <<<END
                <td class="Form_Content_Row_Right_userinfo_{$color}">{$content}</td>
                <td class="Form_Content_Row_End"><img border="0" src="/IBSng/images/row/end_of_row_{$color}.gif"></td>
                <td class="Form_Content_Row_Begin"><img border="0" src="/IBSng/images/row/begin_of_row_{$color}.gif"></td>
END;
            }
            else  if($type=="group")
            {
                $color=getTRColor();
                return <<<END
                <td class="Form_Content_Row_groupinfo_{$color}" align=center>{$content}</td>
                <td class="Form_Content_Row_End"><img border="0" src="/IBSng/images/row/end_of_row_{$color}.gif"></td>
        <tr>
                <td colspan="7" class="Form_Content_Row_Space"></td>
        </tr>
END;
            }
            
        }
    }
}

?>