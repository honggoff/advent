use std::io;
use std::io::Read;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let code = parse_vec(&input);
    let _processed = run(code);
    //println!("{}", processed);
}

fn parse_vec(input: &str) -> Vec<i32> {
    let mut result: Vec<i32> = Vec::new();
    for line in input.split(",") {
        result.push(line.trim().parse::<i32>().unwrap());
    }
    result
}

fn get(arg: i32, mode: i32, memory: &Vec<i32>) -> i32 {
    match mode {
        0 => memory[arg as usize],
        1 => arg,
        _ => panic!("Unknown address mode"),
    }
}

fn set(arg: i32, mode: i32, memory: &mut Vec<i32>, value: i32) {
    assert_eq!(0, mode, "Illegal address mode");
    memory[arg as usize] = value;
}

fn arithmetic(opcode: i32, mode: i32, arguments: &Vec<i32>, memory: &mut Vec<i32>) {
    let a1 = get(arguments[0], mode %10, &memory);
    let mode = mode / 10;
    let a2 = get(arguments[1], mode %10, &memory);
    let mode = mode / 10;
    let result = match opcode {
        1 => a1 + a2,
        2 => a1 * a2,
        _ => panic!("Unknown opcode {}", opcode)
    };
    set(arguments[2], mode %10, memory, result);
}

fn compare(opcode: i32, mode: i32, arguments: &Vec<i32>, memory: &mut Vec<i32>) {
    let a1 = get(arguments[0], mode %10, &memory);
    let mode = mode / 10;
    let a2 = get(arguments[1], mode %10, &memory);
    let mode = mode / 10;
    let result = match opcode {
        7 => a1 < a2,
        8 => a1 == a2,
        _ => panic!("Unknown opcode {}", opcode)
    };
    let value = match result {
        true => 1,
        false => 0
    };

    set(arguments[2], mode %10, memory, value);
}

fn get_arguments(memory: &Vec<i32>, index: &mut usize, count: usize) -> Vec<i32> {
    let mut arguments = Vec::new();
    for _ in 0..count {
        arguments.push(memory[*index]);
        *index += 1;
    }
    arguments
}

fn input(mode: i32, argument: i32, memory: &mut Vec<i32>) {
    let i = 5;
    set(argument, mode, memory, i);
}

fn output(mode: i32, argument: i32, memory: &Vec<i32>) {
    println!("{}", get(argument, mode, memory));
}

fn jump_cond(opcode: i32, mode: i32, arguments: &Vec<i32>, memory: &Vec<i32>) -> Option<i32> {
    let a1 = get(arguments[0], mode %10, &memory);
    let mode = mode / 10;
    let a2 = get(arguments[1], mode %10, &memory);
    let condition = match opcode {
        5 => a1 != 0,
        6 => a1 == 0,
        _ => panic!("Unknown opcode {}", opcode)
    };
    if condition {
        Some(a2)
    }
    else {
        None
    }
}

fn run(mut memory: Vec<i32>) -> Vec<i32> {
    let mut index = 0;
    loop {
        let instruction = memory[index];
        let opcode = instruction % 100;
        let mode = instruction / 100;
        //println!("instruction {} at index {}", instruction, index);
        index += 1;
        match opcode {
            1 | 2 => {
                let arguments = get_arguments(&memory, &mut index, 3);
                arithmetic(opcode, mode, &arguments, &mut memory)
            },
            3 => {
                let arguments = get_arguments(&memory, &mut index, 1);
                input(mode, arguments[0], &mut memory);
            },
            4 => {
                let arguments = get_arguments(&memory, &mut index, 1);
                output(mode, arguments[0], &memory);
            },
            5 | 6 => {
                let arguments = get_arguments(&memory, &mut index, 2);
                if let Some(addres) = jump_cond(opcode, mode, &arguments, &memory) {
                    index = addres as usize;
                }
            },
            7 | 8 => {
                let arguments = get_arguments(&memory, &mut index, 3);
                compare(opcode, mode, &arguments, &mut memory)
            },
            99 => break,
            _ => panic!("Unknown opcode {} at index {}", opcode, index - 1),
        }
    }
    memory
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
            (vec![1002,4,3,4,33], vec![1002,4,3,4,99]),
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