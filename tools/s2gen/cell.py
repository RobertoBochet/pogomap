from typing import List, Tuple

import geojson as gj
import s2sphere as s2


class S2Cluster:
    def __init__(self, cluster: s2.CellId, target_level: int):
        self.cluster = cluster
        self.cluster_level = cluster.level()
        self.target_level = target_level

        self._compute()

    def _compute(self):
        self._x = []
        self._y = []

        x_c = (self.cluster, self.cluster)
        y_c = (self.cluster, self.cluster)

        for i in range(self.target_level - self.cluster_level):
            x_c = (x_c[0].child(0), x_c[1].child(1))
            y_c = (y_c[0].child(0), y_c[1].child(3))

        self._x.append((S2Cluster._get_degrees_vertex(x_c[0])[0], S2Cluster._get_degrees_vertex(x_c[1])[3]))
        self._y.append((S2Cluster._get_degrees_vertex(y_c[0])[0], S2Cluster._get_degrees_vertex(y_c[1])[1]))

        for i in range(2 ** (self.target_level - self.cluster_level)):
            self._x.append((S2Cluster._get_degrees_vertex(x_c[0])[1], S2Cluster._get_degrees_vertex(x_c[1])[2]))
            self._y.append((S2Cluster._get_degrees_vertex(y_c[0])[3], S2Cluster._get_degrees_vertex(y_c[1])[2]))

            x_c = (x_c[0].get_edge_neighbors()[1], x_c[1].get_edge_neighbors()[1])
            y_c = (y_c[0].get_edge_neighbors()[2], y_c[1].get_edge_neighbors()[2])

    def toFeatures(self) -> List[gj.Feature]:
        return [
            gj.Feature(geometry=gj.MultiLineString(self._x)),
            gj.Feature(geometry=gj.MultiLineString(self._y))
        ]

    def toGeoJSON(self) -> str:
        features = gj.FeatureCollection(self.toFeatures())

        return gj.dumps(features)

    def __hash__(self) -> int:
        return int("".join([
            "9" if self.target_level < 10 else "",
            str(self.target_level),
            "010",
            str(self.cluster.id())
        ]))

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)

    @staticmethod
    def _get_degrees_vertex(cell: s2.CellId) -> List[Tuple[int, int]]:
        a = []
        for i in range(4):
            v = s2.Cell(cell).get_vertex_raw(i)
            s = s2.LatLng.from_point(v)
            a.append((s.lng().degrees, s.lat().degrees))
        return a

    @staticmethod
    def _get_degrees_quadrilateral(cell: s2.CellId) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        a = S2Cluster._get_degrees_vertex(cell)
        return [(a[0], a[1]), (a[1], a[2]), (a[2], a[3]), (a[3], a[0])]


if __name__ == "__main__":
    c = s2.CellId.from_lat_lng(s2.LatLng.from_degrees(0, 0))

    sc = S2Cluster(c.parent(10), 17)
    print(hash(S2Cluster(c.parent(10), 17)))
    print(hash(S2Cluster(c.parent(10), 12)))

    with open('s.geojson', 'w') as f:
        gj.dump(gj.FeatureCollection(sc.toFeatures()), f)
    pass
