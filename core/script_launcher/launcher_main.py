from core.script_launcher.launcher import ScriptLauncher

def init():
    global script_launcher
    script_launcher = ScriptLauncher()


def getLauncher():
    return script_launcher
