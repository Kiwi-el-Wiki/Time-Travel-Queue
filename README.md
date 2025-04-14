# Time travel, Advanced Data Structure

The Time Travel problem in the context of data structures refers to the ability to modify and query the state of a data structure at different points in time, both in the past and in the present. This problem is addressed by retroactive data structures, which allow operations to be performed that affect not only the current state of the structure, but also its history of operations.

### Persistence
A persistent data structure maintains previous versions of itself after updates, enabling queries on any historical state without affecting the current one. This is typically achieved through techniques such as path copying or structural sharing, where only the modified portions of the structure are duplicated while unmodified parts are reused.

Persistence looks like:

![Persistence.](https://github.com/elpolloconmayo/Time-Travel-Queue/blob/main/images/persistent.png)

### Retroactivity

A retroactive data structure extends the concept of persistence by allowing insertion, deletion, or modification of operations at any point in the timeline, not just at the end. When a past operation is changed, the data structure recalculates the current state as if the new operation had always existed, propagating the effects forward through time, there are two types of retroactivity:

-**Partially retroactive**: allows modification of past operations, but only current queries are supported.

-**Fully retroactive**: allows both modification and querying at any point in time.

Retroactive data is a little more complex to show in a figure, better see videos in "Current Implementation"

## Current implementation (WIP)

In this implementation, we merge the implementation of Erik Demaine at https://youtu.be/WqCWghETNDc?si=tRViaFba89L1pA3o and the implementation shown by Mitko Nikov at https://youtu.be/m2yRawZGYXk?feature=shared .

**Disclaimer**: this was made purely to have fun and isn't complete.

In file **retroactive_queue.py** there's a class "Queue" that is a Fully retroactive data structure that supports the following operations:
- Insert an element at a given time. (push)
- Delete an element at a given time. (pop)
- Get the queue at given time. (front)
- Get the size at given time (size)
- Undo a operation at a given time if it is possible. (undo) **WIP, testing**
- Print all data inorder (print_in_order)

To make this possible, we use a OST as a base to work, in this case the OST is an augmented RB Tree located in **base_rbt_ost.py** which later is augmented again according to different cases in **modified_ost.py**, but this can work with any tree as long as its got same functions, the three different cases of use are:
- "Add" Tree: this OST only contains the operation of adding an element at a given index, *stores index and value*.
- "deleting" Tree: this OST only contains the operation of deleting an element at a given index, only *stores the index* as it exists.
- "consistency" Tree: this OST contains all the operations of adding and deleting elements, and is used to check and validate consistency of the structure over time, *stores index and prefix* (+1 for adding and -1 for deleting)

There's also another implementation of the retroactive queue which is based on the same principle, but also uses a linked list in it's nodes, so we use it for the inorder traversal, we can compare how much we gain from using it in benchmarks.

### Overview:

![implementation.](https://github.com/elpolloconmayo/Time-Travel-Queue/blob/main/images/curr_implementation.png)

## Benchmarks and how to replicate

Benchmarks are made in **benchmark.ipynb** (obviously), for this file to work all you need is have the files of base_rbt_ost.py, modified_ost.py and retroactive_queue.py in same folder as benchmark, the benchmark starts by creating a random data according to the biggest batch we want to test, and just for fun we order it in another list to compare how much affects data order, then by using perf_counter we measure how much time it takes push and pop functions individually to work. It's **relevant** to mention that _the first node is fixed_ at "datetime(2010, 1, 1, 12, 0, 0)" which is in the center of the range of the random data.

![push.](https://github.com/elpolloconmayo/Time-Travel-Queue/blob/main/images/push.png)

![pop.](https://github.com/elpolloconmayo/Time-Travel-Queue/blob/main/images/pop.png)

Implementation was made thinking it would be log in all cases, but benchmarks show log or linear for push and maybe linear-logarithmic for pop, which isn't bad for a retroactive data structure but there's pretty much room for improvement.

Pop gets greatly benefited with ordered data (probably has something to do with the inorder traversal search), push suffers when data is ordered.

As for undo and front functions, there's no benchmark right now.

## Future Work

- to check consistency we make a fully traversal of the tree, **_this CAN'T be optimized by storing the size of the tree in each node_** as the check should be _inorder_, due to this, a better approach could be to implement a 4th structure that only point's to bridges (like a simple list that stores indexes), or maybe another structure for the consistency tree, like a skiplist would work.
- **fix the undo operation** (in tested enviroment looks fine, with random values there's some bug that I couldn't find)
- benchmark in a better way pop, front and undo operations
- better OST implementation, this one isn't bad, but could be better, AA tree could be a good choice.

## some scribble notes

before coding, I made a notebook to try to understand the problem, here it is if it may help understanding

![implementation.](https://github.com/elpolloconmayo/Time-Travel-Queue/blob/main/images/notes.png)
