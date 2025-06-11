#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <unicodeobject.h>
#include <ctype.h>

#ifndef PyUnicodeWriter
#define PyUnicodeWriter _PyUnicodeWriter
#define PyUnicodeWriter_Init _PyUnicodeWriter_Init
#define PyUnicodeWriter_Dealloc _PyUnicodeWriter_Dealloc
#define PyUnicodeWriter_Finish _PyUnicodeWriter_Finish
#define PyUnicodeWriter_WriteASCIIString _PyUnicodeWriter_WriteASCIIString
#endif

static int write_ascii(PyUnicodeWriter *w, const char *s, Py_ssize_t n) { return PyUnicodeWriter_WriteASCIIString(w, s, n); }

static int dump_string(PyUnicodeWriter *w, PyObject *v) {
    Py_ssize_t n;
    const char *s = PyUnicode_AsUTF8AndSize(v, &n);
    if (!s) return -1;
    if (write_ascii(w, "\"", 1) < 0) return -1;
    if (write_ascii(w, s, n) < 0) return -1;
    return write_ascii(w, "\"", 1);
}

static int dump_long(PyUnicodeWriter *w, PyObject *v) {
    char buf[64];
    long long val = PyLong_AsLongLong(v);
    if (PyErr_Occurred()) return -1;
    int len = snprintf(buf, sizeof buf, "%lld", val);
    return write_ascii(w, buf, len);
}

static int dump_value(PyUnicodeWriter *w, PyObject *v);

static int dump_dict(PyUnicodeWriter *w, PyObject *d) {
    if (write_ascii(w, "{", 1) < 0) return -1;
    Py_ssize_t pos = 0;
    PyObject *key, *value;
    int first = 1;
    while (PyDict_Next(d, &pos, &key, &value)) {
        if (!PyUnicode_CheckExact(key)) {
            PyErr_SetString(PyExc_TypeError, "Keys must be str");
            return -1;
        }
        if (!first) {
            if (write_ascii(w, ",", 1) < 0) return -1;
        }
        first = 0;
        if (dump_string(w, key) < 0) return -1;
        if (write_ascii(w, ":", 1) < 0) return -1;
        if (dump_value(w, value) < 0) return -1;
    }
    return write_ascii(w, "}", 1);
}

static int dump_value(PyUnicodeWriter *w, PyObject *v) {
    if (PyLong_CheckExact(v)) return dump_long(w, v);
    if (PyUnicode_CheckExact(v)) return dump_string(w, v);
    if (PyDict_CheckExact(v)) return dump_dict(w, v);
    PyErr_SetString(PyExc_TypeError, "Unsupported value type");
    return -1;
}

static PyObject *cj_dumps(PyObject *self, PyObject *args) {
    PyObject *obj;
    if (!PyArg_ParseTuple(args, "O", &obj)) return NULL;
    if (!PyDict_Check(obj)) {
        PyErr_SetString(PyExc_TypeError, "Expected dict");
        return NULL;
    }
    PyUnicodeWriter w;
    PyUnicodeWriter_Init(&w);
    w.min_length = 64;
    w.overallocate = 1;
    if (dump_dict(&w, obj) < 0) {
        PyUnicodeWriter_Dealloc(&w);
        return NULL;
    }
    return PyUnicodeWriter_Finish(&w);
}

static const char *skip_ws(const char *p, const char *end) {
    while (p < end && isspace((unsigned char)*p)) ++p;
    return p;
}

static PyObject *parse_string(const char **pp, const char *end) {
    const char *p = *pp;
    if (*p != '"') {
        PyErr_SetString(PyExc_ValueError, "Expected \" at string start");
        return NULL;
    }
    ++p;
    const char *start = p;
    while (p < end && *p != '"') ++p;
    if (p >= end) {
        PyErr_SetString(PyExc_ValueError, "Unterminated string");
        return NULL;
    }
    PyObject *s = PyUnicode_DecodeUTF8(start, p - start, NULL);
    if (!s) return NULL;
    *pp = p + 1;
    return s;
}

static PyObject *parse_number(const char **pp, const char *end) {
    const char *p = *pp;
    char *q;
    double val = strtod(p, &q);
    if (p == q) {
        PyErr_SetString(PyExc_ValueError, "Invalid number");
        return NULL;
    }
    PyObject *res;
    if ((double)(long long)val == val) res = PyLong_FromLongLong((long long)val);
    else res = PyFloat_FromDouble(val);
    *pp = q;
    return res;
}

static PyObject *parse_value(const char **pp, const char *end);

static PyObject *parse_object(const char **pp, const char *end) {
    const char *p = *pp;
    if (*p != '{') {
        PyErr_SetString(PyExc_ValueError, "Expected '{'");
        return NULL;
    }
    ++p;
    PyObject *d = PyDict_New();
    if (!d) return NULL;
    p = skip_ws(p, end);
    if (p < end && *p == '}') { *pp = p + 1; return d; }
    while (p < end) {
        PyObject *key = parse_string(&p, end);
        if (!key) { Py_DECREF(d); return NULL; }
        p = skip_ws(p, end);
        if (p >= end || *p != ':') { Py_DECREF(key); Py_DECREF(d); PyErr_SetString(PyExc_ValueError, "Expected ':'"); return NULL; }
        ++p;
        p = skip_ws(p, end);
        PyObject *val = parse_value(&p, end);
        if (!val) { Py_DECREF(key); Py_DECREF(d); return NULL; }
        if (PyDict_SetItem(d, key, val) < 0) { Py_DECREF(key); Py_DECREF(val); Py_DECREF(d); return NULL; }
        Py_DECREF(key);
        Py_DECREF(val);
        p = skip_ws(p, end);
        if (p < end && *p == ',') { ++p; p = skip_ws(p, end); continue; }
        if (p < end && *p == '}') { ++p; *pp = p; return d; }
        Py_DECREF(d); PyErr_SetString(PyExc_ValueError, "Expected ',' or '}'"); return NULL;
    }
    Py_DECREF(d); PyErr_SetString(PyExc_ValueError, "Unterminated object"); return NULL;
}

static PyObject *parse_value(const char **pp, const char *end) {
    const char *p = skip_ws(*pp, end);
    if (p >= end) { PyErr_SetString(PyExc_ValueError, "Unexpected end"); return NULL; }
    if (*p == '{') return parse_object(pp, end);
    if (*p == '"') return parse_string(pp, end);
    return parse_number(pp, end);
}

static PyObject *cj_loads(PyObject *self, PyObject *args) {
    const char *s; Py_ssize_t n;
    if (!PyArg_ParseTuple(args, "s#", &s, &n)) return NULL;
    const char *p = s, *end = s + n;
    p = skip_ws(p, end);
    if (p >= end || *p != '{') { PyErr_SetString(PyExc_TypeError, "Expected object or value"); return NULL; }
    PyObject *obj = parse_object(&p, end);
    if (!obj) return NULL;
    p = skip_ws(p, end);
    if (p != end) { Py_DECREF(obj); PyErr_SetString(PyExc_ValueError, "Extra data"); return NULL; }
    return obj;
}

static PyMethodDef CustomJsonMethods[] = {
    {"loads", cj_loads, METH_VARARGS, NULL},
    {"dumps", cj_dumps, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef customjsonmodule = {
    PyModuleDef_HEAD_INIT,
    "custom_json",
    NULL,
    -1,
    CustomJsonMethods
};

PyMODINIT_FUNC PyInit_custom_json(void) { return PyModule_Create(&customjsonmodule); }