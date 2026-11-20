//! Tests of chapter 8: units, vectors, and the exercises' solutions.
#[path = "../../../exercises/fraction.rs"]
pub mod fraction;
#[path = "../../../exercises/largest.rs"]
pub mod largest;
#[path = "../../../exercises/matrix.rs"]
pub mod matrix;
#[path = "../../../exercises/shapes.rs"]
pub mod shapes;
#[path = "../../../exercises/typestate.rs"]
pub mod typestate;
#[allow(dead_code)]
#[path = "../../../listings/units.rs"]
pub mod units;
#[allow(dead_code)]
#[path = "../../../listings/vector2.rs"]
pub mod vector2;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn units_arithmetic() {
        use units::*;
        let v = (Metres(400.0) + Metres(1250.0)) / (Seconds(310.0) + Seconds(845.0));
        assert!((v.0 - 1650.0 / 1155.0).abs() < 1e-12);
        assert_eq!(v.to_string(), "1.43 m/s");
        assert_eq!(MetresPerSecond(2.0) * Seconds(3.0), Metres(6.0));
        assert_eq!(std::mem::size_of::<Metres>(), std::mem::size_of::<f64>()); // a newtype costs nothing
    }

    #[test]
    fn vector_operators() {
        use vector2::V2;
        let (a, b) = (V2 { x: 1.0, y: 2.0 }, V2 { x: -3.0, y: 0.5 });
        assert_eq!(a + b - b, a);
        assert_eq!(-(a * 2.0), V2 { x: -2.0, y: -4.0 });
        assert_eq!(a + V2::default(), a);
    }

    #[test]
    fn fraction_lowest_terms() {
        use fraction::Fraction;
        let f = |n, d| Fraction::new(n, d).unwrap().to_string();
        assert_eq!(f(6, 8), "3/4");
        assert_eq!(f(6, -8), "-3/4");
        assert_eq!(f(-6, -8), "3/4");
        assert_eq!(f(10, 5), "2");
        assert_eq!(f(0, 7), "0");
        assert_eq!(Fraction::new(1, 0), None);
        assert_eq!(format!("[{:>5}]", Fraction::new(1, 2).unwrap()), "[  1/2]");
        assert_eq!(Fraction::new(2, 4), Fraction::new(-1, -2)); // equal values, equal representations
    }

    #[test]
    fn largest_generic() {
        assert_eq!(largest::largest(&[65, 133, 98]), Some(133));
        assert_eq!(largest::largest(&[-0.1, -2.5]), Some(-0.1));
        assert_eq!(largest::largest::<char>(&[]), None);
        assert_eq!(largest::largest_ref(&["Mill".to_string(), "Quay".to_string()]).unwrap(), "Quay");
        assert_eq!(largest::largest(&[1.0, f64::NAN, 3.0]), Some(3.0)); // NaN is never greater
        assert!(largest::largest(&[f64::NAN, 3.0]).unwrap().is_nan()); // but a first NaN stays
    }

    #[test]
    fn shapes_collection() {
        use shapes::*;
        let mut v: Vec<Box<dyn Shape>> = vec![Box::new(Rect(4.0, 5.0)), Box::new(Circle(1.5)), Box::new(Triangle(3.0, 4.0, 5.0))];
        assert_eq!(by_area(&mut v), vec!["rect 4x5", "circle r=1.5", "triangle 3-4-5"]);
        assert!((v[2].area() - 6.0).abs() < 1e-12);
        assert_eq!(v[2].perimeter(), 12.0);
    }

    #[test]
    fn matrices() {
        use matrix::Matrix;
        let fib = Matrix { n: 2, a: vec![1i64, 1, 1, 0] };
        assert_eq!(fib.pow(10).a[1], 55);
        assert_eq!(fib.pow(0), Matrix::identity(2));
        let m = Matrix { n: 2, a: vec![0.5, 0.5, 0.0, 1.0] };
        assert_eq!(m.pow(2).a, vec![0.25, 0.75, 0.0, 1.0]);
        // a path 0 -> 1 -> 2 in a three-node graph: reachable in exactly two steps
        let g = Matrix { n: 3, a: [0, 1, 0, 0, 0, 1, 0, 0, 0].map(|b| matrix::Reach(b == 1)).to_vec() };
        assert!(g.pow(2).a[2].0);
        assert!(!g.pow(3).a.iter().any(|r| r.0));
    }

    #[test]
    fn typestate_connection() {
        let mut c = typestate::Connection::new().open();
        c.send("HELLO");
        c.send("BYE");
        let closed = c.close();
        assert_eq!(closed.sent, vec!["HELLO", "BYE"]);
        assert_eq!(std::mem::size_of::<typestate::Connection<typestate::Open>>(), std::mem::size_of::<Vec<String>>());
    }
}
