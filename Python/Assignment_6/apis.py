
class myAPI:
    def swapFirstAndLast(self, the_list):
        '''
        Takes a Python list as parameter and modifies the list parameter by swapping its first and last elements.
         Does not return anything.
        :return: none
        '''
        the_list[0], the_list[-1] = the_list[-1], the_list[0]

        print(the_list)  # just to test it

    def shiftRight(self,the_list):
        '''
        Takes a Python list as parameter and modifies the list parameter by shifting all elements in the list to the
        right and putting the last (rightmost) element in the zeroth position of the list.
        Does not return anything.
        :return: none
        '''
        the_list.insert(0, the_list.pop())
        print(the_list)  # just to test it

    def double(self,the_list):
        '''
        Takes a Python list as parameter and modifies the list parameter by doubling the value of each element in the list.
         Does not return anything.
        :return:
        '''

        [x * 2 for x in the_list]
        print([x * 2 for x in the_list])  # just to test it

    def isSorted(self, the_list):
        '''
        Takes a Python list as parameter and returns True if the list parameter is in sorted order,
        returns False otherwise.
        You can assume that the list parameter has only numbers in it.
        :return:
        '''

        return all(the_list[i] <= the_list[i + 1] for i in range(len(the_list) - 1))
        #
        # if sorted(the_list) == the_list:
        #     return True
        # else:
        #     return False

    def replaceEvens(self, the_list):
        """
        Takes a Python list as parameter and replaces any even elements of the list parameter with a zero.
        This looks at the value of the element to see if it is even, the index of the element does NOT determine
        if the element is replaced with a 0 in the list. Does not return anything.
        :return:
        """
        print([x if x % 2 != 0 else 0 for x in the_list])  # just to test it

    def permuteList(self, the_list):
        import random
        """
        Takes a python list as a parameter and returns a random permutation of that list.
        You can use the algorithm in:
        Knuth random permutation algorithm (Links to an external site.)Links to an external site.
        :return:
        """
        from random import randint

        n = len(the_list)

        for i in range(n - 1):
            j = randint(0, (n - i) - 1)
            the_list[i], the_list[i + j] = the_list[i + j], the_list[i]
        return the_list
        # return random.sample(the_list, min(len(the_list), 8))

my_api = myAPI()

# my_api.swapFirstAndLast([1,2,3])
# my_api.shiftRight([1,2,3])
# my_api.double([1, 2, 3])
# print (my_api.isSorted([1, 1, 2, 3]))
# my_api.replaceEvens([5, 1, 2, 3, 4, 6, 8, 5])
# for p in my_api.permuteList([2,3,4]):
#     print(p)

print(my_api.permuteList([2, 3, 4, 7, 90]))
