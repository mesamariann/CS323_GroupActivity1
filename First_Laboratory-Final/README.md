# Individual Reflections: Distributed Order Processing
## Galleros
1. **How did you distribute orders among worker processes?**
> Orders were distributed evenly by the master process (rank 0) to workers
using comm.send(). Each order was assigned using
(order_index % num_workers) + 1 to cycle through available workers.

2. **What happens if there are more orders than workers?**
> Workers receive multiple orders sequentially. A worker finishes
one order and receives the next, so no order is skipped or lost.

3. **How did processing delays affect order completion?**
> Workers with shorter delays finished earlier, causing results to
arrive at master out of original order. This is visible in the
output where Order #2 was stored before Order #1.

4. **How did you implement shared memory, and where was it initialized?**
> A Python list (completed) was initialized in the master process.
Workers sent results back to master via MPI messages using tag=2,
and master appended each result to the list under a Lock().

5. **What issues occurred when multiple workers wrote to shared memory?**
> Without synchronization, concurrent writes could cause race conditions
resulting in lost entries or inconsistent ordering. This was observed
when running without Lock() where results arrived unpredictably.

6. **How did you ensure consistent results?**
> A Lock() was used as a context manager (with lock:) around each
append() call in the master process, ensuring only one result
was written at a time and producing a complete, consistent final list.

## Mesa
1. **How did you distribute orders among worker processes?**
> Orders were distributed by the master process using a round-robin or cyclical assignment strategy. By utilizing comm.send(), the master rotated through the available worker ranks, assigning tasks evenly so that the workload was shared across the entire system rather than piling up on a single worker.

2. **What happens if there are more orders than workers?**
> When the total number of orders exceeds the number of available workers, the system simply assigns multiple tasks to each worker. As soon as a worker finishes processing one order, it takes on the next assigned task in its queue, ensuring that every single order is eventually processed without any being skipped.

3. **How did processing delays affect order completion?**
> Because each order had different processing delays, workers finished their tasks at different times. Workers handling shorter tasks finished earlier than those with longer delays, which meant that the completed orders arrived back at the master process out of their original assigned sequence.

4. **How did you implement shared memory, and where was it initialized?**
> Shared memory was set up as a centralized Python list, which was initialized in the master process before any tasks were processed. As workers completed their orders, they sent the results back via messages, and the master process stored them in this central list.

5. **What issues occurred when multiple workers wrote to shared memory?**
> When multiple workers tried to send their results to the shared memory at the exact same time without any protective measures, it caused race conditions. This lack of synchronization resulted in unpredictable behavior, meaning the list could become inconsistent or entries could be lost.

6. **How did you ensure consistent results?**
> To guarantee consistent and reliable results, a Lock() mechanism was implemented in the master process. By using a lock context manager, the system ensured that only one process could append data to the shared list at any given time, completely preventing race conditions and keeping the final data intact.

## Betonio
1. **How did you distribute orders among worker processes?**
> Orders were distributed by the master process using comm.send(), where each order was assigned to a worker process based on the available ranks. The distribution used a cycle-like approach so the tasks could be shared among workers instead of being handled by only one process.

2. **What happens if there are more orders than workers?**
> If there are more orders than workers, some workers receive and process more than one order. This still works because the orders are assigned one by one until all orders are handled.

3. **How did processing delays affect order completion?**
> The processing delays made some workers finish earlier or later depending on how long their assigned task took. Because of this, the completed orders did not always appear in the same order as they were originally assigned.

4. **How did you implement shared memory, and where was it initialized?**
> Shared memory was implemented using a shared list where completed orders were stored after processing. It was initialized in the master process before collecting the results from the workers.

5. **What issues occurred when multiple workers wrote to shared memory?**
> When multiple workers wrote to shared memory at the same time, the results could become inconsistent or appear in an unpredictable order. This showed why synchronization was needed when several processes access the same data.

6. **How did you ensure consistent results?**
> Consistent results were ensured by using a Lock() so only one process could write to the shared list at a time. This helped prevent race conditions and made sure the final list of completed orders was complete and reliable.

## Galendez

## Panandigan
1. **How did you distribute orders among worker processes?**
> Task allocation was coordinated centrally, with jobs forwarded to different processing units through MPI communication calls. Instead of concentrating execution on one unit, the system rotated assignments across multiple processors to balance the workload more effectively.

2. **What happens if there are more orders than workers?**
> If the quantity of incoming orders is greater than the active processing units, each unit handles several jobs sequentially rather than only one. After completing a task, the processor immediately continues with another pending assignment, allowing all requests to be completed while preventing unprocessed entries.

3. **How did processing delays affect order completion?**
> Variations in execution time caused certain processing units to complete their workloads sooner than others. As a result, finished tasks were returned in a different sequence from the one used during the initial distribution phase.

4. **How did you implement shared memory, and where was it initialized?**
> A common data structure was established to act as shared storage for finalized tasks once processing was completed. This container was prepared by the coordinating process prior to receiving outputs from the worker nodes, allowing incoming results to be gathered in a centralized location. By maintaining a unified repository, the system could efficiently organize processed entries, simplify result tracking, and ensure that all completed operations were available for later review or reporting.

5. **What issues occurred when multiple workers wrote to shared memory?**
> When several worker processes attempted to write their outputs to the shared storage simultaneously without synchronization control, race conditions occurred. Because access to the shared resource was unmanaged, the system produced inconsistent results, which sometimes caused missing or corrupted entries in the list.

6. **How did you ensure consistent results?**
> Without synchronization mechanisms in place, concurrent result submissions from multiple worker processes created race conditions within the shared storage. As a consequence, unpredictable system behavior occurred, leading to inconsistent data and the possible loss of some recorded entries.

