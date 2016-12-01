{foreach from=$start_with_chars item=char key=index}
    {if $index%6 == 0}
        {multiTableTR}
    {/if}

    {reportToShowCheckBox name="username_`$char`" value=$char output=$char default_checked="" always_in_form=""}
{/foreach}

