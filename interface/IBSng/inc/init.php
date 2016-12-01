<?php
require_once ("defs.php");
require_once (IBSINC."session.php");
require_once (IBSINC."errors.php");
require_once (IBSINC."error.php");
require_once (IBSINC."auth.php");
require_once (IBSINC."request.php");
require_once (IBSINC."smarty.php");
require_once (IBSINC."lib.php");
require_once (IBSINC."lang.php");

session_init();
auth_init();

require_once (IBSINC."referrer.php");

?>