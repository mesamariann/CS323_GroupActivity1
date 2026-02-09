import threading
import time


# =======================
# HEADER DESIGN
# =======================
print("-" * 40)
print("+    GWA Calculator (Multithreading)   +")
print("-" * 40 + "\n\n")

def process_subject(grade, subject_id, shared_results, lock):
    """
    Handles the computation for a single subject.
    """
    time.sleep(0.1)  # Simulate processing time

    with lock:
        print(f"| [Thread-{subject_id}] Subject {subject_id:<2} → Grade: {grade:<5} |")
        shared_results.append(grade)


def main():
    # =======================
    # INPUT SECTION
    # =======================
    print("-" * 40)
    print("+           INPUT SECTION             +")
    print("-" * 40)

    num_subjects = int(input("Enter number of subjects: "))
    grades = []

    for i in range(num_subjects):
        grade = float(input(f"Enter grade for subject {i + 1}: "))
        grades.append(grade)

    # =======================
    # THREADING SETUP
    # =======================
    threads = []
    results = []
    lock = threading.Lock()

    start_time = time.time()

    print("\n\n" + "-" * 40)
    print("+         PROCESSING SUBJECTS         +")
    print("-" * 40)

    for index, grade in enumerate(grades, start=1):
        thread = threading.Thread(
            target=process_subject,
            args=(grade, index, results, lock)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # =======================
    # RESULTS SECTION
    # =======================
    gwa = sum(results) / len(results)
    end_time = time.time()

    print("\n\n" + "-" * 40)
    print("+              RESULTS                +")
    print("-" * 40)
    print(f"|  Final GWA             : {gwa:.2f}        |")
    print(f"|  Execution Time (secs) : {end_time - start_time:.4f}      |" + "\n")
    print("-" * 40)
    print("+   All subject threads completed!    +")
    print("-" * 40)


if __name__ == "__main__":
    main()
