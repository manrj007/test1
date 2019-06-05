import { Component, OnInit, Inject, ViewChild } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material';
import { PdfViewerComponent } from 'ng2-pdf-viewer';

@Component({
  selector: 'app-pdf-viewer-dialog',
  templateUrl: './pdf-viewer-dialog.component.html',
  styleUrls: ['./pdf-viewer-dialog.component.scss']
})
export class PdfViewerDialogComponent implements OnInit {
  src: string;
  constructor(@Inject(MAT_DIALOG_DATA) public data: any) { }

  @ViewChild(PdfViewerComponent) private pdfComponent: PdfViewerComponent;

  ngOnInit() {
    this.src = `../assets/Testing_data/${this.data.fileName}.pdf`;
    setTimeout(() => {
      this.pdfComponent.pdfFindController.executeCommand('find', {
        caseSensitive: false, findPrevious: undefined, highlightAll: true, phraseSearch: true, query: this.data.searchText
      });
      console.log('highlighted');
    }, 1000)
  }
}
