import math

class MaxHeap:

    def __init__(self, list=[]):
        self.heap = list
        self.heap_size = len(list)
        self.build()

    def __str__(self):
        return "{}".format(self.heap)

    def parent(self, key):
        return int(math.floor((key-1)/2))

    def left(self, key):
       return 2*key+1

    def right(self,key):
       return 2*key+2

    def heapify(self, i):
        l = self.left(i)
        r = self.right(i)
        if l<self.heap_size and self.heap[l][0]>self.heap[i][0]:
            max = l
        else:
            max = i
        if r<self.heap_size and self.heap[r][0]>self.heap[max][0]:
            max = r
        if max !=i:
            aux = self.heap[i]
            self.heap[i] = self.heap[max]
            self.heap[max] = aux
            self.heapify(max)

    def build(self):
        lastNonLeaf = int(math.floor((len(self.heap)-1)/2))
        for i in range(lastNonLeaf, -1, -1):
            self.heapify(i)

    def insert(self, priority, label):
        newNode = [0,0]
        newNode[0] = priority
        newNode[1] = label
        self.heap_size+=1
        self.heap.append(newNode)
        self.increase_priority(self.heap_size-1, priority)

    def extract_max(self):
        if self.heap_size<1:
            raise Exception("heap underflow")
        else:
            max = self.heap[0]
            self.heap[0] = self.heap[self.heap_size-1]
            self.heap_size-=1
            self.heapify(0)
            del self.heap[self.heap_size]
        return max

    def increase_priority(self, i, priority):
        if priority < self.heap[i][0]:
            raise Exception("new priority is lower than current priority")
        else:
            self.heap[i][0] = priority
            while i>0 and self.heap[self.parent(i)][0] < self.heap[i][0]:
                aux = self.heap[i]
                self.heap[i] = self.heap[self.parent(i)]
                self.heap[self.parent(i)] = aux
                i = self.parent(i)


import unittest

class TestMaxHeapMethods(unittest.TestCase):
    def test_parent(self):
        heap = MaxHeap()
        self.assertEqual(heap.parent(1), 0)
        self.assertEqual(heap.parent(2), 0)
        self.assertEqual(heap.parent(3), 1)
        self.assertEqual(heap.parent(4), 1)
        self.assertEqual(heap.parent(5), 2)
        self.assertEqual(heap.parent(6), 2)

    def test_left(self):
        heap = MaxHeap()
        self.assertEqual(heap.left(0), 1)
        self.assertEqual(heap.left(1), 3)
        self.assertEqual(heap.left(2), 5)

    def test_right(self):
        heap = MaxHeap()
        self.assertEqual(heap.right(0), 2)
        self.assertEqual(heap.right(1), 4)
        self.assertEqual(heap.right(2), 6)

    def test_heapify(self):
        heap = MaxHeap()
        heap.heap = [[1,1],[5,5],[6,6],[4,4],[3,3]]
        heap.heap_size = 5
        heap.heapify(0)
        self.assertEqual(heap.heap[0][0], 6)
        self.assertEqual(heap.heap[2][0], 1)

    def test_extract_max(self):
        heap = MaxHeap()
        heap.heap = [[1,1],[5,5],[6,6],[4,4],[3,3]]
        heap.heap_size = 5
        heap.heapify(0)
        max = heap.extract_max()
        self.assertEqual(max[0], 6)
        self.assertEqual(heap.heap[0][0], 5)
        self.assertEqual(heap.heap[1][0], 4)
        for i in range(1,5):
            heap.extract_max()
        with self.assertRaises(Exception):
            heap.extract_max()

    def test_increase_priority(self):
        heap = MaxHeap()
        heap.heap = [[1,1],[5,5],[6,6],[4,4],[3,3]]
        heap.heap_size = 5
        heap.heapify(0)
        heap.increase_priority(4,10)
        self.assertEqual(heap.heap[0][1], 3)
        self.assertEqual(heap.heap[1][0], 6)
        self.assertEqual(heap.heap[4][0], 5)

if __name__ == '__main__':
    unittest.main()