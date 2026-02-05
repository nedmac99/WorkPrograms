import sys
import csv
from pathlib import Path

file_path = Path(__file__).parent / "units.csv"

class Concentrator:
    def __init__(self, model, rma, warranty_type, revenue, flow_rate, is_repaired):
        self._model = model
        self._rma = rma
        self._warranty_type = warranty_type
        self._revenue = float(revenue)
        self._flow_rate = flow_rate
        self._is_repaired = is_repaired

    @property
    def warranty_type(self):
        return self._warranty_type
    
    @property
    def is_repaired(self):
        return self._is_repaired

    @is_repaired.setter
    def is_repaired(self, value):
        self._is_repaired = value

    def get_info(self):
        return f"Model: {self._model} - RMA: {self._rma} | Warranty Type: {self._warranty_type} | Revenue: ${self._revenue} | Flow Rate: {self._flow_rate}L | Repaired: {self._is_repaired}"

    def __str__(self):
        return self.get_info()


class HomeConcentrator(Concentrator):
    def __init__(self, model, rma, warranty_type, revenue, flow_rate, is_repaired, noise_level):
        super().__init__(model, rma, warranty_type, revenue, flow_rate, is_repaired)
        self._noise_level = float(noise_level)

    def get_info(self):
        return super().get_info() + f" | Noise level: {self._noise_level} dB"


class PortableConcentrator(Concentrator):
    def __init__(self, model, rma, warranty_type, revenue, flow_rate, is_repaired, battery_level):
        super().__init__(model, rma, warranty_type, revenue, flow_rate, is_repaired)
        self._battery_level = battery_level

    def get_info(self):
        return super().get_info() + f" | Battery level: {self._battery_level}%"


class PediatricConcentrator(Concentrator):
    def __init__(self, model, rma, warranty_type, revenue, flow_rate, is_repaired, age):
        super().__init__(model, rma, warranty_type, revenue, flow_rate, is_repaired)
        self._age = age

    def get_info(self):
        return super().get_info() + f" | Age: {self._age}"


class Inventory:
    def __init__(self):
        self._stock = []

    def receive_unit(self, unit):
        if any(u._rma == unit._rma for u in self._stock):
            print(f"\nRMA {unit._rma} already exists! Unit not added.\n")
        else:
            self._stock.append(unit)

    def ship_unit(self, unit):
        if unit in self._stock:
            self._stock.remove(unit)
        else:
            print("\nUnit not found!\n")

    def check_repair_status(self, rma):
        unit = next((u for u in self._stock if u._rma == rma), None)
        return unit._is_repaired if unit else None
    
    def check_warranty_type(self, rma):
        unit = next((u for u in self._stock if u._rma == rma), None)
        return unit._warranty_type if unit else None

    def show_stock(self):
        if not self._stock:
            return "No units in inventory"
        else:
            return "\n".join([str(unit) for unit in self._stock])

    def show_revenue(self):
        return f"Total Revenue value: ${sum(unit._revenue for unit in self._stock):.2f}"


def main():
    inv = load_units_from_csv()
    while True:
        selection = input(
            "Enter selection: \n1.Receive unit\n2.Ship unit\n3.Check repair status\n4.Change repair status\n5.View inventory\n6.Show revenue\n7.Check warranty type\n8.Exit\n"
        )

        if selection == "1":
            receiving(inv)

        elif selection == "2":
            shipping(inv)

        elif selection == "3":
            if not inv._stock:
                print("No units in inventory")
                continue
            rma = input("Enter RMA to check repair status: ").strip().upper()
            status = inv.check_repair_status(rma)
            if status is not None:
                print(f"Repair status: {status}")
            else:
                print("\nUnit not found!\n")

        elif selection == "4":
            if not inv._stock:
                print("No units in inventory")
                continue
            rma = input("Enter RMA of unit to update repair status: ").strip().upper()
            unit = next((u for u in inv._stock if u._rma == rma), None)
            if unit:
                while True:
                    new_status = input("Enter new status (y for completed / n for not completed): ").lower()
                    if new_status == "y":
                        unit.is_repaired = "Completed"
                        print(f"Repair status updated to Completed for RMA {rma}")
                        break
                    elif new_status == "n":
                        unit.is_repaired = "Not completed"
                        print(f"Repair status updated to Not completed for RMA {rma}")
                        break
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
            else:
                print("Unit not found.")

        elif selection == "5":
            print(f"\n{inv.show_stock()}\n")

        elif selection == "6":
            print(f"\n{inv.show_revenue()}\n")

        elif selection == "7":
            if not inv._stock:
                print("No units in inventory")
                continue
            rma = input("Enter RMA to check warranty type: ").strip().upper()
            w_type = inv.check_warranty_type(rma)
            print(f"Warranty type: {w_type}")

        elif selection == "8":
            save_units_to_csv(inv._stock)
            print("\nSaved!\n")
            sys.exit(
                "-------------------------------------------------------\nThank you for using my O2 Inventory management system!\n-------------------------------------------------------"
            )
        else:
            print("Invalid input!")


def receiving(inv):
    while True:
        type = input(
            "Enter type of unit to receive: \n1.Home\n2.Portable\n3.Pediatric\n4.Exit\n"
        )

        if type == "1":
            model, rma, warranty_type, revenue, flow_rate, is_repaired = receive("HomeConcentrator")
            noise_level = input("Enter noise level in dB: ")
            unit = HomeConcentrator(
                model, rma, warranty_type, revenue, flow_rate, is_repaired, noise_level
            )
            inv.receive_unit(unit)
            print(f"\nUnit received\n")

        elif type == "2":
            model, rma, warranty_type, revenue, flow_rate, is_repaired = receive("PortableConcentrator")
            battery_level = input("Enter battery level: ")
            unit = PortableConcentrator(
                model, rma, warranty_type, revenue, flow_rate, is_repaired, battery_level
            )
            inv.receive_unit(unit)
            print(f"\nUnit received\n")

        elif type == "3":
            model, rma, warranty_type, revenue, flow_rate, is_repaired = receive("PediatricConcentrator")
            age = input("Enter patients age: ")
            unit = PediatricConcentrator(
                model, rma, warranty_type, revenue, flow_rate, is_repaired, age
            )
            inv.receive_unit(unit)
            print(f"\nUnit received\n")

        elif type == "4":
            break

        else:
            print("Invalid Input")


def receive(unit_type):
    model = input("Enter Model type: ").upper()
    rma = input("Enter RMA: ").strip().upper()
    
    while True:
        warranty_code = input("Enter warranty type Manufature Warranty(m), Flat rate(f), QM Warranty(q): ").lower()
        if model == "P2":
            if warranty_code in ["m", "q"]:
                print("Invalid warranty type for P2")
                continue

        if warranty_code == "m":
            warranty_type = "Manufacture Warranty"
            break

        elif warranty_code == "f":
            warranty_type = "Flat rate"
            break

        elif warranty_code == "q":
            warranty_type = "QM Warranty"
            break

        else:
            print("Invalid input")
            
    revenue = calculate_revenue(model, warranty_code)
    
    while True:
        try:
            flow_rate = float(input("Enter Flow Rate in liters: "))
            if flow_rate < 0:
                print("Cannot have negative flow rate. Please re-enter.")
                continue
            if unit_type == "PediatricConcentrator" and flow_rate > 2:
                print("Flow rate for Pediatric units cannot exceed 2 liters. Please re-enter.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for flow rate.")
    while True:
        is_repaired = input("Is the unit repaired(y/n): ").lower()
        if is_repaired == "y":
            is_repaired = "Completed"
            break

        elif is_repaired == "n":
            is_repaired = "Not completed"
            break

        else:
            print("Incorrect input")

    return model, rma, warranty_type, revenue, flow_rate, is_repaired


def shipping(inv):
    while True:
        if not inv._stock:
            print("\nNo units available to ship.\n")
            break
        print("\nCurrent Inventory: \n")
        print(f"\n{inv.show_stock()}\n")
        rma = input("\nEnter RMA of unit to ship or c to cancel: \n").strip().upper()

        if rma.lower() == "c":
            break
        unit = next((u for u in inv._stock if u._rma == rma), None)

        if unit:
            inv.ship_unit(unit)
            print(f"\nUnit with RMA {rma} has been shipped!\n")

        else:
            print(f"\nUnit with RMA {rma} not found\n")



def calculate_revenue(model, warranty):
    model = model.upper()
    warranty = warranty.lower()
    if warranty == "m":
        if model in ["525DD", "525DDP", "EVERFLOW", "EVERFLOW Q"]:
            return 45.00
        elif model == "1025DD":
            return 75.00
        
    elif warranty == "f":
        if model in ["525DD", "525DDP", "EVERFLOW", "EVERFLOW Q", "P2"]:
            return 299.98
        elif model == "1025DD":
            return 375.98
        
    elif warranty == "q":
        return 0.00
    
    return 0.00
        

def save_units_to_csv(units, filename=file_path):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Concentrator_type", "Model", "RMA", "Warranty_type", "Revenue", "Flow_rate", "Repair_status", "Noise_level", "Battery_level", "Age"])
        for unit in units:
            writer.writerow([type(unit).__name__, unit._model, unit._rma, unit._warranty_type, unit._revenue, unit._flow_rate, unit._is_repaired, getattr(unit, '_noise_level', 'N/A'), getattr(unit, '_battery_level', 'N/A'), getattr(unit, '_age', 'N/A')])

            
def load_units_from_csv(filename=file_path):
    inventory = Inventory()
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader, None) 
            for row in reader:
                unit_type, model, rma, warranty, revenue, flow_rate, repaired, noise, battery, age = row
                flow_rate = flow_rate
                if unit_type == "HomeConcentrator":
                    unit = HomeConcentrator(model, rma, warranty, revenue, flow_rate, repaired, noise)
                elif unit_type == "PortableConcentrator":
                    unit = PortableConcentrator(model, rma, warranty, revenue, flow_rate, repaired, battery)
                elif unit_type == "PediatricConcentrator":
                    unit = PediatricConcentrator(model, rma, warranty, revenue, flow_rate, repaired, age)
                else:
                    continue
                inventory.receive_unit(unit)
    except FileNotFoundError:
        print("No previous inventory found.")
    return inventory



if __name__ == "__main__":
    main()
