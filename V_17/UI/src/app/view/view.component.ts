import { Component, OnInit, EventEmitter } from "@angular/core";
import { Router } from "@angular/router";
import { HttpClient } from "@angular/common/http";
import { ArgusService } from '../service/argus.service';
import { MatDialog } from '@angular/material'
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { FileSelectDirective, FileUploader } from 'ng2-file-upload';
import { BASEURL } from '../constants/app.constants';
const uri = BASEURL;

@Component({
  selector: "app-view",
  templateUrl: "./view.component.html",
  styleUrls: ["./view.component.scss"]
})

export class ViewComponent implements OnInit {
  showProgress: boolean;
  fileList_one: string;
  fileList_two: string;
  filesList: string;
  isTestingFileUploaded: boolean;
  isTrainingFileUploaded: boolean;
  linientArray: any[] = [];
  mediumArray: any[] = [];
  strictArray: any[] = [];

  uploader_training: FileUploader = new FileUploader({ url: `${uri}/training` });
  uploader_testing: FileUploader = new FileUploader({ url: `${uri}/testing` });
  uploader_testing_pdf: FileUploader = new FileUploader({ url: `${uri}/testing_pdf` });

  trainingArray: any[] = [];
  testingArray: any[] = [];
  testingPdfArray: any[] = [];

  attachmentList: any[] = [];

  selected_training: string;
  selected_testing: string;
  selected_testing_pdf: string;

  trainingArray_local: any[] = [];
  testingArray_local: any[] = [];
  testingPdfArray_local: any[] = [];

  isPdfSelected = false;

  constructor(public dialog: MatDialog, private route: Router, private http: HttpClient,
    private argusService: ArgusService) {
    this.uploader_training.onCompleteItem = (item: any, response: any, status: any, headers: any) => {
      this.trainingArray.push(JSON.parse(response));
      localStorage.setItem('training', JSON.stringify(this.trainingArray));
    }
    this.uploader_testing.onCompleteItem = (item: any, response: any, status: any, headers: any) => {
      this.testingArray.push(JSON.parse(response));
      localStorage.setItem('testing', JSON.stringify(this.testingArray));
    }
    this.uploader_testing_pdf.onCompleteItem = (item: any, response: any, status: any, headers: any) => {
      this.testingPdfArray.push(JSON.parse(response));
      localStorage.setItem('testingPdf', JSON.stringify(this.testingPdfArray));
    }
    this.loadData();
  }

  ngOnInit() {
    this.isTestingFileUploaded = false;
    this.isTrainingFileUploaded = false;
  }

  loadData() {
    this.trainingArray_local = JSON.parse(localStorage.getItem('training'));
    this.testingArray_local = JSON.parse(localStorage.getItem('testing'));
    this.testingPdfArray_local = JSON.parse(localStorage.getItem('testingPdf'));
  }
  selectTraining() {
    this.isTestingFileUploaded = true;
  }
  selectTesting() {
    this.isTrainingFileUploaded = true;
  }
  selectTestingPdf() {
    localStorage.setItem('output_pdf', '');
    setTimeout(() => {
      console.log(this.testingPdfArray[0]);
      localStorage.setItem('output_pdf', this.testingPdfArray[0]['uploadName']);
    },2000)
    this.isPdfSelected = true;
  }
  callModel(trainingFileName, testingFileName) {
    let obj = { 'trainingDocument': trainingFileName, 'testingDocument': testingFileName };
    this.http.post("http://127.0.0.1:6000/predict", obj).subscribe((data) => {
      if (data) {
        if (data['training_count'] === 0) {
          this.openDialog({ 'errorTitle': 'Error', 'errorMessage': 'No Data Found. Please check the input files.' });
          return;
        }

        this.linientArray = [];
        this.mediumArray = [];
        this.strictArray = [];
        for (let i = 0; i < data['count_linient']; i++) {
          this.linientArray.push(data['sentence_linient'][i]);
        }
        for (let i = 0; i < data['count_medium']; i++) {
          this.mediumArray.push(data['sentence_medium'][i]);
        }
        for (let i = 0; i < data['count_strict']; i++) {
          this.strictArray.push(data['sentence_strict'][i]);
        }
        this.argusService.emitResult.next({
          'linient': this.linientArray,
          'medium': this.mediumArray,
          'strict': this.strictArray
        });

        if ((this.linientArray && this.linientArray.length == 0) &&
          (this.mediumArray && this.mediumArray.length == 0) &&
          (this.strictArray && this.strictArray.length == 0)) {
          // Show the modal for "No Data Found"
          this.openDialog({ 'errorTitle': 'Error', 'errorMessage': "Model output doesn't meet the acceptance criteria." });
          return;
        }
        // Routing to the ouput page.
        this.route.navigateByUrl('/output');
        return;
      }

      if (!data) {
        // Show the modal for "Exception Found"
        this.openDialog({ 'errorTitle': 'Exception', 'errorMessage': 'Exception occurs. Please check the logs.' });
      }
    });
  }
  openDialog(modalData) {
    const dialogRef = this.dialog.open(ErrorModalComponent, {
      width: '500px',
      data: modalData
    });
    this.showProgress = false;
  }

  submit() {
    this.showProgress = true;
    if(!this.isPdfSelected) {
      localStorage.setItem('output_pdf', '');
    }
    setTimeout(() => {
      this.callModel( this.trainingArray[0]['uploadName'], this.testingArray[0]['uploadName']);
    }, 1000);
  }

  saveTextAsFile(data, filename) {
    if (!data) {
      console.error("Console.save: No data");
      return;
    }

    if (!filename) filename = "F:\\Datascience_Project\\output.txt";

    var blob = new Blob([data], { type: "text/plain" }),
      e = document.createEvent("MouseEvents"),
      a = document.createElement("a");
    // FOR IE:

    if (window.navigator && window.navigator.msSaveOrOpenBlob) {
      window.navigator.msSaveOrOpenBlob(blob, filename);
    } else {
      var e = document.createEvent("MouseEvents"),
        a = document.createElement("a");

      a.download = filename;
      a.href = window.URL.createObjectURL(blob);
      a.dataset.downloadurl = ["text/plain", a.download, a.href].join(":");
      e.initEvent("click", true, false);
      a.dispatchEvent(e);
    }
  }

  triggerTraining(uploadEvent){
    console.log('printing ', uploadEvent);
    uploadEvent[0].upload();
  }
}
