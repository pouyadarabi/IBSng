from core.user import user_main
user_obj=user_main.getUserPool().getUserByID(222)
print user_obj.hasAttr("normal_username")
user_attrs=user_obj.getUserAttrs().getAllAttributes()
for attr in user_attrs: 
        print attr,user_attrs[attr]
