import math

class Node:
    def __init__(self, point, station_id, left=None, right=None):
        self.point = point
        self.id = station_id
        self.left = left
        self.right = right

class KDTree:
    def __init__(self, points_with_ids):
        self.k = 2
        self.root = self.build_kd_tree(points_with_ids)

    def build_kd_tree(self, points_with_ids, depth=0):
        if not points_with_ids:
            return None

        axis = depth % 2
        points_with_ids.sort(key=lambda x: x[0][axis])
        
        median = len(points_with_ids) // 2
        median_point, station_id = points_with_ids[median]

        return Node(
            point=median_point,
            station_id=station_id,
            left=self.build_kd_tree(points_with_ids[:median], depth + 1),
            right=self.build_kd_tree(points_with_ids[median + 1:], depth + 1)
        )
    
    def insert(self, point, station_id, depth=0):
        self.root = self._insert(self.root, point, station_id, depth)

    def _insert(self, node, point, station_id, depth):
        if node is None:
            return Node(point, station_id)

        axis = depth % self.k
        if point[axis] < node.point[axis]:
            node.left = self._insert(node.left, point, station_id, depth + 1)
        else:
            node.right = self._insert(node.right, point, station_id, depth + 1)

        return node

    def nearest_neighbor(self, node, target, target_id, depth=0, best=None):
        if node is None:
            return best

        axis = depth % self.k

        if node.id != target_id:
            current_distance = self.distance(node.point, target)
            if best is None or current_distance < self.distance(best.point, target):
                best = node

        if target[axis] < node.point[axis]:
            best = self.nearest_neighbor(node.left, target, target_id, depth + 1, best)
            if (float(target[axis]) + self.distance(best.point, target) >= float(node.point[axis])):
                best = self.nearest_neighbor(node.right, target, target_id, depth + 1, best)
        else:
            best = self.nearest_neighbor(node.right, target, target_id, depth + 1, best)
            if (float(target[axis]) - self.distance(best.point, target) <= float(node.point[axis])):
                best = self.nearest_neighbor(node.left, target, target_id, depth + 1, best)

        return best

    @staticmethod
    def distance(point1, point2):
        return math.sqrt((float(point1[0]) - float(point2[0])) ** 2 + (float(point1[1]) - float(point2[1])) ** 2)
