from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Task deduction functions
def compute_sss(salary):
    return salary * 0.045

def compute_philhealth(salary):
    return salary * 0.025

def compute_pagibig(salary):
    return salary * 0.02

def compute_tax(salary):
    return salary * 0.10


# PART A – TASK PARALLELISM
def task_parallelism(employee):
    name, salary = employee
    width = 44

    print("\n" + "┌" + "─" * width + "┐")
    print("│{:^{w}}│".format("PART A – TASK PARALLELISM", w=width))
    print("├" + "─" * width + "┤")
    print("│ Employee Name : {:<27}│".format(name))
    print("│ Gross Salary  : ₱ {:<25,.2f}│".format(salary))
    print("└" + "─" * width + "┘")

    with ThreadPoolExecutor(max_workers=4) as executor:
        deductions = {
            "SSS": executor.submit(compute_sss, salary),
            "PhilHealth": executor.submit(compute_philhealth, salary),
            "Pag-IBIG": executor.submit(compute_pagibig, salary),
            "Tax": executor.submit(compute_tax, salary),
        }

        total = 0
        for label, future in deductions.items():
            amount = future.result()
            total += amount
            print(f"{label:<12}: ₱{amount:,.2f}")

        print(f"{'Total Deduction':<12}: ₱{total:,.2f}")


# PART B – DATA PARALLELISM
def compute_payroll(employee):
    name, salary = employee
    total = salary * (0.045 + 0.025 + 0.02 + 0.10)
    net = salary - total
    return name, salary, total, net


def data_parallelism(employees):
    width = 44

    print("\n" + "┌" + "─" * width + "┐")
    print("│{:^{w}}│".format("PART B – DATA PARALLELISM", w=width))
    print("└" + "─" * width + "┘")

    with ProcessPoolExecutor() as executor:
        results = executor.map(compute_payroll, employees)

        for name, salary, total, net in results:
            print("\n" + "┌" + "─" * width + "┐")
            print("│ Employee Name : {:<27}│".format(name))
            print("├" + "─" * width + "┤")
            print("│ Gross Salary  : ₱{:>26,.2f}│".format(salary))
            print("│ Total Deduct. : ₱{:>26,.2f}│".format(total))
            print("│ Net Salary    : ₱{:>26,.2f}│".format(net))
            print("└" + "─" * width + "┘")


# MAIN
if __name__ == "__main__":
    employees = [
        ("Alice", 25000),
        ("Bob", 32000),
        ("Charlie", 28000),
        ("Diana", 40000),
        ("Edward", 35000)
    ]

    task_parallelism(employees[0])
    data_parallelism(employees)