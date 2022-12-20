use std::collections::HashMap;
use std::io;

type OrbitMap = HashMap<String, Vec<String>>;

fn parse_line(input: &str) -> (String, String) {
    let mut s = input.trim().split(')');
    let center = s.next().expect(&format!("Cannot parse {}", input));
    let orbiter = s.next().expect(&format!("Cannot parse {}", input));
    (center.to_string(), orbiter.to_string())
}

fn parse_input() -> OrbitMap
{
    let mut result = HashMap::new();
    loop {
        let mut line = String::new();
        match io::stdin().read_line(&mut line) {
            Ok(_) if line.len() > 0 => {
                let (center, orbiter) = parse_line(&line);
                let center = result.entry(center).or_insert(Vec::new());
                center.push(orbiter);
            },
            _ => break,
        }
    }
    result
}

fn calculate_orbits_for(body: &str, level: u32, map: &OrbitMap) -> u32 {
    // println!("Visiting {}", body);
    let mut sum = level;
    for orbiter in map.get(body).unwrap_or(&vec!()) {
        sum += calculate_orbits_for(orbiter, level + 1, map);
    }
    sum
}

fn calculate_orbits(map: &OrbitMap) -> u32
{
    calculate_orbits_for("COM", 0, map)
}

fn orbital_distance(from: &str, to: &str, map: &OrbitMap) -> u32 {
    for orbiter in map.get(from).unwrap_or(&vec!()) {
        if orbiter == to {
            return 1;
        }
        let dist = orbital_distance(orbiter, to, map);
        if dist > 0 {
            return dist + 1;
        }
    }
    0
}

fn minimal_transfers(body: &str, map: &OrbitMap) -> u32 {
    for orbiter in map.get(body).unwrap_or(&vec!()) {
        let t = minimal_transfers(orbiter, map);
        if t > 0 {
            return t;
        }
    }
    let you = orbital_distance(body, "YOU", map);
    let santa = orbital_distance(body, "SAN", map);
    if you > 0 && santa > 0 {
        return you + santa - 2;
    }
    0
}

fn main() {
    let input = parse_input();
    // println!("{:?}", input);
    println!("Number of orbits: {}", calculate_orbits(&input));
    println!("Minimal number of transfers: {}", minimal_transfers("COM", &input));
}
