<?php
require_once("../../inc/init.php");
require_once(IBSINC."dialer.php");
require_once(IBSINC."user.php");

needDialerAuth();

print answerDialer(TRUE,"");
?>
