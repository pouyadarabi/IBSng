<?php
function smarty_function_arraySizeof($params,&$smarty)
{/*

    param array(array,required): array that we will return size for

*/
    return sizeof($params["array"]);
}

?>