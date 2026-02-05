from o2_concentrator_inventory_system import calculate_revenue, Inventory, HomeConcentrator, PediatricConcentrator

def test_calculate_revenue():
    assert calculate_revenue("525DD", "m") == 45.00
    assert calculate_revenue("1025DD", "m") == 75.00
    assert calculate_revenue("525DD", "f") == 299.98
    assert calculate_revenue("1025DD", "f") == 375.98
    assert calculate_revenue("P2", "f") == 298.98
    assert calculate_revenue("ANY", "q") == 0.00
    assert calculate_revenue("unknown", "z") == 0.00

def test_shipping():
    inv = Inventory()
    unit = HomeConcentrator("525DD", "RMA123", "Flat rate", 299.98, 5.0, "Completed", 40.0)
    inv.receive_unit(unit)
    assert len(inv._stock) == 1
    inv.ship_unit(unit)
    assert len(inv._stock) == 0

def test_receiving():
    inv = Inventory()
    unit = PediatricConcentrator("P2", "RMA555", "QM Warranty", 0.0, 1.5, "Not completed", 6)
    inv.receive_unit(unit)
    assert inv._stock[0]._rma == "RMA555"