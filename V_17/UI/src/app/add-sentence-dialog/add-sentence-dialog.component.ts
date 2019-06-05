import { Component, OnInit, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';
import { ArgusService } from '../service/argus.service';

@Component({
  selector: 'app-add-sentence-dialog',
  templateUrl: './add-sentence-dialog.component.html',
  styleUrls: ['./add-sentence-dialog.component.scss']
})
export class AddSentenceDialogComponent implements OnInit {

  constructor(public dialogRef: MatDialogRef<AddSentenceDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any, private argusService: ArgusService) { }

  ngOnInit() {

  }
  addSentence(selectedSentence){
    this.argusService.emitSelectedSenteces.next(selectedSentence);
    this.dialogRef.close();
  }
}
