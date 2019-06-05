// server.js

const path = require('path');
const fs = require('fs');
const express = require('express');
const multer = require('multer');
const bodyParser = require('body-parser')
const app = express();
const router = express.Router();

const DIR = './uploads';
const TRAINING_DIR = './training';
const TESTING_DIR = './testing';
const TESTING_PDF_DIR = './testing_pdf';

const conFilePath = 'C:\\Users\\ArgusMLPOC_Admin\\Desktop\\Argus\\Final_demo\\backup\\V_16\\Middleware\\';

let storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, DIR);
    },
    filename: (req, file, cb) => {
        cb(null, file.fieldname + '-' + Date.now()  + path.extname(file.originalname));
    }
});
let storage_training = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, TRAINING_DIR);
    },
    filename: (req, file, cb) => {
        cb(null, file.fieldname + '-' + Date.now()  + path.extname(file.originalname));
    }
});
let storage_testing = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, TESTING_DIR);
    },
    filename: (req, file, cb) => {
        cb(null, file.fieldname + '-' + Date.now()  + path.extname(file.originalname));
    }
});
let storage_testing_pdf = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, TESTING_PDF_DIR);
    },
    filename: (req, file, cb) => {
        cb(null, file.fieldname + '-' + Date.now()  + path.extname(file.originalname));
    }
});
let upload = multer({ storage: storage }).single('file');
let upload_training = multer({ storage: storage_training }).single('file');
let upload_testing = multer({ storage: storage_testing }).single('file');
let upload_testing_pdf = multer({ storage: storage_testing_pdf }).single('file');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(function (req, res, next) {
    res.setHeader('Access-Control-Allow-Origin', 'http://localhost:4200');
    res.setHeader('Access-Control-Allow-Methods', 'POST');
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
    res.setHeader('Access-Control-Allow-Credentials', true);
    next();
});

app.get('/api', function (req, res) {
    res.end('file catcher example');
});

app.post('/api/upload', function (req, res) {
    upload(req, res, function (err) {
        if (err) {
            return res.status(501).json({ error: err });
        }
        res.json({ originalName: req.file.originalname, uploadName: req.file.filename });
    });
});

app.post('/api/upload/training', function (req, res) {
    upload_training(req, res, function (err) {
        if (err) {
            return res.status(501).json({ error: err });
        }
        res.json({ originalName: req.file.originalname, uploadName: req.file.filename });
    });
});

app.post('/api/upload/testing', function (req, res) {
    upload_testing(req, res, function (err) {
        if (err) {
            return res.status(501).json({ error: err });
        }
        res.json({ originalName: req.file.originalname, uploadName: req.file.filename });
    });
});

app.post('/api/upload/testing_pdf', function (req, res) {
    upload_testing_pdf(req, res, function (err) {
        if (err) {
            return res.status(501).json({ error: err });
        }
        res.json({ originalName: req.file.originalname, uploadName: req.file.filename });
    });
});

app.get('/api/upload/:filename', function (req, res) {
    var filePath = conFilePath + "uploads\\"+ req.params.filename;
    console.log(filePath);
    fs.readFile(filePath , function (err,data){
        res.contentType("application/pdf");
        console.log(data);
        res.send(data);
    });
});

app.get('/api/upload/testing_pdf/:filename', function (req, res) {
    var filePath = conFilePath + "testing_pdf\\"+ req.params.filename;
    fs.readFile(filePath , function (err,data){
        res.contentType("application/pdf");
        console.log(data);
        res.send(data);
    });
});

const PORT = process.env.PORT || 5602;

app.listen(PORT, function () {
    console.log('Node.js server is running on port ' + PORT);
});