import numpy as np
from collections import deque
import pyautogui

class Test_Unittest:
    def test_array_syntax(self):
        a = np.array([1, 2, 3, 4])
        
        assert (a[0] < a[1] < a[2] < a[3]) == True
    
    def check_deque(self, sequence_deque, start_point):
        # Iterate through the deque starting at the given point
        for i in range(start_point, len(sequence_deque)):
            if sequence_deque[i] == [0, 0]:
                # If we encounter a [0, 0] element, count it
                count = 1
                # Check subsequent elements until we encounter a non-zero element or reach the end of the deque
                for j in range(i+1, len(sequence_deque)):
                    if sequence_deque[j] == [0, 0]:
                        count += 1
                    else:
                        break
                # If we counted 5 [0, 0] elements, return True
                if count == 5:
                    return True
        # If we looped through the entire deque without finding 5 [0, 0] elements, return False
        return False

    def test_deque_syntax(self):
        my_deque = deque([[405, 260], [418, 262], [427, 261], [436, 260], [438, 261], [444, 259], [447, 257], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]], maxlen=16)

        assert self.check_deque(my_deque, 14) == True

    def test_pyautogui(self):
        w, h = pyautogui.size()
        w1, h1 = pyautogui.position()
        
        assert (w, h, w1, h1) == (10, 10, 10, 10)

    def test_int(self):
        w0, w1 = 2, 10
        
        assert w0 / w1 == 0.1

    def test_dict(self):
        a = {}
        
        assert len(a) == 0