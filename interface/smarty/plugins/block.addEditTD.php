<?php

function smarty_block_addEditTD($params,$content,&$smarty,&$repeat)
{/*     Create an Add edit style column. Also TR s are created when needed
        parameter type("string",required): show td type, for 1 column table can be "left" and "right"
                                           and for 2 column tables can be "left1" "right1" "left2" "right2"

        parameter double(boolean,optional): if true, create a td suitable for double column tables
                                            all of "left1" "left2" "right1" "right2" td s should have
                                            this flag set
        parameter comment(boolean,optional): if true, create a td suitable for comments, both
                                            "left" and "right" tds should have this flag set

        parameter id("string",optional): set optional id tag of td WARNING XXX: not set for all type
        parameter err(string,optional)
*/
    
    if(!is_null($content))
    {
        if(in_array($params["type"],array("left","left1","left2")) and trim($content)!="")
            $content.=" :";

        $ret="";
        $err_star_img_link="<img src='/IBSng/images/msg/error.gif'> ";
        if (isset($params["err"]) and $smarty->is_assigned($params["err"]) and $smarty->get_assigned_value($params["err"])==TRUE)
            $err_star=$err_star_img_link;
        else
            $err_star="";

        $id=isset($params["id"])?"id={$params["id"]}":"";

        if(isset($params["double"]) and $params["double"]=="TRUE" and isset($params["comment"]) and $params["comment"]=="TRUE")
        {
            if($params["type"]=="left")
            {
                $color=getTRColor(TRUE);
                $ret=<<<END
        <tr>
                <!-- Form Text Area -->
                <td class="Form_Content_Row_Left_Textarea_2col" valign="top" colspan="2">
                <table border="0" width="100%" cellspacing="0" cellpadding="0">
                        <tr>
                                <td class="Form_Content_Row_Begin"><img border="0" src="/IBSng/images/row/begin_of_row_{$color}.gif"></td>
                                <td class="Form_Content_Row_Left_textarea_td_{$color}">{$content}</td>
                                <td class="Form_Content_Row_End"><img border="0" src="/IBSng/images/row/end_of_row_{$color}.gif"></td>
                        </tr>
                </table>
                </td>

END;
            }
            else if ($params["type"]=="right")
            {
                $color=getTRColor();
                $ret=<<<END

                <td colspan="7" class="Form_Content_Row_Right_Textarea_2col">
                <table border="0" width="100%" cellspacing="0" cellpadding="0" >
                        <tr>
                                <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/top_left_of_comment_{$color}.gif"></td>
                                <td class="Form_Content_Row_Top_textarea_line_{$color}"></td>
                                <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/top_right_of_comment_{$color}.gif"></td>
                        </tr>
                        <tr>
                                <td class="Form_Content_Row_Left_textarea_line_{$color}">&nbsp;</td>
                                <td class="Form_Content_Row_Right_textarea_td_{$color}">{$content}</td>
                                <td class="Form_Content_Row_Right_textarea_line_{$color}">&nbsp;</td>
                        </tr>
                        <tr>
                                <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/bottom_left_of_comment_{$color}.gif"></td>
                                <td class="Form_Content_Row_Bottom_textarea_line_{$color}">&nbsp;</td>
                                <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/bottom_right_of_comment_{$color}.gif"></td>
                        </tr>
                </table>
                </td>
                <!-- End Form Text Area -->
                <tr>
                    <td colspan="9" class="Form_Content_Row_Space"></td>
                </tr>

END;
            }
        
        } //end comment double


        else if(isset($params["double"])and $params["double"]=="TRUE")
        {
            if($params["type"]=="left1")
            {
                $color=getTRColor(TRUE);
                $ret=<<<END
        <tr>
                <td class="Form_Content_Row_Begin"><img border="0" src="/IBSng/images/row/begin_of_row_{$color}.gif"></td>
                <td class="Form_Content_Row_Left_2col_{$color}">{$err_star}{$content}</td>
END;
            }
            else if ($params["type"]=="right1")
            {
                $color=getTRColor();
                $ret=<<<END
                <td class="Form_Content_Row_Right_2col_{$color}">{$content}</td>
                <td class="Form_Content_Row_End"><img border="0" src="/IBSng/images/row/end_of_row_{$color}.gif"></td>
END;
            }
            else if($params["type"]=="left2")
            {
                $color=getTRColor();
                $ret=<<<END
                <td class="Form_Content_Col_Space">&nbsp;</td>
                
                <td class="Form_Content_Row_Begin"><img border="0" src="/IBSng/images/row/begin_of_row_{$color}.gif"></td>
                <td class="Form_Content_Row_Left_2col_{$color}">{$err_star} {$content}</td>

END;
            }
            else if ($params["type"]=="right2")
            {
                $color=getTRColor();
                $ret=<<<END
                <td class="Form_Content_Row_Right_2col_{$color}">{$content}</td>
                <td class="Form_Content_Row_End"><img border="0" src="/IBSng/images/row/end_of_row_{$color}.gif"></td>
                
        </tr>
                <tr>
                    <td colspan="9" class="Form_Content_Row_Space"></td>
                </tr>

END;
            }

            
        } //end double
        else if (isset($params["comment"]) and $params["comment"]=="TRUE")
        {
            if($params["type"]=="left")
            {
                $color=getTRColor(TRUE);
                $ret=<<<END
<tr>
                <!-- Form Text Area -->
                <td class="Form_Content_Row_Left_Textarea" valign="top" colspan="2">
                <table border="0" width="100%" cellspacing="0" cellpadding="0">
                        <tr>
                                <td class="Form_Content_Row_Begin"><img border="0" src="/IBSng/images/row/begin_of_row_{$color}.gif"></td>
                                <td class="Form_Content_Row_Left_textarea_td_{$color}">{$content}</td>
                                <td class="Form_Content_Row_End"><img border="0" src="/IBSng/images/row/end_of_row_{$color}.gif"></td>
                        </tr>
                </table>
                </td>
END;
            } 
            else //type is right
            {
                $color=getTRColor();
                $ret=<<<END
                <td colspan="2" class="Form_Content_Row_Right_Textarea">
                <table border="0" width="100%" cellspacing="0" cellpadding="0" >
                        <tr>
                                <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/top_left_of_comment_{$color}.gif"></td>
                                <td class="Form_Content_Row_Top_textarea_line_{$color}"></td>
                                <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/top_right_of_comment_{$color}.gif"></td>
                        </tr>
                        <tr>
                                <td class="Form_Content_Row_Left_textarea_line_{$color}">&nbsp;</td>
                                <td class="Form_Content_Row_Right_textarea_td_{$color}">{$content}</td>
                                <td class="Form_Content_Row_Right_textarea_line_{$color}">&nbsp;</td>
                        </tr>
                        <tr>
                                <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/bottom_left_of_comment_{$color}.gif"></td>
                                <td class="Form_Content_Row_Bottom_textarea_line_{$color}">&nbsp;</td>
                                <td class="Form_Content_Row_Textarea_corner"><img border="0" src="/IBSng/images/comment/bottom_right_of_comment_{$color}.gif"></td>
                        </tr>
                </table>
                </td>
                <!-- End Form Text Area -->
                <tr>
                <td colspan="4" class="Form_Content_Row_Space"></td>
        </tr>
END;
            }
        
        
        }//end comment
        else //normal 1 row table
        {
            if($params["type"]=="left")
            {
                $color=getTRColor(TRUE);
                $ret=<<<END
        <tr {$id}>
                <td class="Form_Content_Row_Begin"><img border="0" src="/IBSng/images/row/begin_of_row_{$color}.gif"></td>
                <td class="Form_Content_Row_Left_{$color}">{$err_star} {$content}</td>
END;
            }
            else //type is right
            {
                $color=getTRColor();
                $ret=<<<END
                <td class="Form_Content_Row_Right_{$color}">{$content}</td>
                <td class="Form_Content_Row_End"><img border="0" src="/IBSng/images/row/end_of_row_{$color}.gif"></td>
        </tr>
        <tr>
                <td colspan="4" class="Form_Content_Row_Space"></td>
        </tr>
END;
            }
        }

        return $ret;
    }
    
}

