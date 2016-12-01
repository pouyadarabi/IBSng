/* WARNING: Current implemention requires that an input checkbox should be only member of one container */

function CheckBoxContainer(name) 
{
    this.init(name);
}

    CheckBoxContainer.prototype.init=function(name)
    {
	this.check_box_objs=new Array();
	this.name=name
	/*methods*/
	this.add=add
	this.addByName=addByName
	this.allChecked=allChecked
	this.allUnChecked=allUnChecked
        this.checkAll=checkAll
	this.unCheckAll=unCheckAll
	this.setCheck=setCheck
        this.reverse=reverse
        this.setCheckAll=setCheckAll
    }

    function add(check_box_obj)
    {/*
	Add new checkbox object to container
    */
	this.check_box_objs.push(check_box_obj);
	check_box_obj.onclick=checkBoxOnClick;
	check_box_obj.container=this;
    }
    
    function addByName(form_name,check_box_name)
    {/*
	Add new checkbox to container
    */
//	eval("document."+form_name+"."+check_box_name).checked=true;
	this.add(eval("document."+form_name+"."+check_box_name));
    }

    function allChecked()
    {/*
	return True if all check boxes in container is checked now
    */	
	if (this.check_box_objs.length==0)
	    return false;
	for (index in this.check_box_objs)
	    if (this.check_box_objs[index].checked==false)
		return false;	    
	return true;
    }

    function allUnChecked()
    {/*
	return True if all check boxes in container is unchecked now
    */	
	if (this.check_box_objs.length==0)
	    return true;
	for (index in this.check_box_objs)
	    if (this.check_box_objs[index].checked==true)
		return false;
	return true;
    }
    
    function checkAll()
    {/*
	check all of checkboxes in container
    */
	this.setCheck(true);
    }

    function unCheckAll()
    {/*
	check all of checkboxes in container
    */
	this.setCheck(false);
    }
    
    function setCheck(bool)
    {
	for (index in this.check_box_objs)
	{
	    this.check_box_objs[index].checked=bool;
	}
    }
    
    function reverse()
    {
	if(this.allChecked())
	    this.unCheckAll();
	else
	    this.checkAll();
    }
    
    function setCheckAll(form_name,check_box_name)
    {/*
	set check all input box for container
	checkall input box will check or uncheck all check boxes
    */
	this.check_all=eval("document."+form_name+"."+check_box_name);
	this.check_all.container=this;
	this.updateCheckAll();
	this.check_all.onclick=checkAllOnClick;

    }

CheckBoxContainer.prototype.updateCheckAll=function()
    {/*
	update check all status. this test if all checkboxes are checked, then check the checkall box
	else uncheck it
    */
	if (this.allChecked())
	    this.check_all.checked=true;
	else
	    this.check_all.checked=false;
    }    

function checkAllOnClick(evt)
{
    if (evt && evt.target)
	evt.target.container.reverse();
    if (window.event && window.event.srcElement)
	window.event.srcElement.container.reverse();
}

function checkBoxOnClick(evt)
{
    if (evt && evt.target)
        evt.target.container.updateCheckAll();
    if (window.event && window.event.srcElement)
	window.event.srcElement.container.updateCheckAll();
}
