use std::io;
use std::io::Read;

fn module_fuel(weight: u32) -> u32 {
    let fraction = weight / 3;
    if fraction > 2 {
        fraction - 2
    }
    else {
        0
    }
}

fn sum_fuel_from_string(input: &str) -> u32 {
    let mut sum = 0;
    for line in input.split_whitespace() {
        sum += module_fuel(line.parse::<u32>().unwrap());
    }
    sum
}

fn sum_recursive_fuel_from_string(input: &str) -> u32 {
    let mut sum = 0;
    for line in input.split_whitespace() {
        let fuel = module_fuel(line.parse::<u32>().unwrap());
        sum += sum_recursively(fuel);
    }
    sum
}

fn sum_recursively(mut weight: u32) -> u32 {
    let mut total_weight = 0;
    while weight > 0 {
        total_weight += weight;
        weight = module_fuel(weight);
    }
    total_weight
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let fuel = sum_fuel_from_string(&input);
    println!("{}", fuel);
    let fuel = sum_recursive_fuel_from_string(&input);
    println!("{}", fuel);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sum_recursively() {
        let inputs = [
            (2, 2),
            (2, 2),
            (654, 966),
            (33583, 50346),
        ];
        for (weight, fuel) in inputs.iter() {
            assert_eq!(*fuel, sum_recursively(*weight));
        }
    }

    #[test]
    fn test_sum_string() {
        let input = "12 14\n1969 100756";
        let output = 2 + 2 + 654 + 33583;
        assert_eq!(output, sum_fuel_from_string(input));
    }

    #[test]
    fn test_module_mass() {
        let inputs = [
            (12, 2),
            (14, 2),
            (1969, 654),
            (100756, 33583),
        ];
        for (weight, fuel) in inputs.iter() {
            assert_eq!(*fuel, module_fuel(*weight))
        }
    }
}