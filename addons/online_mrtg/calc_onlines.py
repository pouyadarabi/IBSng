
admin_username=sys.argv[1]




def sendRequest(admin_username,admin_password):
    server=xmlrpclib.ServerProxy("http://localhost:1235")
    return getattr(server,"report.getOnlineUsers")({"sort_by":"user_id",
                                                "auth_name":admin_username,
                                                "auth_pass":admin_password,
                                                "auth_type":"ADMIN",
                                                "auth_remoteaddr":"127.0.0.1"
                                                })
