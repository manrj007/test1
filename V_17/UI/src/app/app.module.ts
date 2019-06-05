import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './material.module';
import { MatFileUploadModule } from 'angular-material-fileupload';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { LeftPanelComponent } from './left-panel/left-panel.component';
import { MainContainerComponent } from './main-container/main-container.component';
import { CompareComponent } from './compare/compare.component';
import { ViewComponent } from './view/view.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { PdfViewerModule } from 'ng2-pdf-viewer';
import { PdfViewerDialogComponent } from './pdf-viewer-dialog/pdf-viewer-dialog.component';
import { OutputComponent } from './output/output.component';
import { AddSentenceDialogComponent } from './add-sentence-dialog/add-sentence-dialog.component';
import { ErrorModalComponent } from './error-modal/error-modal.component';
import { FileUploadModule } from 'ng2-file-upload';

@ NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    LeftPanelComponent,
    MainContainerComponent,
    CompareComponent,
    ViewComponent,
    PdfViewerDialogComponent,
    OutputComponent,
    AddSentenceDialogComponent,
    ErrorModalComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    MatFileUploadModule,
    FormsModule,
    ReactiveFormsModule,
    PdfViewerModule,
    HttpClientModule,
    FileUploadModule
  ],
  providers: [],
  bootstrap: [AppComponent],
  entryComponents: [PdfViewerDialogComponent, AddSentenceDialogComponent, ErrorModalComponent]
})
export class AppModule { }
