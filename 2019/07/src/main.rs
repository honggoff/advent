use std::io::Read;
use std::sync::mpsc::{channel, Receiver, Sender};
use std::{io, thread};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let code = parse_vec(&input);
    println!("{:?}", find_maximal_signal(&code));
    println!("{:?}", find_maximal_signal_with_feedback(&code));
}

fn parse_vec(input: &str) -> Vec<i32> {
    let mut result: Vec<i32> = Vec::new();
    for line in input.split(",") {
        result.push(line.trim().parse::<i32>().unwrap());
    }
    result
}

fn permutate(input: Vec<i32>) -> Vec<Vec<i32>> {
    let mut result = Vec::new();
    if input.len() == 1 {
        result.push(input);
    } else {
        for (index, &i) in input.iter().enumerate() {
            let mut rest = input.clone();
            rest.remove(index);
            for mut part in permutate(rest) {
                part.push(i);
                result.push(part);
            }
        }
    }
    result
}

fn find_maximal_signal(code: &Vec<i32>) -> i32 {
    let mut signal = 0;
    let mut best_phases = vec![];
    for phases in permutate(vec![0, 1, 2, 3, 4]) {
        let current_signal = run_phase_combination(code, phases.as_slice());
        //println!("phase combination {:?}, signal {}", phases, current_signal);
        if current_signal > signal {
            signal = current_signal;
            best_phases = phases;
        }
    }
    println!("Best phase combination was {:?}", best_phases);
    signal
}

fn find_maximal_signal_with_feedback(code: &Vec<i32>) -> i32 {
    let mut signal = 0;
    let mut best_phases = vec![];
    for phases in permutate(vec![5, 6, 7, 8, 9]) {
        let current_signal = run_phase_combination_with_feedback(code, phases.as_slice());
        //println!("phase combination {:?}, signal {}", phases, current_signal);
        if current_signal > signal {
            signal = current_signal;
            best_phases = phases;
        }
    }
    println!("Best phase combination was {:?}", best_phases);
    signal
}

fn run_phase_combination(code: &Vec<i32>, phases: &[i32]) -> i32 {
    let mut amplitude = 0;
    for &phase in phases {
        let (input_tx, input_rx) = channel();
        let (output_tx, output_rx) = channel();
        input_tx.send(phase).unwrap();
        input_tx.send(amplitude).unwrap();
        let name = format!("Phase {}", phase);
        let mut computer = Computer::from(code.clone(), input_rx, output_tx, name);
        computer.run();
        amplitude = output_rx.recv().unwrap();
    }
    //println!("phase combination {:?}, signal {}", phases, amplitude);
    amplitude
}

fn run_phase_combination_with_feedback(code: &Vec<i32>, phases: &[i32]) -> i32 {
    let mut senders = vec![];
    let mut receivers = vec![];
    for &phase in phases.iter().rev() {
        let (sender, receiver) = channel();
        sender.send(phase).unwrap();
        senders.push(sender);
        receivers.push(receiver);
    }

    // assign output of last to input of first
    let last = senders.pop().unwrap();
    last.send(0).unwrap();
    senders.insert(0, last);

    let (result_sender, result_receiver) = channel();

    let mut threads = vec![];
    for (i, phase) in phases.iter().enumerate() {
        let input_rx = receivers.pop().unwrap();
        let output_tx = senders.pop().unwrap();
        let name = format!("Amplifier {}, phase {}", i, phase);
        let mut computer = Computer::from(code.clone(), input_rx, output_tx, name);
        let this_result_sender = result_sender.clone();
        threads.push(thread::spawn(move || {
            computer.run();
            if i == 0 {
                let result = computer.inputs.recv().unwrap();
                println!("Result: {}", result);
                this_result_sender.send(result).unwrap();
            }
        }));
    }

    threads.pop().unwrap().join().unwrap();
    //    for thread in threads {
    //        thread.join().unwrap();
    //    }
    //println!("phase combination {:?}, signal {}", phases, amplitude);
    let amplitude = result_receiver.recv().unwrap();
    amplitude
}

struct Computer {
    memory: Vec<i32>,
    inputs: Receiver<i32>,
    outputs: Sender<i32>,
    name: String,
}

impl Computer {
    fn from(
        memory: Vec<i32>,
        inputs: Receiver<i32>,
        outputs: Sender<i32>,
        name: String,
    ) -> Computer {
        Computer {
            memory,
            inputs,
            outputs,
            name,
        }
    }

    fn get(&self, arg: i32, mode: i32) -> i32 {
        match mode {
            0 => self.memory[arg as usize],
            1 => arg,
            _ => panic!("Unknown address mode"),
        }
    }

    fn set(&mut self, arg: i32, mode: i32, value: i32) {
        assert_eq!(0, mode, "Illegal address mode");
        self.memory[arg as usize] = value;
    }

    fn arithmetic(&mut self, opcode: i32, mode: i32, arguments: &Vec<i32>) {
        let a1 = self.get(arguments[0], mode % 10);
        let mode = mode / 10;
        let a2 = self.get(arguments[1], mode % 10);
        let mode = mode / 10;
        let result = match opcode {
            1 => a1 + a2,
            2 => a1 * a2,
            _ => panic!("Unknown opcode {}", opcode),
        };
        self.set(arguments[2], mode % 10, result);
    }

    fn compare(&mut self, opcode: i32, mode: i32, arguments: &Vec<i32>) {
        let a1 = self.get(arguments[0], mode % 10);
        let mode = mode / 10;
        let a2 = self.get(arguments[1], mode % 10);
        let mode = mode / 10;
        let result = match opcode {
            7 => a1 < a2,
            8 => a1 == a2,
            _ => panic!("Unknown opcode {}", opcode),
        };
        let value = match result {
            true => 1,
            false => 0,
        };

        self.set(arguments[2], mode % 10, value);
    }

    fn get_arguments(&self, index: &mut usize, count: usize) -> Vec<i32> {
        let mut arguments = Vec::new();
        for _ in 0..count {
            arguments.push(self.memory[*index]);
            *index += 1;
        }
        arguments
    }

    fn input(&mut self, mode: i32, argument: i32) {
        let i = self.inputs.recv().expect("Missing input");
        self.set(argument, mode, i);
    }

    fn output(&mut self, mode: i32, argument: i32) {
        let value = self.get(argument, mode);
        println!("{} writing {} to output", self.name, value);
        self.outputs
            .send(value)
            .expect(&format!("Output failed in {}", self.name));
    }

    fn jump_cond(&self, opcode: i32, mode: i32, arguments: &Vec<i32>) -> Option<i32> {
        let a1 = self.get(arguments[0], mode % 10);
        let mode = mode / 10;
        let a2 = self.get(arguments[1], mode % 10);
        let condition = match opcode {
            5 => a1 != 0,
            6 => a1 == 0,
            _ => panic!("Unknown opcode {}", opcode),
        };
        if condition {
            Some(a2)
        } else {
            None
        }
    }

    fn run(&mut self) {
        let mut index = 0;
        loop {
            let instruction = self.memory[index];
            let opcode = instruction % 100;
            let mode = instruction / 100;
            //println!("instruction {} at index {}", instruction, index);
            index += 1;
            match opcode {
                1 | 2 => {
                    let arguments = self.get_arguments(&mut index, 3);
                    self.arithmetic(opcode, mode, &arguments)
                }
                3 => {
                    let arguments = self.get_arguments(&mut index, 1);
                    self.input(mode, arguments[0]);
                }
                4 => {
                    let arguments = self.get_arguments(&mut index, 1);
                    self.output(mode, arguments[0]);
                }
                5 | 6 => {
                    let arguments = self.get_arguments(&mut index, 2);
                    if let Some(addres) = self.jump_cond(opcode, mode, &arguments) {
                        index = addres as usize;
                    }
                }
                7 | 8 => {
                    let arguments = self.get_arguments(&mut index, 3);
                    self.compare(opcode, mode, &arguments)
                }
                99 => break,
                _ => panic!("Unknown opcode {} at index {}", opcode, index - 1),
            }
        }
        println!("{} is done", self.name);
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_permutate() {
        assert_eq!(
            vec![
                vec![3, 2, 1],
                vec![2, 3, 1],
                vec![3, 1, 2],
                vec![1, 3, 2],
                vec![2, 1, 3],
                vec![1, 2, 3]
            ],
            permutate(vec![1, 2, 3])
        )
    }

    #[test]
    fn test_find_maximal_signal() {
        let test_data = vec![
            (
                vec![
                    3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0,
                ],
                43210,
            ),
            (
                vec![
                    3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23,
                    23, 4, 23, 99, 0, 0,
                ],
                54321,
            ),
            (
                vec![
                    3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7,
                    33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0,
                ],
                65210,
            ),
        ];
        for (code, signal) in test_data {
            assert_eq!(signal, find_maximal_signal(&code));
        }
    }

    #[test]
    fn test_run_phase_combination() {
        let code = vec![
            3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0,
        ];
        let phases = [4, 3, 2, 1, 0];
        let amplitude = run_phase_combination(&code, &phases);
        assert_eq!(43210, amplitude);
    }

    #[test]
    fn test_run() {
        let test_data = vec![
            (
                vec![1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
                vec![3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
            ),
            (vec![1, 0, 0, 0, 99], vec![2, 0, 0, 0, 99]),
            (vec![2, 3, 0, 3, 99], vec![2, 3, 0, 6, 99]),
            (vec![2, 4, 4, 5, 99, 0], vec![2, 4, 4, 5, 99, 9801]),
            (
                vec![1, 1, 1, 4, 99, 5, 6, 0, 99],
                vec![30, 1, 1, 4, 2, 5, 6, 0, 99],
            ),
            (vec![1002, 4, 3, 4, 33], vec![1002, 4, 3, 4, 99]),
            //            (vec![], vec![]),
        ];
        for (input, output) in test_data.iter() {
            let (_, input_rx) = channel();
            let (output_tx, _) = channel();

            let mut computer =
                Computer::from(input.clone(), input_rx, output_tx, String::from("test"));
            computer.run();
            assert_eq!(*output, computer.memory);
        }
    }

    #[test]
    fn test_parse_vec() {
        assert_eq!(vec![1, 3, 7, 99], parse_vec("1, 3, 7, 99"))
    }
}
