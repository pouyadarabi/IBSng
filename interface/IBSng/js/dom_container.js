function DomContainer()
{/* Dom Container keep html elements refrenced by dom ids.
    it's capable of selecting on of elements , and change attributes of the selected element
    (ex. changing background..)

*/
    this.objs=new Array();
    this.dependent_objs=Array();
    this.set_on_select=Array(); /*array of arrays*/
    this.set_on_unselect=Array(); /*array of arrays*/
    this.__selected="";
    this.disable_unselected=false;
    
    this.disable=disable
    this.setAttribute=setAttribute;
    this.__addObj=__addObj;
    this.addByID=addByID;
    this.setOnSelect=setOnSelect;
    this.setOnUnSelect=setOnUnSelect;
    this.select=select;
    this.toggle=toggle;
    this.__getObjByID=__getObjByID;
    this.__setSelectedAttrs=__setSelectedAttrs;
    this.__setSelectedAttr=__setSelectedAttr;
    this.__setUnselectedsAttrs=__setUnselectedsAttrs;
    this.__setUnselectedAttr=__setUnselectedAttr;
    this.__addDependents=__addDependents;

}
    function setAttribute(obj,attr_name,attr_value)
    {
	eval("obj.style."+attr_name+"=attr_value");
    }

    function disable(obj,disable_status)
    {
	if(obj && obj.disabled!=undefined)
	    obj.disabled=disable_status;
    }
    
    function __addObj(obj)
    {
	this.objs.push(obj);
    }

    function addByID(dom_id,dependent_ids)
    {/*add a new element with id "dom_id"
       dependent_ids is array of id's that will be selected when dom_id is selected too 
    */
	obj = document.getElementById(dom_id);
	if(!obj)
	{
	    alert(dom_id);
	    return null;
	}
	this.__addObj(obj);
	this.__addDependents(dependent_ids);
    }

    function __addDependents(dependent_ids)
    {
	dep_objs=new Array();
	for (dep_index in dependent_ids)
	    dep_objs.push(document.getElementById(dependent_ids[dep_index]));
        this.dependent_objs.push(dep_objs);
    }
    function setOnSelect(attr_name,attr_value)
    {/*
	add a new attribute to set when element is selected
    */
	this.set_on_select.push(new Array(attr_name,attr_value));
    }

    function setOnUnSelect(attr_name,attr_value)
    {/*
	add a new attribute to set when element is unselected
    */
	this.set_on_unselect.push(new Array(attr_name,attr_value));
    }
    
    
    function toggle(id)
    {/*toggle of element, useful for on/off situations*/
	if(this.__selected==id)
	    this.select("dummy_id");
	else
	    this.select(id);
    }
    
    function select(id)
    {/* select of elements */
	this.__selected=id;
	this.__setSelectedAttrs(id);
	this.__setUnselectedsAttrs(id);
    }
    
    function __getObjByID(id)
    {
	for (obj_index in this.objs)
	{
	    if (this.objs[obj_index].id == id)
		return new Array(this.objs[obj_index],this.dependent_objs[obj_index]);
	}
	return null;
    }
    
    function __setSelectedAttrs(id)
    {

	arr=this.__getObjByID(id);
	if(!arr)
	    return;
	    
	obj=arr[0];
	dependents=arr[1];
	this.__setSelectedAttr(obj);
	for (dep_index in dependents)
	    this.__setSelectedAttr(dependents[dep_index]);
    }


    function __setSelectedAttr(obj)
    {
	for (attr_index in this.set_on_select)
	{
	    attr_name=this.set_on_select[attr_index][0];
	    attr_value=this.set_on_select[attr_index][1];
	    this.setAttribute(obj,attr_name,attr_value);
	}

	if(this.disable_unselected)
	    this.disable(obj,false);

    }
    
    function __setUnselectedsAttrs(id)
    {
	for (obj_index in this.objs)
	{
	    if (this.objs[obj_index].id == id)
		continue;

	    obj=this.objs[obj_index];
	    this.__setUnselectedAttr(obj);
	    for (dep_index in this.dependent_objs[obj_index])
		this.__setUnselectedAttr(this.dependent_objs[obj_index][dep_index]);
	}
    }

    function __setUnselectedAttr(obj)
    {
        for (attr_index in this.set_on_unselect)
        {
    	    attr_name=this.set_on_unselect[attr_index][0];
	    attr_value=this.set_on_unselect[attr_index][1];
	    this.setAttribute(obj,attr_name,attr_value);
	}

	if(this.disable_unselected)
	    this.disable(obj,true);

    }
