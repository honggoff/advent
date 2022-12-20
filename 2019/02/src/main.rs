use std::io;
use std::io::Read;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let code = parse_vec(&input);
    let processed = run_with_inputs(12, 02, &code);
    println!("{}", processed);
    println!("{:?}", find_inputs_for(19690720, &code));

}

fn find_inputs_for(output: i32, program: &Vec<i32>) -> (i32, i32) {
    for noun in 0..100 {
        for verb in 0..100 {
            if run_with_inputs(noun, verb, program) == output {
                return (noun, verb)
            }
        }
    }
    panic!("inputs not found")
}

fn parse_vec(input: &str) -> Vec<i32> {
    let mut result: Vec<i32> = Vec::new();
    for line in input.split(",") {
        result.push(line.trim().parse::<i32>().unwrap());
    }
    result
}

fn run_with_inputs(noun: i32, verb: i32, program: &Vec<i32>) -> i32 {
    let mut memory = program.clone();
    memory[1] = noun;
    memory[2] = verb;
    let result = run(memory);
    result[0]
}

fn run(mut code: Vec<i32>) -> Vec<i32> {
    let mut index = 0;
    while code[index] != 99 {
        let op = code[index];
        let a1 = code[index + 1] as usize;
        let a2 = code[index + 2] as usize;
        let a3 = code[index + 3] as usize;
        match op {
            1 => { code[a3] = code[a1] + code[a2]; }
            2 => { code[a3] = code[a1] * code[a2]; }
            _ => panic!("Unknown opcode")
        }
        index += 4;
    }
    code
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_run() {
        let test_data = vec!(
            (vec![1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], vec![3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
            (vec![1,0,0,0,99], vec![2,0,0,0,99]),
            (vec![2,3,0,3,99], vec![2,3,0,6,99]),
            (vec![2,4,4,5,99,0], vec![2,4,4,5,99,9801]),
            (vec![1,1,1,4,99,5,6,0,99], vec![30,1,1,4,2,5,6,0,99]),
//            (vec![], vec![]),
        );
        for (input, output) in test_data.iter() {
            assert_eq!(*output, run(input.clone()));
        }
    }

    #[test]
    fn test_parse_vec() {
        assert_eq!(vec![1, 3, 7, 99], parse_vec("1, 3, 7, 99"))
    }
}