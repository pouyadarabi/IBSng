<?php

require_once (IBSINC."xml.php");
require_once (IBSINC."generator/mygenerator.php");

/**
 */
class XmlGenerator extends MyGenerator
{
	/**
	 * @access public
	 */
	function XmlGenerator($root, $element)
	{
		$this->root = $root;
		$this->element = $element;
	}
	function doArray($array)
	{
		return "<{$this->element}>".convDicToXML($array)."</{$this->element}>";
	}

	function init()
	{
		return "<{$this->root}>";
	}

	function dispose()
	{
		return "</{$this->root}>";
	}

}