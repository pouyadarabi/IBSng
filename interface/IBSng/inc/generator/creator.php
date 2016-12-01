<?php
/**
 * 
 * creator.php
 * 
 * */
class Creator
{
    /**
     * will initialize variables and will call at
     * first time.
     * @access public
     * @author hossein zolfi
     * */
    function init()
    {
        $this->controller = NULL;
    }
    
    /**
     * register controller
     * @param Controller $controller  
     * */
    function registerController (& $controller)
    {
		$this->controller = & $controller;
    }

    /**
     * this method will be called at end of generation
     * you can override this.
     * @access public
     * @author hossein zolfi
     * */
    function dispose()
    {
    }
}
?>