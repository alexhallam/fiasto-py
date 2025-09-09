use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use serde_json::Value;

/// Parse a Wilkinson's formula string and return structured JSON metadata as a Python dictionary
#[pyfunction]
fn parse_formula(formula: &str) -> PyResult<PyObject> {
    Python::with_gil(|py| {
        match fiasto::parse_formula(formula) {
            Ok(json_value) => {
                // Convert serde_json::Value to Python object
                let py_dict = json_value_to_python(py, &json_value)?;
                Ok(py_dict.into())
            }
            Err(e) => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                "Formula parsing error: {}",
                e
            ))),
        }
    })
}

/// Tokenize a formula string and return JSON describing each token as a Python dictionary
#[pyfunction]
fn lex_formula(formula: &str) -> PyResult<PyObject> {
    Python::with_gil(|py| {
        match fiasto::lex_formula(formula) {
            Ok(json_value) => {
                // Convert serde_json::Value to Python object
                let py_dict = json_value_to_python(py, &json_value)?;
                Ok(py_dict.into())
            }
            Err(e) => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                "Formula lexing error: {}",
                e
            ))),
        }
    })
}

/// Convert a serde_json::Value to a Python object
fn json_value_to_python(py: Python, value: &Value) -> PyResult<PyObject> {
    match value {
        Value::Null => Ok(py.None()),
        Value::Bool(b) => Ok(b.into_py(py)),
        Value::Number(n) => {
            if let Some(i) = n.as_i64() {
                Ok(i.into_py(py))
            } else if let Some(f) = n.as_f64() {
                Ok(f.into_py(py))
            } else {
                Ok(n.to_string().into_py(py))
            }
        }
        Value::String(s) => Ok(s.into_py(py)),
        Value::Array(arr) => {
            let py_list = PyList::empty_bound(py);
            for item in arr {
                let py_item = json_value_to_python(py, item)?;
                py_list.append(py_item)?;
            }
            Ok(py_list.into())
        }
        Value::Object(obj) => {
            let py_dict = PyDict::new_bound(py);
            for (key, value) in obj {
                let py_value = json_value_to_python(py, value)?;
                py_dict.set_item(key, py_value)?;
            }
            Ok(py_dict.into())
        }
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn fiasto_py(_py: Python, m: &Bound<PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_formula, m)?)?;
    m.add_function(wrap_pyfunction!(lex_formula, m)?)?;
    Ok(())
}
