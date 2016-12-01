from core.ras import ras_main
ras_obj=ras_main.getLoader().getRasByIP('127.0.0.2')
print ras_obj.onlines
print ras_obj.waitings
