from core.user import user_main
attr_manager=user_main.getAttributeManager()
search_helper=attr_manager.runAttrSearchers({"normal_username_op":"like","normal_username":"a{1-10}"})

#               {"normal_charge":["test","123"],
#               "group_name":["asd","1234"],
#               "normal_username":"a{1-10}",
print str(search_helper.createQuery())
