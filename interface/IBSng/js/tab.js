function Tab(tab_color)
{
    this.tab_color=tab_color;
    this.tab_names=Array();
    this.selected=null;
    this.form_name="";

    this.setFormName=setFormName;
    this.__changeFormSelected=__changeFormSelected;

    this.addTab=addTab;
    this.__setTabEventHandlers=__setTabEventHandlers;
    this.__setTabHoverCursor=__setTabHoverCursor;
    this. __addTabObj= __addTabObj;
    this.handleOnClick=handleOnClick;
    this.__unSelectFirst=__unSelectFirst;
    this.__unSelectMiddle=__unSelectMiddle;
    this.__selectFirst=__selectFirst;
    this.__selectMiddle=__selectMiddle;
    this.__changeImageTo=__changeImageTo;
    this.__changeStyleToGray=__changeStyleToGray;
    this.__changeStyleToSelected=__changeStyleToSelected;
    this.__changeContent=__changeContent;
    this.initContent=initContent;
}
    function addTab(tab_name)
    {
	this.tab_names.push(tab_name);
	this.__setTabEventHandlers(tab_name);
	this.__setTabHoverCursor(tab_name);
	this.__addTabObj(tab_name);
	if(this.selected==null)
	{
	    this.selected=tab_name;
    	    this.__changeStyleToSelected(tab_name);
	}
	else
	    this.__changeStyleToGray(tab_name);

    }
    
    function setFormName(form_name)
    {
	this.form_name=form_name;
    }	

    function __changeFormSelected(tab_name)
    {
	if(this.form_name!="")
	{
	    i=tab_name.indexOf("_");
	    table_id=tab_name.slice(0,i);
	    tab_value=tab_name.slice(i+1,tab_name.length);
	    
	    form_obj = eval("document."+this.form_name);
	    input_obj = eval("form_obj."+table_id+"_selected");

	    if (!input_obj)
	    {
		input_obj = document.createElement("INPUT");
		input_obj.name = table_id+"_selected";
		input_obj.type = "HIDDEN";
		form_obj.appendChild(input_obj);
	    }
	    input_obj.value=tab_value;
	}
	    
    }
    
    function __setTabEventHandlers(tab_name)
    {
	el=document.getElementById(tab_name+"_td");
	if(el.addEventListener)
	    el.addEventListener("click", this.handleOnClick, false);
	else if (el.attachEvent)
	    el.attachEvent("onclick",this.handleOnClick);
    }
    
    function __setTabHoverCursor(tab_name)
    {
	el=document.getElementById(tab_name+"_td");
	el.style.cursor="pointer";
    }

    function __addTabObj(tab_name)
    {
	el=document.getElementById(tab_name+"_td");
	el.tab_obj=this;
    }

    
    function handleOnClick(e)
    {
	if(e.target)
	    td_id=e.target.id;
	else if (e.srcElement)
	    td_id=e.srcElement.id;
	else
	    td_id=e;

	tab_name=td_id.substr(0,td_id.length-3);
	tab=document.getElementById(td_id).tab_obj;

	if(tab_name!=self.selected)
	{
	    if(tab.tab_names[0]==tab.selected)
		tab.__unSelectFirst(tab.selected);
	    else
		tab.__unSelectMiddle(tab.selected);
		
	    if(tab.tab_names[0]==tab_name)
		tab.__selectFirst(tab_name);
    	    else
		tab.__selectMiddle(tab_name);
	    tab.__changeContent(tab.selected,false);
	    tab.__changeContent(tab_name,true);
	    tab.selected=tab_name;
	    
	    tab.__changeFormSelected(tab_name);
	}
    }
    
    function __unSelectFirst(tab_name)
    {
	this.__changeImageTo(tab_name+"_begin","/IBSng/images/tab/begin_of_tab_gray_"+this.tab_color+".gif");
	this.__changeImageTo(tab_name+"_end","/IBSng/images/tab/end_of_tab_gray_"+this.tab_color+".gif");
	this.__changeStyleToGray(tab_name);
    }

    function __unSelectMiddle(tab_name)
    {
	this.__changeImageTo(tab_name+"_begin","/IBSng/images/tab/mid_begin_of_tab_gray_"+this.tab_color+".gif");
	this.__changeImageTo(tab_name+"_end","/IBSng/images/tab/end_of_tab_gray_"+this.tab_color+".gif");
	this.__changeStyleToGray(tab_name);
    }

    function __selectFirst(tab_name)
    {
	this.__changeImageTo(tab_name+"_begin","/IBSng/images/tab/begin_of_tab_"+this.tab_color+".gif");
	this.__changeImageTo(tab_name+"_end","/IBSng/images/tab/end_of_tab_"+this.tab_color+".gif");
	this.__changeStyleToSelected(tab_name);

    }
    
    function __selectMiddle(tab_name)
    {
	this.__changeImageTo(tab_name+"_begin","/IBSng/images/tab/mid_begin_of_tab_"+this.tab_color+".gif");
	this.__changeImageTo(tab_name+"_end","/IBSng/images/tab/end_of_tab_"+this.tab_color+".gif");
	this.__changeStyleToSelected(tab_name);
    }
    
    function __changeImageTo(img_id,img_src)
    {
	img_el=document.getElementById(img_id);
	img_el.src=img_src;
    }

    function __changeStyleToGray(tab_name)
    {
	td_el=document.getElementById(tab_name+"_td");
	td_el.style.backgroundColor="#929292";
	td_el.style.backgroundImage="url('/IBSng/images/tab/middle_of_tab_gray_"+this.tab_color+".gif')";
	td_el.style.height=18;
    }    

    function __changeStyleToSelected(tab_name)
    {
	td_el=document.getElementById(tab_name+"_td");
	td_el.style.backgroundImage="";
	if(this.tab_color=="red")
	    td_el.style.backgroundColor="#9A1111";
	else if (this.tab_color=="orange")
	    td_el.style.backgroundColor="#FF9C00 ";
	td_el.style.height=20;
    }    

    function __changeContent(tab_name,display)
    {
	content=document.getElementById(tab_name+"_content");
	if(content)
	    if(display)
		content.style.display="";
	    else
		content.style.display="none";
    }
    

    function initContent(tab_name)
    {
	if(tab_name!=this.selected)
	    this.__changeContent(tab_name,false);
    }