<?php
function smarty_modifier_duration($seconds)
{       /*
            make seconds look like durations in format xxxx:xx:xx
        */
    return formatDuration($seconds);
}
?>
