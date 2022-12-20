/*
fn has_two_consecutive(bytes: &[u8]) -> bool {
    false
}

fn does_not_decrease(bytes: &[u8]) -> bool {
    false
}
*/

fn passes1(i: u32) -> bool {
    let s = i.to_string();
    let bytes = s.as_bytes();
    let mut monotonic = true;
    let mut cons = false;

    let mut last = bytes[0];
    for &b in bytes[1..].iter() {
        if b == last {
            cons = true;
        }
        if b < last {
            monotonic = false;
            break;
        }
        last = b;
    }
    cons && monotonic
}

fn passes2(i: u32) -> bool {
    let s = i.to_string();
    let bytes = s.as_bytes();
    let mut monotonic = true;
    let mut cons = false;
    let mut stride = 1;

    let mut last = bytes[0];
    for &b in bytes[1..].iter() {
        if b == last {
            stride += 1;
        }
        else {
            if stride == 2 {
                cons = true;
            }
            stride = 1
        }
        if b < last {
            monotonic = false;
            break;
        }
        last = b;
    }
    if stride == 2 {
        cons = true;
    }
    cons && monotonic
}

fn main() {
    let mut count1 = 0;
    let mut count2 = 0;
    for i in 108457..562041 {
        if passes1(i) {
            count1 += 1;
        }
        if passes2(i) {
            count2 += 1;
        }
    }
    println!("{}", count1);
    println!("{}", count2);
}
