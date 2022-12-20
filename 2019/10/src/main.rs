use cgmath::Vector2;
use std::io;
use std::io::Read;
use std::collections::HashMap;

type Direction = Vector2<i32>;

fn aligned(left: &Direction, right: &Direction) -> bool
{
    left * right.x == right * left.x && left.x * right.x >= 0 && left.y * right.y >= 0
}

fn number_visible(from: &Direction, to: &Vec<Direction>) -> usize {
    let mut found = vec![];
    for target in to {
        if *target != *from {
            let direction = target - *from;
            if ! found.iter().any( |f | aligned(f, &direction)) {
                found.push(direction);
            }
            else {
            }
        }
    }
    found.len()
}

fn most_visible(to: &Vec<Direction>) -> usize {
    to.iter().map(|f| number_visible(f, to)).max().unwrap()
}

fn find_nth_vaporized(map: &Vec<Direction>, &from: &Direction, n: usize) -> Direction {
    let mut sorted : HashMap<Direction, Vec<Direction>> = HashMap::new();
    for &target in map {
        if target != from {
            let direction = target - from;
            let aligned = sorted.keys().find(|&f | aligned(f, &direction)).cloned();
            match aligned {
                Some(same) => sorted.get_mut(&same).unwrap().push(direction),
                None => {sorted.insert(direction, vec![direction]);},
            }
        }
    }
    Vector2::new(0, 0).angle()
}

fn parse_map(input: &str) -> Vec<Direction> {
    let mut result = Vec::new();
    for (y, line) in input.split("\n").enumerate() {
        for (x, pos) in line.chars().enumerate() {
            if pos == '#' {
                result.push(Vector2::new(x as i32, y as i32));
            }
        }
    }
    result
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let map = parse_map(&input);

    println!("{}", most_visible(&map));
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_aligned() {
        let data = vec![
            (Vector2::new(2, 6), Vector2::new(3, 9), true),
            (Vector2::new(-2, -6), Vector2::new(3, 9), false),
            (Vector2::new(0, -6), Vector2::new(3, 0), false),
            (Vector2::new(0, 2), Vector2::new(0, 3), true),
        ];
        for (v1, v2, e) in data {
            assert_eq!(aligned(&v1, &v2), e, "left: {:?}, right: {:?}", v1, v2);
        }
    }

    #[test]
    fn test_number_visible_simple() {
        let map = vec![
            Vector2::new(1, 0),
            Vector2::new(2, 0),
            Vector2::new(3, 0),
        ];
        assert_eq!(number_visible(&Vector2::new(1, 0), &map), 1);
        assert_eq!(number_visible(&Vector2::new(2, 0), &map), 2);
    }

    #[test]
    fn test_number_visible() {
        let map = vec![
            Vector2::new(1, 0),
            Vector2::new(4, 0),
            Vector2::new(0, 2),
            Vector2::new(1, 2),
            Vector2::new(2, 2),
            Vector2::new(3, 2),
            Vector2::new(4, 2),
            Vector2::new(4, 3),
            Vector2::new(3, 4),
            Vector2::new(4, 4),
        ];
        assert_eq!(number_visible(&Vector2::new(3, 4), &map), 8);
        assert_eq!(number_visible(&Vector2::new(1, 0), &map), 7);
    }

    #[test]
    fn test_most_visible() {
        let map = vec![
            Vector2::new(1, 0),
            Vector2::new(4, 0),
            Vector2::new(0, 2),
            Vector2::new(1, 2),
            Vector2::new(2, 2),
            Vector2::new(3, 2),
            Vector2::new(4, 2),
            Vector2::new(4, 3),
            Vector2::new(3, 4),
            Vector2::new(4, 4),
        ];
        assert_eq!(most_visible(&map), 8);
    }

    #[test]
    fn test_parse_map() {

        let map = vec![
            Vector2::new(1 as i32, 0 as i32),
            Vector2::new(4, 0),
            Vector2::new(0, 2),
            Vector2::new(1, 2),
            Vector2::new(2, 2),
            Vector2::new(3, 2),
            Vector2::new(4, 2),
            Vector2::new(4, 3),
            Vector2::new(3, 4),
            Vector2::new(4, 4),
        ];
        let input =
".#..#
.....
#####
....#
...##";
        assert_eq!(parse_map(input), map);
    }
}