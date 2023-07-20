class SummaryRoute():
    def __init__(self, origin, destination, avg_time, avg_dis, num_routes):
        self.origin = origin
        self.destination = destination
        self.avg_time = avg_time
        self.avg_dis = avg_dis
        self.num_routes = num_routes

    def __lt__(self, other):
        if self.avg_time != other.avg_time:
            return self.avg_time < other.avg_time
        elif self.avg_dis != other.avg_dis:
            return self.avg_dis < other.avg_dis
        else:
            return self.num_routes > other.num_routes

    def __eq__(self, other):
        return self.avg_time == other.avg_time and self.avg_dis == other.avg_dis and self.num_routes == other.num_routes

    def __repr__(self):
        return f"{self.origin} - {self.destination}:\nAverage Time: {self.avg_time} min\nAverage Distance: {self.avg_dis} km\nNumber of Routes: {self.num_routes}"
