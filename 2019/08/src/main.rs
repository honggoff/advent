use std::io::stdin;

type Layer = Vec<u32>;

fn main() {
    let mut input= String::new();
    stdin().read_line(&mut input).unwrap();
    let data = parse_data(&input);
    let layers = split_into_layers(data, 25 * 6);
    let index = find_layer_with_least_0(&layers);
    let number_of_1 = count_number(&layers[index], 1);
    let number_of_2 = count_number(&layers[index], 2);
    println!("{}", number_of_1 * number_of_2);
    let picture = compose_layers(&layers);
    println!("{}", format_layer(picture, 25, 6));
}

fn format_layer(layer: Layer, width: usize, height: usize) -> String {
    let mut result = String::new();
    for (i, c) in layer.iter().enumerate() {
        if i % width == 0 {
            result.push('\n');
        }
        result.push(match(c) {
            0 => ' ',
            1 => 'X',
            _ => panic!("Unknown color"),
        })
    }
    result
}

fn compose_layers(layers: &Vec<Layer>) -> Layer {
    let mut result = layers[0].clone();
    for (i, mut r) in result.iter_mut().enumerate() {
        for k in layers.iter().skip(1) {
            if *r == 2 {
                *r = k[i];
            }
            else {
                break;
            }
        }
    }
    result
}

fn find_layer_with_least_0(layers: &Vec<Layer>) -> usize {
    let mut number_of_0 = usize::max_value();
    let mut layer_index = 0;
    for (i, layer) in layers.iter().enumerate() {
        let count = count_number(layer, 0);
        if count < number_of_0 {
            number_of_0 = count;
            layer_index = i;
        }
    }
    layer_index
}

fn count_number(layer: &Layer, number: u32) -> usize {
    layer.iter().filter(|e| **e == number).count()
}

fn parse_data(data: &str) -> Vec<u32> {
    let mut result = vec![];
    for c in data.chars() {
        if c == '\n' {
            break;
        }
        result.push(c.to_digit(10).expect(&format!("Error parsing character {}", c)));
    }
    result
}

fn split_into_layers(data: Vec<u32>, layer_size: usize) -> Vec<Layer> {
    let mut result = vec![];
    let mut data = &data[..];
    while data.len() > 0 {
        let (layer, rest) = data.split_at(layer_size);
        result.push(Layer::from(layer));
        data = rest;
    }
    result
}

#[cfg(test)]
mod test {
    use crate::{split_into_layers, parse_data, find_layer_with_least_0, compose_layers};

    #[test]
    fn test_compose_layers() {
        let input = split_into_layers(parse_data("0222112222120000"), 4);
        let result = compose_layers(&input);
        assert_eq!(vec![0, 1, 1, 0], result);
    }

    #[test]
    fn test_find_layer_with_least_0() {
        let layers = vec![vec![1, 2, 3, 0, 0, 6], vec![7, 8, 9, 0, 1, 2]];
        let result = find_layer_with_least_0(&layers);
        assert_eq!(1, result);
    }

    #[test]
    fn test_parse_data() {
        let data = "123456789012";
        let result = parse_data(data);
        assert_eq!(vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2], result);
    }

    #[test]
    fn test_split_into_layers() {
        let layer_size = 2 * 3;
        let data = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2];
        let result = split_into_layers(data, layer_size);
        assert_eq!(vec![vec![1, 2, 3, 4, 5, 6], vec![7, 8, 9, 0, 1, 2]], result);
    }
}