<pre>
Multiple String is a type in IBSng, to enter multiple values in one field.
They composed of one or more smaller strings. For example "name1,name2" is
a valid multi str, composed of two strings "name1" and "name2". 
if you click on multi str icon, beside a field, it will show you what strings
the multi str composed of. You can use two types of multi str operators to 
create a valid multi str. 
1. ",": separate each string member of multi str. ex: 1,2,3 will be expanded to "1 2 3"
2. ranges: You can specify a range in multi str. 
   ex: name&#123;1-6&#125; will  be expanded to "name1 name2 name3 name4 name5"
   ranges are start and end inclusive. if a range is more that 1 digit
   all range members will be padded to the biggest length
   ex. &#123;8-12&#125; will  be expanded to "08 09 10 11" 

Multiple Strings is very useful in ibs. You can enter them in many places to enter
more than value. For example to add a bunch of username, or to see multiple usernames
report, or change credit of multiple users.
Even it's useful when you're adding ras ports and ip pool ip's. Have eye for
multi str icon beside fields ;). If a field support multi str, it should have
a multi str icon beside it

TODO: add icon image, spell check or maybe rewrite!
</pre>