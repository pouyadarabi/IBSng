from core.charge import charge_main
charge_obj=charge_main.getLoader().getChargeByName('test')
rules=charge_obj.getRules()
print rules[8].interval.containsNow()
