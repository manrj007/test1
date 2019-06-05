import { Component, OnInit, ViewChild, EventEmitter, Inject, ChangeDetectorRef } from '@angular/core';
import { PdfViewerComponent } from 'ng2-pdf-viewer'
import { STATEMENTS } from '../constants/statements';
import { PdfViewerDialogComponent } from '../pdf-viewer-dialog/pdf-viewer-dialog.component';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material'
import { AddSentenceDialogComponent } from '../add-sentence-dialog/add-sentence-dialog.component';
import { ArgusService } from '../service/argus.service';
import { PDFProgressData, PDFDocumentProxy, PDFSource } from 'ng2-pdf-viewer';
import { FileSelectDirective, FileUploader } from 'ng2-file-upload';
import { HttpClient } from '@angular/common/http';
import { BASEURL } from '../constants/app.constants';
const uri = BASEURL;

@Component({
  selector: 'app-main-container',
  templateUrl: './main-container.component.html',
  styleUrls: ['./main-container.component.scss']
})
export class MainContainerComponent implements OnInit {
  src: string | PDFSource | ArrayBuffer = '';
  statements: any[] = [];
  searchText = new EventEmitter();
  selectedText: string = '';
  displayedColumns: string[] = ['no', 'trainingSentence', 'delete'];
  dataSource = [];

  displayedColumns_docs: string[] = ['no', 'name', 'action'];
  dataSource_docs = [];

  uploader: FileUploader = new FileUploader({ url: uri });
  attachmentList: any[] = [];
  documentLists: any[] = [];

  constructor(public dialog: MatDialog, private argusService:
    ArgusService, private changeDetectorRefs: ChangeDetectorRef, private http: HttpClient) {
    this.uploader.onCompleteItem = (item: any, response: any, status: any, headers: any) => {
      this.attachmentList.push(JSON.parse(response));
      //localStorage.setItem('preview', '');
      localStorage.setItem('preview', JSON.stringify(this.attachmentList));
      console.log(localStorage);
      this.setLocalStrorage();
    }
  }

  ngOnInit() {
    this.argusService.emitSelectedSenteces.subscribe((data) => {
      if (data) {
        this.statements.push(data);
        this.dataSource = this.statements.map((data, index) => {
          return {
            'no': index + 1,
            'trainingSentence': data.sentence,
            'delete': index
          }
        });
      }
    });
    this.setLocalStrorage();
  }
  setLocalStrorage() {
    let tempList = localStorage.getItem('preview');
    this.documentLists = JSON.parse(tempList);
    if(tempList) {
      this.dataSource_docs = this.documentLists.map((data, index) => {
        return {
          'no': index + 1,
          'name': data.originalName,
          'action': index
        }
      });
    }
  }
  showSelectedText() {
    var text = "";
    if (window.getSelection) {
      text = window.getSelection().toString();
    } else if (document['selection'] && document['selection'].type != "Control") {
      text = document['selection'].createRange().text;
    }
    this.selectedText = text;
    if (this.selectedText && this.selectedText.length > 0) {
      this.openDialog(this.selectedText);
    }
  }


  openDialog(selectedText) {
    const dialogRef = this.dialog.open(AddSentenceDialogComponent, {
      width: '500px',
      data: { sentence: selectedText }
    });
  }

  deleteItem(index) {
    this.statements.splice(index, 1);

    this.dataSource = this.statements.map((data, index) => {
      return {
        'no': index + 1,
        'trainingSentence': data.sentence,
        'delete': index
      }
    });
  }

  downloadTrainingDocument() {
    let fileName = 'Training_document.txt';
    if (!this.dataSource) {
      console.error("Console.save: No data");
      return;
    }
    let final_sentence = '';
    this.dataSource.forEach((lines) => {
      final_sentence = final_sentence + '\r\n' + lines.trainingSentence;
    });
    final_sentence = final_sentence.trim();
    var blob = new Blob([final_sentence], { type: "text/plain" }),
      e = document.createEvent("MouseEvents"),
      a = document.createElement("a");

    // FOR IE:

    if (window.navigator && window.navigator.msSaveOrOpenBlob) {
      window.navigator.msSaveOrOpenBlob(blob, fileName);
    } else {
      var e = document.createEvent("MouseEvents"),
        a = document.createElement("a");

      a.download = fileName;
      a.href = window.URL.createObjectURL(blob);
      a.dataset.downloadurl = ["text/plain", a.download, a.href].join(":");
      e.initEvent("click", true, false);
      a.dispatchEvent(e);
    }
  }

  uploadPDF() {
    let $img: any = document.querySelector('#file');
    if (typeof (FileReader) !== 'undefined') {
      let reader = new FileReader();
      reader.onload = (e: any) => {
        this.src = e.target.result;
      };
      reader.readAsArrayBuffer($img.files[0]);
      this.saveToLocal($img.files[0].name, $img.files[0]);

    }
  }

  saveToLocal(fileName, fileData) {
    this.argusService.saveToLocal(fileName, fileData);
  }

  viewItem(index) {
    this.http.get(`${uri}/${this.documentLists[index].uploadName}`, { responseType: 'arraybuffer' }).subscribe((data) => {
      console.log(data);
      this.src = data;
    });
  }

  search(item) {
    this.dialog.open(PdfViewerDialogComponent, {
      data: {
        searchText: item.searchText,
        fileName: item.filename
      }
    });

  }
}
