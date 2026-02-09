import threading
import time

def process_subject(grade, subject_id, shared_results, lock):
    """
    Handles the computation for a single subject.
    """
    time.sleep(0.1)  

    with lock:  
        print(f"[Thread-{subject_id}] Subject {subject_id} processed → Grade: {grade}")
        shared_results.append(grade)


def main():
    num_subjects = int(input("Enter number of subjects: "))
    grades = []


    for i in range(num_subjects):
        grade = float(input(f"Enter grade for subject {i + 1}: "))
        grades.append(grade)

    threads = []
    results = []
    lock = threading.Lock()

    start_time = time.time()

    
    for index, grade in enumerate(grades, start=1):
        thread = threading.Thread(
            target=process_subject,
            args=(grade, index, results, lock)
        )
        threads.append(thread)
        thread.start()

    
    for thread in threads:
        thread.join()

    
    gwa = sum(results) / len(results)
    end_time = time.time()

    print("\nAll subject threads completed.")
    print(f"Final GWA: {gwa:.2f}")
    print(f"Multithreading Execution Time: {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    main()
