from core.report.onlines_filter import OnlinesFilter

class UsernameOnlinesFilter(OnlinesFilter):
    """
        filter online users by username prefix
    """
    def appliesOnCond(self, conds):
        return conds.has_key("username_starts_with")
    
    def filter(self, user_obj, instance, conds):
        if user_obj.isNormalUser() and user_obj.getUserAttrs().hasAttr("normal_username"):
            attr_name = "normal_username"       
        elif user_obj.isVoIPUser() and user_obj.getUserAttrs().hasAttr("voip_username"):
            attr_name = "voip_username"
        else:
            return False

        for prefix in conds["username_starts_with"]:
            if user_obj.getUserAttrs()[attr_name].startswith(prefix):
                return True
    
        return False
