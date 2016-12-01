<?php
require_once("init.php");
require_once(SMARTY_DIR."Smarty.class.php");


class IBSSmarty extends Smarty 
{
   function IBSSmarty()
   {
        $this->Smarty();

        $this->template_dir = SMARTY_ROOT.'templates/';
        $this->compile_dir = SMARTY_ROOT.'templates_c/';
        $this->config_dir = SMARTY_ROOT.'configs/';
        $this->cache_dir = SMARTY_ROOT.'cache/'; 

        $this->caching = false;

        $this->plugins_dir[] = SMARTY_ROOT.'plugins/';


        $this->setIBSDefinedVars();
        $this->setAuthVars();
//      $this->register_outputfilter("stripPostFilter");
   }

    function setAuthVars()
    {/* set authenticated user variables in smarty variable
        
     */
        $auth=getAuth();
        $this->assign("auth_type",$auth->getAuthType());
        $this->assign("auth_name",$auth->getAuthUsername());
    }

    function setIBSDefinedVars()
    {
        $this->assign("MONEY_UNIT",MONEY_UNIT);
        $this->assign("IBSNG_VERSION",IBSNG_VERSION);
        $this->assign("DATE_TYPE",getDateType());
        $this->assign("LANGUAGE",getLang());
    }

    /**
     * check if varibale assigned in template
     *
     * @param string $tpl_var the template variable name
     * 
     */
    function is_assigned($tpl_var)
    {
        return isset($this->_tpl_vars[$tpl_var]);
    }

    function get_assigned_value($tpl_var)
    {
        return $this->_tpl_vars[$tpl_var];
    }


    function assign_array($arr)
    {/*Assign members of $arr*/
        foreach($arr as $key=>$value)
            if(is_array($value))
                $this->assign_by_ref($key,$arr[$key]);
            else
                $this->assign($key,$value);
    }

    function set_field_errs($vars_keys,$err_keys)
    {/* set errors in $err_keys(an array of error keys) in $smarty_obj
        $vars_keys is an array of array(smarty_err_var_name=>array(error_keys))
        it means set smarty_err_var_name to TRUE if on of my error_keys is in $err_keys
     */
        $set_keys=array();
        foreach($err_keys as $err_key)
            foreach($vars_keys as $var_name=>$keys)
                if(in_array($err_key,$keys))
                {
                    $this->assign($var_name,TRUE);
                    unset($vars_keys[$var_name]); //changing loop array in loop!!!
                }
                
        foreach ($vars_keys as $var_name=>$keys)
                $this->assign($var_name,FALSE);

    }

    function set_page_error($errs)
    { /* set page err_msgs array in smarty or append previous array values 
         It means you can call this multiple times within a single page, and all of errors will be shown.    
    */
        if(!is_array($errs))
            $errs=array($errs);
        
        if ($this->is_assigned("err_msgs"))
            foreach($errs as $err)
                $this->append("err_msgs",$err);
        else    
            $this->assign("err_msgs",$errs);
    }

}

function stripPostFilter($tpl_source,&$smarty)
{
    $search=array("/[\n\t\r]/","/>\s+</","/\s{2,}/");
    $replace=array("","><","");
    $tpl_source=preg_replace($search,$replace,$tpl_source);
    return $tpl_source;
}

?>
