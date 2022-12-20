use std::collections::HashMap;
use std::io;
use std::io::Read;

type Map = HashMap<(i32, i32), u32>;

fn get_direction(m: &str) -> (i32, i32) {
    match &m[0..1] {
        "U" => (0, 1),
        "D" => (0, -1),
        "L" => (-1, 0),
        "R" => (1, 0),
        _ => panic!("Unknown direction")
    }
}

fn get_distance(m: &str) -> u32 {
    m[1..].parse().unwrap()
}

trait Addable {
    fn add(&mut self, other: &Self);
    fn norm(&self) -> u32;
}

impl Addable for (i32, i32) {
    fn add(&mut self, other: &(i32, i32)) {
        self.0 += other.0;
        self.1 += other.1;
    }

    fn norm(&self) -> u32 {
        (self.0.abs() + self.1.abs()) as u32
    }
}

fn traverse_path(path: &str, mut f: impl FnMut((i32, i32))) {
    let mut pos = (0, 0);
    for m in path.split(",") {
        let direction = get_direction(&m);
        let distance = get_distance(&m);
        for _ in 0..distance {
            pos.add(&direction);
            f(pos);
        }
    }
}

fn mark_path(path: &str) -> Map {
    let mut map = Map::new();
    let mut step = 1;
    traverse_path(path, |pos| {
        map.insert(pos, step);
        step += 1;
    });
    map
}

fn find_closest_intersection_with_map(path: &str, map: Map) -> u32
{
    let mut dist = u32::max_value();
    traverse_path(path, |pos| {
        if map.contains_key(&pos) && pos.norm() < dist {
            dist = pos.norm();
        }
    });
    dist
}

fn find_fastest_intersection_with_map(path: &str, map: Map) -> u32
{
    let mut dist = u32::max_value();
    let mut step: u32 = 1;
    traverse_path(path, |pos| {
        if let Some(&step_other) = map.get(&pos) {
            let s = step + step_other;
            if s < dist {
                dist = s;
            }
        }
        step += 1;
    });
    dist
}

fn find_closest_intersection(paths: &str) -> u32
{
    let mut paths = paths.split('\n');
    let map = mark_path(paths.next().unwrap());
    find_closest_intersection_with_map(paths.next().unwrap(), map)
}

fn find_fastest_intersection(paths: &str) -> u32
{
    let mut paths = paths.split('\n');
    let map = mark_path(paths.next().unwrap());
    find_fastest_intersection_with_map(paths.next().unwrap(), map)
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    println!("{}", find_closest_intersection(&input));
    println!("{}", find_fastest_intersection(&input));
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_add() {
        let mut a = (33, 2);
        a.add(&(1, 3));
        assert_eq!((34, 5), a);
        let mut a = (3, 2);
        a.add(&(5, 3));
        assert_eq!((8, 5), a);
    }

    #[test]
    fn test_get_distance() {
        assert_eq!(23, get_distance("L23"));
        assert_eq!(11, get_distance("R11"));
        assert_eq!(3, get_distance("U3"));
        assert_eq!(999, get_distance("D999"));
    }

    #[test]
    fn test_get_direction() {
        assert_eq!((0, 1), get_direction("U12"));
        assert_eq!((0, 1), get_direction("U1"));
        assert_eq!((0, -1), get_direction("D9"));
        assert_eq!((1, 0), get_direction("R1"));
        assert_eq!((-1, 0), get_direction("L1"));
    }

    #[test]
    fn test_mark_path() {
        let map = mark_path("R8,U5,L5,D3");
        assert_eq!(map.get(&(1, 0)), Some(&1));
        assert_eq!(map.get(&(8, 2)), Some(&10));
        assert!(map.contains_key(&(5, 0)));
        assert!(map.contains_key(&(8, 2)));
        assert!(map.contains_key(&(3, 2)));
    }

    #[test]
    fn test_find_closest_intersection() {
        assert_eq!(159, find_closest_intersection("R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83"));
        assert_eq!(135, find_closest_intersection("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7"));
    }

    #[test]
    fn test_find_fastest_intersection() {
        assert_eq!(610, find_fastest_intersection("R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83"));
        assert_eq!(410, find_fastest_intersection("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7"));
    }
}