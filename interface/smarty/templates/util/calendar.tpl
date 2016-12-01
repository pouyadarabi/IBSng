  <link rel="stylesheet" type="text/css" media="all" href="/IBSng/js/calendar/calendar-win2k-1.css" />

  <script type="text/javascript" src="/IBSng/js/calendar/jalali.js"></script>
  <script type="text/javascript" src="/IBSng/js/calendar/jdate.js"></script>
  <script type="text/javascript" src="/IBSng/js/calendar/calendar.js"></script>
  <script type="text/javascript" src="/IBSng/js/calendar/calendar-setup.js"></script>

  <script type="text/javascript" src="/IBSng/js/calendar/calendar-JA.js"></script>
  <script type="text/javascript" src="/IBSng/js/calendar/calendar-en.js"></script>


<script type="text/javascript">
{literal}

function setup_calendar(input_id, trigger_id, calDateType){
    return Calendar.setup({
        dateType       :    calDateType,
        inputField     :    input_id,      // id of the input field
        showsTime      :    true,            // will display a time selector
        button         :    trigger_id,   // trigger for the calendar (button ID)
        ifFormat       :    "%Y/%m/%d %H:%M",       // format of the input field
        singleClick    :    false,           // double-click mode
        step           :    1                // show all years in drop-down boxes (instead of every other year as default)
    });
}
{/literal}
</script>
