import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormBuilder, Validators} from '@angular/forms';
import { PdfViewerComponent } from 'ng2-pdf-viewer';
import { ArgusService } from '../service/argus.service';
import { HttpClient } from '@angular/common/http';
import { BASEURL } from '../constants/app.constants';
const uri = BASEURL + '/testing_pdf/';
import * as _ from 'lodash'; 
@Component({
  selector: 'app-output',
  templateUrl: './output.component.html',
  styleUrls: ['./output.component.scss']
})
export class OutputComponent implements OnInit {
  src: any;
  searchText: string;
  searchText_1: string;
  finalSentences: any = [];
  form: FormGroup;
  outputFileName: string;
  // sente = "Hilton Worldwide and its Affiliates own, license, lease, operate, manage and provide various services for the Network.";
  constructor(private argusService: ArgusService, private fb: FormBuilder,
    private http: HttpClient) { 
    this.outputFileName = localStorage.getItem('output_pdf');
  }
  @ViewChild(PdfViewerComponent) private pdfComponent: PdfViewerComponent;
  ngOnInit() {
    this.form = this.fb.group({
      model_type: ['linient', Validators.required]
    });
    this.getData('linient');
    
    setTimeout(() => {
      this.getOutputDocument();
      console.log('time out', this.outputFileName);
    }, 200);
  }
  onChange() {
    this.getData(this.form.value.model_type);
  }
  getData(value) {
    this.finalSentences = [];
    this.argusService.emitResult.subscribe((result) => {
      if(result) {
        console.log(result);
        this.finalSentences =_.uniq(result[value]);
      }
    });
  }
  getOutputDocument() {
    console.log(this.outputFileName);
    console.log(uri);
    this.http.get(`${uri}${ this.outputFileName }`, { responseType: 'arraybuffer' }).subscribe((data) => {
      console.log("asdjklashdkajsdhasjdh",data);
      this.src = data;
    });
  }
  search(searchText) {
    searchText = searchText.trim();
    console.log("***", searchText + "***");
      this.pdfComponent.pdfFindController.executeCommand('find', {
        caseSensitive: false, findPrevious: undefined, highlightAll: true, phraseSearch: true, query: searchText
      });
  }
}
