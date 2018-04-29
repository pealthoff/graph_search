import math

class MinHeap:

    def __init__(self, list=[]):
        self.heap = list
        self.heap_size = len(list)
        self.build()

    def print_heap(self):
        i=0
        while i< self.heap_size:
            j = min(self.left(i), self.heap_size)
            while i<j:
                print(self.heap[i], end = '  ')
                i+=1
            print("\n")
        return ""

    def parent(self, key):
        return int(math.floor((key-1)/2))

    def left(self, key):
       return 2*key+1

    def right(self,key):
       return 2*key+2

    def heapify(self, i):
        l = self.left(i)
        r = self.right(i)
        if l<self.heap_size and self.heap[l][0]<self.heap[i][0]:
            min = l
        else:
            min = i
        if r<self.heap_size and self.heap[r][0]<self.heap[min][0]:
            min = r
        if min !=i:
            aux = self.heap[i]
            self.heap[i] = self.heap[min]
            self.heap[min] = aux
            self.heapify(min)

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
        self.decrease_priority(self.heap_size-1, priority)

    def extract_min(self):
        if self.heap_size<1:
            raise Exception("heap underflow")
        else:
            min = self.heap[0]
            self.heap[0] = self.heap[self.heap_size-1]
            self.heap_size-=1
            self.heapify(0)
            del self.heap[self.heap_size]
        return min

    def decrease_priority(self, i, priority):
        if priority > self.heap[i][0]:
            raise Exception("new priority is higher than current priority")
        else:
            self.heap[i][0] = priority
            while i>0 and self.heap[self.parent(i)][0] > self.heap[i][0]:
                aux = self.heap[i]
                self.heap[i] = self.heap[self.parent(i)]
                self.heap[self.parent(i)] = aux
                i = self.parent(i)

    def extract_max(self):
        if self.heap_size<1:
            raise Exception("heap underflow")
        else:
            max = int(math.floor(self.heap_size/2))
            for i in range(int(math.floor(self.heap_size/2))+1, self.heap_size-1):
                if self.heap[i] > self.heap[max]:
                    max = i
            maxEl = self.heap[max]
            if max == self.heap_size-1:
                del self.heap[self.heap_size-1]
                self.heap_size-=1
            else:
                self.heap[max] = self.heap[self.heap_size-1]
                del self.heap[self.heap_size-1]
                self.heap_size-=1
                self.heapify(max)
        return (max, maxEl)


import unittest

class TestMinHeapMethods(unittest.TestCase):
    def test_parent(self):
        heap = MinHeap()
        self.assertEqual(heap.parent(1), 0)
        self.assertEqual(heap.parent(2), 0)
        self.assertEqual(heap.parent(3), 1)
        self.assertEqual(heap.parent(4), 1)
        self.assertEqual(heap.parent(5), 2)
        self.assertEqual(heap.parent(6), 2)

    def test_left(self):
        heap = MinHeap()
        self.assertEqual(heap.left(0), 1)
        self.assertEqual(heap.left(1), 3)
        self.assertEqual(heap.left(2), 5)

    def test_right(self):
        heap = MinHeap()
        self.assertEqual(heap.right(0), 2)
        self.assertEqual(heap.right(1), 4)
        self.assertEqual(heap.right(2), 6)

    def test_heapify(self):
        heap = MinHeap()
        heap.heap = [[6,6],[2,2],[4,4],[3,3],[5,5]]
        heap.heap_size = 5
        heap.heapify(0)
        self.assertEqual(heap.heap[0][0], 2)
        self.assertEqual(heap.heap[1][0], 3)
        self.assertEqual(heap.heap[3][0], 6)

    def test_extract_min(self):
        heap = MinHeap()
        heap.heap = [[6,6],[2,2],[4,4],[3,3],[5,5]]
        heap.heap_size = 5
        heap.heapify(0)
        min = heap.extract_min()
        self.assertEqual(min[0], 2)
        self.assertEqual(heap.heap[0][0], 3)
        self.assertEqual(heap.heap[1][0], 5)
        for i in range(1,5):
            heap.extract_min()
        with self.assertRaises(Exception):
            heap.extract_min()

    def test_decrease_priority(self):
        heap = MinHeap()
        heap.heap = [[6,6],[2,2],[4,4],[3,3],[5,5]]
        heap.heap_size = 5
        heap.heapify(0)
        heap.decrease_priority(4,0)
        self.assertEqual(heap.heap[0][1], 5)
        self.assertEqual(heap.heap[1][0], 2)
        self.assertEqual(heap.heap[4][0], 3)

    def test_extract_max(self):
        heap = MinHeap()
        heap.heap = [[6,6],[2,2],[4,4],[3,3],[5,5]]
        heap.heap_size = 5
        heap.heapify(0)
        max = heap.extract_max()
        self.assertEqual(max[1][0], 6)
        self.assertEqual(heap.heap[0][0], 2)
        self.assertEqual(heap.heap[3][0], 5)
        for i in range(1,5):
            heap.extract_max()
        with self.assertRaises(Exception):
            heap.extract_max()


if __name__ == '__main__':
    unittest.main()