# https://github.com/MuhibAhmed/DSA_MULTOPS
class Record:
    def __init__(self):
        self.from_rate = 0 # rate of packets sent from victims' machine
        self.to_rate = 0  # rate of packets sent to victims' machine
        self.child = None

    def update_rate(self,fwd,from_rate=1,to_rate=1):
        # if the given address is forward (i.e. defined in our router's routes)
        # update to_rate else update from_rate
        beta = 0.75 # calculated with 4 max childs in mind
        if fwd:
            self.to_rate = beta*self.to_rate + (1-beta)*to_rate
        else:
            self.from_rate = beta*self.from_rate + (1-beta)*from_rate


class Table:
    def __init__(self,parent = None) -> None:
        # a pointer pointing to the parent table
        self.parent = parent
        # records with 256 objects of Record
        self.records = [Record() for i in range(256)] # 0-255


# [192.168.1.1]
class Multops:
    def __init__(self):
        self.root = Table()
        self.threshold = 200 # using this threshold for max_ratio and min_ratio both
        self.childs_list = list() # with this new feature we don't have to use a doubly linked list with every node

    def ratio_blocker(self):
        """Go to every record's leaf node and check if its parents ratio of 
        to_rate and from_rate is less than the min_ratio then drop that packet"""
        for each in self.childs_list:
            # check if the parents of all childs has a ratio less than the threshold
            if each.parent and (each.parent.to_rate < self.threshold and each.parent.to_rate < self.threshold):
                # drop that packet
                each.parent.child = None
                each.parent = None

    def update(self,addr,packet,fwd):
        """Create new subnet of address and if address already exist, 
        update its rates """
        # separating address by .
        addr = addr.split('.')
        # choosing root table for first iteration
        t = self.root
        # temp variable to store the No. of iterations or "No. of childs"
        temp = int()
        # defining r outside so that it can be used outside for loop
        r = None
        # iterate max 4 times 
        # because there are 4 bytes and therefore the max height of the tree must be 4
        for i in range(4):
            r = t.records[int(addr[i])] #goto corresponding record. for ex, if addr is 192.168.1.1 then at first iteration go to the 192th record then on next iteration goto 168th record and so on
            # calculate EWMA of rates and update
            # if it's not the root table
            r.update_rate(fwd,packet.from_rate,packet.to_rate)
            # if there is no children of this record then break else re-iterate on its children
            if not r.child:
                break
            t = r.child
            temp = i + 1

        # if to_rate or from_rate is greater than threshold and r is not the leaf node
        if (r.from_rate > self.threshold or r.to_rate > self.threshold) and temp != 4:
            # create a table under the record r and set its parent to be r
            r.child = Table(r)
            # Storing newly created child to a list so that we don't have to iterate
            # through 256 records and their 256*256 childs
            self.childs_list.append(r.child)

            


class Packet:
    def __init__(self,from_rate,to_rate) -> None:
        self.from_rate = from_rate
        self.to_rate = to_rate


# obj_packet = Packet(from_rate=300,to_rate=400)

# x = Multops()
# x.update('192.168.1.4',obj_packet,True)
# x.ratio_blocker()
# x.update('192.168.1.4',obj_packet,True)
# x.update('192.168.1.4',obj_packet,True)
# x.update('192.168.1.4',obj_packet,True)
# x.update('192.168.1.4',obj_packet,True)
# x.ratio_blocker()
