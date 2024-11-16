# network_manager.py

class managerwater:
    def __init__(self):
        self.network = {}

    def add_connection(self, start, end, cost):
        if start not in self.network:
            self.network[start] = {}
        self.network[start][end] = cost
        
        if end not in self.network:
            self.network[end] = {}
        self.network[end][start] = cost  # Assuming bidirectional connection

    def remove_connection(self, start, end):
        if start in self.network and end in self.network[start]:
            del self.network[start][end]
        if end in self.network and start in self.network[end]:
            del self.network[end][start]

    def update_connection(self, start, end, new_cost):
        if start in self.network and end in self.network[start]:
            self.network[start][end] = new_cost
            self.network[end][start] = new_cost
