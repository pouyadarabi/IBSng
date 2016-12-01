<?php

class Creator
{

    function init()
    {
        $this->controller = NULL;
    }

    function registerController (& $controller)
    {
		$this->controller = & $controller;
    }

    function dispose()
    {
    }
}