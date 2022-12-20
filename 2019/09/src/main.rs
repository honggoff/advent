use std::io::Read;
use std::sync::mpsc::{channel, Receiver, Sender};
use std::{io, thread};

type Word = i128;
type Memory = Vec<Word>;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let code = parse_vec(&input);

    run_with_input(code.clone(), 1);
    run_with_input(code.clone(), 2);
}

fn run_with_input(code: Memory, input: Word) -> () {
    let (input_tx, input_rx) = channel();
    let (output_tx, output_rx) = channel();
    let mut computer =
        Computer::from(code, input_rx, output_tx, String::from("test"));
    input_tx.send(input);
    computer.run();
    loop {
        if let Ok(o) = output_rx.try_recv() {
            println!("{}", o);
        } else {
            break;
        }
    }
}

fn parse_vec(input: &str) -> Memory {
    let mut result = Vec::new();
    for line in input.split(",") {
        result.push(line.trim().parse::<Word>().unwrap());
    }
    result
}

struct Computer {
    memory: Memory,
    relative_base: Word,
    inputs: Receiver<Word>,
    outputs: Sender<Word>,
    name: String,
}

impl Computer {
    fn from(
        memory: Memory,
        inputs: Receiver<Word>,
        outputs: Sender<Word>,
        name: String,
    ) -> Computer {
        Computer {
            memory,
            relative_base: 0,
            inputs,
            outputs,
            name,
        }
    }

    fn get(&mut self, arg: Word, mode: Word) -> Word {
        match mode {
            0 | 2 => {
                let offset = if mode == 0 { 0 } else { self.relative_base };
                let index = (arg + offset) as usize;
                if index >= self.memory.len() {
                    self.memory.resize(index + 1, 0);
                }
                self.memory[index]
            }
            1 => arg,
            _ => panic!("Unknown address mode"),
        }
    }

    fn set(&mut self, arg: Word, mode: Word, value: Word) {
        let offset = match mode {
            0 => 0,
            1 => panic!("Illegal address mode for set"),
            2 => self.relative_base,
            _ => panic!("Unknown address mode"),
        };

        let index = (arg + offset) as usize;
        if index >= self.memory.len() {
            self.memory.resize(index + 1, 0);
        }
        self.memory[index] = value;
    }

    fn arithmetic(&mut self, opcode: Word, mode: Word, arguments: &Vec<Word>) {
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

    fn compare(&mut self, opcode: Word, mode: Word, arguments: &Vec<Word>) {
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

    fn get_arguments(&self, index: &mut usize, count: usize) -> Vec<Word> {
        let mut arguments = Vec::new();
        for _ in 0..count {
            arguments.push(self.memory[*index]);
            *index += 1;
        }
        arguments
    }

    fn input(&mut self, mode: Word, argument: Word) {
        let i = self.inputs.recv().expect("Missing input");
        self.set(argument, mode, i);
    }

    fn output(&mut self, mode: Word, argument: Word) {
        let value = self.get(argument, mode);
        // println!("{} writing {} to output", self.name, value);
        self.outputs
            .send(value)
            .expect(&format!("Output failed in {}", self.name));
    }

    fn jump_cond(&mut self, opcode: Word, mode: Word, arguments: &Vec<Word>) -> Option<Word> {
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

    fn adjust_relative_base(&mut self, mode: Word, argument: Word) {
        self.relative_base += self.get(argument, mode);
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
                9 => {
                    let arguments = self.get_arguments(&mut index, 1);
                    self.adjust_relative_base(mode, arguments[0]);
                }
                99 => break,
                _ => panic!("Unknown opcode {} at index {}", opcode, index - 1),
            }
        }
        // println!("{} is done", self.name);
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_run_output() {
        let test_data = vec![
            (vec![104, 1125899906842624, 99], vec![1125899906842624]),
            (
                vec![1102, 34915192, 34915192, 7, 4, 7, 99, 0],
                vec![1219070632396864],
            ),
            (
                vec![
                    109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99,
                ],
                vec![
                    109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99,
                ],
            ),
            //(vec![], vec![]),
        ];
        for (input, outputs) in test_data.iter() {
            let (_, input_rx) = channel();
            let (output_tx, output_rx) = channel();

            let mut computer =
                Computer::from(input.clone(), input_rx, output_tx, String::from("test"));
            computer.run();
            for output in outputs {
                assert_eq!(*output, output_rx.recv().unwrap());
            }
        }
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
        assert_eq!(vec![1, 3, 7, 99], parse_vec("1, 3, 7, 99"));
        assert_eq!(
            vec![104, 1125899906842624, 99],
            parse_vec("104,1125899906842624,99")
        );
    }
}
