class Binary_Search_Tree:

    def __init__(self, data):
        self.data = data
        self.Left_child = None
        self.Right_child = None

    def Add_Node(self, data):
        if data == self.data:
            return # node already exist

        if data < self.data:
            if self.Left_child:
                self.Left_child.Add_Node(data)
            else:
                self.Left_child = Binary_Search_Tree(data)

        else:
            if self.Right_child:
                self.Right_child.Add_Node(data)
            else:
                self.Right_child = Binary_Search_Tree(data)


    def Find_Node(self, val):

        if self.data == val:
            return self.data

        if val < self.data:
            if self.Left_child:
                return self.Left_child.Find_Node(val)
            else:
                return self.data  # return nearest distance

        if val > self.data:
            if self.Right_child:
                return self.Right_child.Find_Node(val)
            else:
                return self.data # return nearest distance
